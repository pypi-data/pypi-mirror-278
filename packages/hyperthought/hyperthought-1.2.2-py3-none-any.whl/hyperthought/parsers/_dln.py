from datetime import datetime
import dateutil.parser
import json

from ..parsers.base import BaseParser
from ..metadata import MetadataItem

# ## Develop parser class
# Extend the parser base class to define a parser for DLN JSON files.


CONTAINER_INPUT_USED_KEYS = ("inputName", "inputValue",)
CONTAINER_INPUT_IGNORED_KEYS = ("files",)
CONTAINER_INPUT_CHILD_KEYS = ("inputDate", "emailAddress",)
DATE_VALUE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_ANNOTATION_FORMATS = ("%Y-%m-%dT%H:%M:%S.%f%z", "%m/%d/%y %I:%M %p")


def get_annotation(input_, used_keys=None, has_child=False):
    """Generate metadata annotation from unused keys in container input."""
    if not isinstance(input_, dict):
        raise ValueError("input_ parameter to get_annotation must be a dict")

    if used_keys is None:
        used_keys = set()
        used_keys.update(CONTAINER_INPUT_USED_KEYS)

    if has_child:
        used_ = set()
        used_.update(used_keys)
        used_.update(CONTAINER_INPUT_CHILD_KEYS)
        used_keys = used_

    ignored_keys = CONTAINER_INPUT_IGNORED_KEYS

    annotation = ""

    for key in input_:
        if key in used_keys or key in ignored_keys:
            continue

        annotation += f"{key}={input_[key]}, "

    # Removing trailing ", ".
    annotation = annotation[:-2]

    return annotation


def convert(value):
    """Attempt to convert a string value to a numeric type."""
    if not isinstance(value, str):
        return value

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    try:
        date_ = dateutil.parser.parse(value)
        return date_.strftime(DATE_VALUE_FORMAT)
    except (ValueError, TypeError):
        pass

    return value


def has_value(value_):
    """
    Check if this has been passed a meaningful value.
    This includes zero and False as meaningful.
    """
    if isinstance(value_, (int, float, bool)):
        return True
    return bool(value_)


def get_date_annotation(value, formats=None):
    """Generate an annotation from a date value in the provided date formats."""
    if not isinstance(value, datetime):
        try:
            date_ = dateutil.parser.parse(value)
        except (ValueError, TypeError):
            return None
    else:
        date_ = value

    annotation = ""

    if formats is None:
        formats = DATE_ANNOTATION_FORMATS

    for format_ in formats:
        annotation += f"{date_.strftime(format_)}, "

    annotation = annotation[:-2]

    return annotation


class AmDigitalLabNotebook(BaseParser):
    """
    Parse data from an AM Lab digital lab notebook JSON file.
    Nests the metadata by the screen.
    """

    VALID_EXTENSIONS = {"json"}

    def parse(self):
        """Parse data from a DLN JSON file."""
        try:
            with open(self._file_path, 'r') as fh:
                data = json.load(fh)
        except Exception as e:
            # Add exception message to error and re-raise.
            raise ValueError(
                f"{type(e).__name__}: {e}\n"
                "Unable to open specified file.  "
                "Is the content formatted as JSON?"
            )

        metadata = []

        self.get_common_fields(data=data, metadata=metadata)

        # add all user provided tags
        # and get the names of auto-tagged inputs from the list of tags.
        tagged_input_names = set()
        if "tags" in data and isinstance(data["tags"], list):
            for tag in data["tags"]:
                if "value" not in tag:
                    continue

                if "name" not in tag:
                    tag_name = "tag"
                else:
                    tag_name = tag["name"]

                if "autoTag" in tag:
                    auto_tagged = tag["autoTag"]
                    if auto_tagged:
                        tagged_input_names.add(tag_name)
                    else:
                        metadata.append(
                            MetadataItem(
                                key=tag_name,
                                value=convert(tag["value"]),
                            )
                        )

        # Get inputs from containers.
        if "containers" in data:
            self.get_containers(
                containers=data["containers"],
                metadata=metadata,
                selected_inputs=tagged_input_names
            )

        # Set metadata.
        self.metadata = metadata

    def get_common_fields(self, data, metadata):
        """Creates metadata items for common fields of notebook entries."""
        # Add title, if present.
        if "title" in data:
            metadata.append(
                MetadataItem(
                    key="Title",
                    value=data["title"],
                )
            )

        # Add project name, if present.
        if "projectName" in data:
            metadata.append(
                MetadataItem(
                    key="Project Name",
                    value=data["projectName"],
                )
            )

        # Add program name, if present.
        if "programName" in data:
            metadata.append(
                MetadataItem(
                    key="Program Name",
                    value=data["programName"],
                )
            )

        # Add point of contact, if present.
        if "pointOfContact" in data:
            metadata.append(
                MetadataItem(
                    key="Point Of Contact",
                    value=data["pointOfContact"],
                )
            )
            metadata.append(
                MetadataItem(
                    key="POC",
                    value=data["pointOfContact"],
                )
            )

        # Add charge number, if present.
        if "chargeNumber" in data:
            metadata.append(
                MetadataItem(
                    key="Charge Number",
                    value=data["chargeNumber"],
                )
            )

        # Add start and modified or end dates, if present.
        # Dates are stored as strings in our database, so format them for search.
        if "startDate" in data:
            metadata.append(
                MetadataItem(
                    key="Start Date",
                    value=convert(data["startDate"]),
                    annotation=get_date_annotation(data["startDate"]),
                )
            )

        if "endDate" in data:
            metadata.append(
                MetadataItem(
                    key="End Date",
                    value=convert(data["endDate"]),
                    annotation=get_date_annotation(data["endDate"]),
                )
            )
        elif "modifiedDate" in data:
            metadata.append(
                MetadataItem(
                    key="Modified Date",
                    value=convert(data["modifiedDate"]),
                    annotation=get_date_annotation(data["modifiedDate"]),
                )
            )

    def get_containers(self, containers, metadata, selected_inputs=None):
        """
        Generate nested metadata items from the list of container entry data.
        """
        screens_set = set()
        screen_container_set = set()

        dynamic_screens = set()
        multiple_containers = set()

        # loop through containers to get which screens repeat
        # screen either repeat because they are dynamic screens
        # or because they have multiple containers
        for container in containers:
            screen_name = (
                container["screenName"]
                if "screenName" in container
                else None
            )
            container_name = (
                container["containerName"]
                if "containerName" in container
                else None
            )
            index_ = (
                container["index"]
                if "index" in container
                else 0
            )
            if not screen_name or not container_name:
                continue
            screen_container = screen_name + container_name

            if screen_name in screens_set:
                if screen_container not in screen_container_set:
                    multiple_containers.add(screen_name)
                if index_ != 0:
                    dynamic_screens.add(screen_name)

            screens_set.add(screen_name)
            screen_container_set.add(screen_container)

        screen_item_dict = {}

        # create the nested metadata items
        for container in containers:
            screen_name = (
                container["screenName"]
                if "screenName" in container
                else "Unnamed screen"
            )
            container_name = (
                container["containerName"]
                if "containerName" in container
                else "Unnamed container"
            )
            index_ = (
                container["index"]
                if "index" in container
                else 0
            )

            # create the container metadata item
            container_item = MetadataItem(
                key=container_name,
            )

            # if it is a dynamic screen add the screen number to the name
            if screen_name in dynamic_screens:
                screen_number = "{:0>4}".format(index_ + 1)
                screen_name = f"{screen_number} {screen_name}"

            screen_item = screen_item_dict.get(
                screen_name,
                MetadataItem(
                    key=screen_name,
                    children=[]
                )
            )

            # create inputs metadata add as children to container item
            if "inputs" in container:
                input_items = []
                inputs_found = False

                for input_ in container["inputs"]:
                    if "inputName" in input_ and "inputValue" in input_:
                        input_name = input_["inputName"]
                        if selected_inputs is None or input_name in selected_inputs:
                            input_value_ = convert(input_["inputValue"])

                            if has_value(input_value_):
                                inputs_found = True
                                annotation_ = get_annotation(input_=input_, has_child=True,)
                                date_annotation = get_date_annotation(input_value_)
                                if annotation_:
                                    annotation_ += f", {date_annotation}"
                                else:
                                    annotation_ = date_annotation
                                children_ = self.get_input_children(input_=input_)

                                input_items.append(
                                    MetadataItem(
                                        key=input_name,
                                        value=input_value_,
                                        annotation=annotation_,
                                        children=children_,
                                    )
                                )

                # add inputs/container to screen only if an input values was found
                if inputs_found:
                    container_item.children = input_items
                    screen_item.add_child(child=container_item)
                    if screen_name not in screen_item_dict:
                        metadata.append(screen_item)
                        screen_item_dict[screen_name] = screen_item

    def get_input_children(self, input_, child_keys=None):
        """Creates child metadata items for specific keys in the supplied input json object."""
        if not isinstance(input_, dict):
            return []

        if child_keys is None:
            child_keys = CONTAINER_INPUT_CHILD_KEYS

        children_items = []

        for input_key in input_:
            if input_key in child_keys:
                date_annotation = get_date_annotation(input_[input_key])
                children_items.append(
                    MetadataItem(
                        key=input_key,
                        value=input_[input_key],
                        annotation=date_annotation,
                    )
                )

        return children_items
