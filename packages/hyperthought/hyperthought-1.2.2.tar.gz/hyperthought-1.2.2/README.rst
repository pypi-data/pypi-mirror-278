============
hyperthought
============


Modules that encapsulate HyperThought API calls and make
operations like authentication and file transfer (upload
or download) easier to accomplish.

Description
===========

Example usage:

Here is the code needed to upload a file to a HyperThought workspace.

.. code-block:: python

    from getpass import getpass
    import hyperthought as ht

    auth_info = getpass("Enter encoded auth info from your HyperThought profile page: ")
    auth = ht.auth.Authorization(auth_info)
    files_api = ht.api.files.FilesAPI(auth)

    # space_id can be found in the url for the workspace
    # e.g. https://www.hyperthought.io/workspace/<space_id>/detail
    space_id = input("Enter destination project id (in url of project): ")

    # Create a folder.
    # Use default (root) path and don't specify any metadata for the folder.
    # (See method docstring for info on unused parameters.)
    folder_id = files_api.create_folder(
        name="Tests",
        space_id=space_id,
    )

    # Get a path for the file.
    # Paths consist of comma-separated parent folder ids.
    path = f",{folder_id},"

    local_file_path = input("Enter path to local file: ")
    files_api.upload(
        local_path=local_file_path,
        space_id=space_id,
        path=path,
    )
    # Look in the HyperThought UI to see the uploaded file.
