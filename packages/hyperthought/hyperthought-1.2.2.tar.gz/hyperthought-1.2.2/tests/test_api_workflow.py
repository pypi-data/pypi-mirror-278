import datetime
import re
import time
import unittest

import hyperthought as ht
import yaml


UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$',
    flags=re.IGNORECASE
)


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        with open('setup.yml', 'r') as f:
            self.setup = yaml.safe_load(f)

        self.auth = ht.auth.TokenAuthentication(
            self.setup['auth']['info'],
            verify=False,
            delayed_refresh=True,
        )
        self.workflow_api = ht.api.workflow.WorkflowAPI(auth=self.auth)
        self.space_id = self.setup['api']['workflow']['space_id']
        workflow = ht.api.workflow.Workflow(
            name='setup_workflow',
            space_id=self.space_id,
        )
        process = ht.api.workflow.Process(
            name='Process01',
            parent_id=workflow.id,
        )
        workflow.add_child(process)
        self.workflow_api.create_workflow(workflow=workflow)
        self.setup_workflow_id = workflow.id

    def test_get_templates(self):
        templates = self.workflow_api.get_templates(self.space_id)
        self.assertIsNotNone(templates)
        self.assertTrue(
            len(templates) >= 1,
            msg='Is the response an array that contains things?'
        )
        for entry in templates:
            self.assertIn('title', entry)
            self.assertIn('key', entry)
            self.assertRegex(
                entry['key'], UUID_RE,
                msg="Does the key look like an ID?"
            )
            self.assertIn('name', entry)
            self.assertIn('icon', entry)
            self.assertIn('lazy', entry)

    def test_get_children(self):
        workflow_id = self.setup_workflow_id
        children = self.workflow_api.get_children(workflow_id)
        self.assertIsNotNone(children)
        self.assertTrue(
            len(children) >= 1,
            msg='Is the response an array that contains things?'
        )
        for entry in children:
            self.assertIn('content', entry)
            self.assertIn('status', entry['content'])
            self.assertIn('xml', entry['content'])
            self.assertIn('name', entry['content'])
            self.assertIn('parent_process', entry['content'])
            self.assertIn('children', entry['content'])
            self.assertIn('predecessors', entry['content'])
            self.assertIn('successors', entry['content'])
            self.assertIn('process_type', entry['content'])
            self.assertIn('template', entry['content'])
            self.assertIn('pk', entry['content'])
            self.assertIn('hyperthought', entry)
            self.assertIn('name', entry['hyperthought'])
            self.assertIn('objectType', entry['hyperthought'])
            self.assertIn('triples', entry)
            self.assertIn('metadata', entry)
            self.assertIn('permissions', entry)
            self.assertIn('restrictions', entry)
            self.assertIn('headers', entry)

    def test_update_document(self):
        document_id = self.setup_workflow_id
        document = self.workflow_api.get_document(document_id)
        self.assertIsNotNone(document)
        self.assertIn('name', document)
        orig_name = document['name']
        new_name = f'Test update {orig_name}'
        document['name'] = new_name
        self.workflow_api.update_document(document)
        updated_document = self.workflow_api.get_document(document_id)
        self.assertIsNotNone(updated_document)
        self.assertIn('name', updated_document)
        self.assertEqual(updated_document['name'], new_name)

    def test_create_workflow(self):
        workflow = ht.api.workflow.Workflow(
            name='test_create_workflow',
            space_id=self.space_id,
        )
        process = ht.api.workflow.Process(
            name='Process01',
            parent_id=workflow.id,
        )
        workflow.add_child(process)
        self.workflow_api.create_workflow(workflow=workflow)
        workflow_document = self.workflow_api.get_document(workflow.id)
        self.assertIsNotNone(workflow_document)
        self.assertIn('name', workflow_document)
        self.assertEqual(workflow_document['name'], 'test_create_workflow')
        self.assertIn('children', workflow_document)
        self.assertEqual(len(workflow_document['children']), 1)

    def test_create_process(self):
        workflow = ht.api.workflow.Workflow(
            name='test_create_process',
            space_id=self.space_id,
        )
        self.workflow_api.create_workflow(workflow=workflow)
        process = ht.api.workflow.Process(
            parent_id=workflow.id,
            name="NewProcess"
        )
        self.workflow_api.create_process(process=process)
        process_document = self.workflow_api.get_document(process.id)
        self.assertIsNotNone(process_document)
        self.assertIn('name', process_document)
        self.assertEqual(process_document['name'], 'NewProcess')

    def test_get_document(self):
        document_id = self.setup_workflow_id
        document = self.workflow_api.get_document(document_id)
        self.assertIsNotNone(document)
        self.assertIn('name', document)

    def test_get_active_workflows(self):
        active_workflows = self.workflow_api.get_active_workflows(
            self.space_id)
        self.assertTrue('In Progress' in active_workflows)
        self.assertTrue(isinstance(active_workflows['In Progress'], list))

    def test_add_link(self):
        workflow = ht.api.workflow.Workflow(
            name='test_add_link',
            space_id=self.space_id,
        )
        process_01 = ht.api.workflow.Process(
            name='Process01',
            parent_id=workflow.id,
        )
        workflow.add_child(process_01)
        process_02 = ht.api.workflow.Process(
            name='Process02',
            parent_id=workflow.id,
        )
        workflow.add_child(process_02)
        self.workflow_api.create_workflow(workflow=workflow)
        self.workflow_api.add_link(
            source_id=process_01.id,
            target_id=process_02.id,
        )
        self.workflow_api.redraw_canvas(workflow_id=workflow.id)
        process_01_document = self.workflow_api.get_document(
            document_id=process_01.id)
        self.assertIn(process_02.id, process_01_document['successors'])
        process_02_document = self.workflow_api.get_document(
            document_id=process_02.id)
        self.assertIn(process_01.id, process_02_document['predecessors'])

    def test_redraw_canvas(self):
        workflow = ht.api.workflow.Workflow(
            name='test_redraw_canvas',
            space_id=self.space_id,
        )
        self.workflow_api.create_workflow(workflow=workflow)
        process_name = "NewProcess"
        process = ht.api.workflow.Process(
            parent_id=workflow.id,
            name=process_name,
        )
        self.workflow_api.create_process(process=process)
        self.workflow_api.redraw_canvas(workflow_id=workflow.id)
        workflow_document = self.workflow_api.get_document(
            document_id=workflow.id)
        self.assertTrue(process_name in workflow_document['xml'])

    def test_create_decision_indirectly(self):
        workflow = ht.api.workflow.Workflow(
            name='test_create_decision_indirectly',
            space_id=self.space_id,
        )
        decision = ht.api.workflow.Decision(
            parent_id=workflow.id,
            name="Decision",
            decision_question="Does this work?",
        )
        workflow.add_child(decision)
        yes_process = ht.api.workflow.Process(
            parent_id=workflow.id,
            name="If Yes"
        )
        workflow.add_child(yes_process)
        decision.add_successor(element=yes_process, successor_type='yes')
        no_process = ht.api.workflow.Process(
            parent_id=workflow.id,
            name="If No"
        )
        workflow.add_child(no_process)
        decision.add_successor(element=no_process, successor_type='no')
        self.workflow_api.create_workflow(workflow=workflow)
        decision_document = self.workflow_api.get_document(decision.id)
        self.assertEqual(decision.id, decision_document['id'])
        self.assertEqual(
            decision_document['decisionPath'][yes_process.id],
            'yes'
        )
        self.assertEqual(
            decision_document['decisionPath'][no_process.id],
            'no'
        )

    def test_execute_workflow(self):
        test_execute_workflow = ht.api.workflow.Workflow(
            name='test_execute_workflow',
            space_id=self.space_id,
        )
        ht.api.workflow.Process(
            parent=test_execute_workflow,
            name='Process 1',
            metadata=[]
        )
        self.workflow_api.create_workflow(workflow=test_execute_workflow)
        workflow_document = self.workflow_api.get_document(
            test_execute_workflow.id)
        self.assertEqual(test_execute_workflow.id, workflow_document['id'])
        old_workflow_count = len(
            self.workflow_api.get_active_workflows(
                self.space_id,
            )["In Progress"]
        )
        workflow_name = 'test_execute_workflow'
        self.workflow_api.execute_workflow(
            template_id=test_execute_workflow.id,
            workflow_name=workflow_name,
        )

        for _ in range(10):
            new_workflows = self.workflow_api.get_active_workflows(
                self.space_id,
            )["In Progress"]
            new_workflow_count = len(new_workflows)

            if new_workflow_count > old_workflow_count:
                break

            time.sleep(1)

        self.assertGreater(new_workflow_count, old_workflow_count)
        workflow_names = [
            workflow["title"]
            for workflow in new_workflows
        ]
        self.assertIn(workflow_name, workflow_names)

    def test_accept(self):
        """
        Test the method for accepting a workflow.

        See hyperthought.api.workflow.WorkflowAPI.accept.
        """
        # Create the workflow to be used in the test.
        now = datetime.datetime.now()
        timestamp = (
            f"{now.year:04}{now.month:02}{now.day:02}_"
            f"{now.hour:02}{now.minute:02}{now.second:02}"
        )
        workflow_name = f"test_accept_workflow_{timestamp}"
        workflow_template = ht.api.workflow.Workflow(
            name=workflow_name,
            space_id=self.space_id,
        )
        ht.api.workflow.Process(
            name='Process 1',
            parent=workflow_template,
        )
        self.workflow_api.create_workflow(workflow=workflow_template)
        self.workflow_api.execute_workflow(
            template_id=workflow_template.id,
            workflow_name=workflow_name,
        )

        # Get the new workflow.
        # This is in a loop in case workflow execution takes non-trivial time.
        max_iterations = 10
        workflow = None

        for _ in range(max_iterations):
            workflows = self.workflow_api.get_active_workflows(
                self.space_id,
            )["In Progress"]

            for workflow in workflows:
                if workflow["name"] == workflow_name:
                    break

        self.assertIsNotNone(workflow)

        # Get the child elements to be accepted.
        children = self.workflow_api.get_children(workflow_id=workflow["key"])

        # Accept all children.
        for child in children:
            self.workflow_api.accept(element_id=child["content"]["pk"])

        # Get children again after accepting.
        children = self.workflow_api.get_children(workflow_id=workflow["key"])

        # Verify assignee and status for children.
        expected_assignee = self.auth.get_username()
        expected_status = "in progress"

        for child in children:
            assignee = child["content"]["assignee"]
            self.assertEqual(expected_assignee, assignee)
            status = child["content"]["status"]
            self.assertEqual(expected_status, status)

    def test_complete(self):
        """
        Test the method for completing a workflow.

        See hyperthought.api.workflow.WorkflowAPI.complete.
        """
        # Create the workflow to be used in the test.
        now = datetime.datetime.now()
        timestamp = (
            f"{now.year:04}{now.month:02}{now.day:02}_"
            f"{now.hour:02}{now.minute:02}{now.second:02}"
        )
        workflow_name = f"test_complete_workflow_{timestamp}"
        workflow_template = ht.api.workflow.Workflow(
            name=workflow_name,
            space_id=self.space_id,
        )
        ht.api.workflow.Process(
            name='Process 1',
            parent=workflow_template,
            assignee=self.auth.get_username(),
        )
        self.workflow_api.create_workflow(workflow=workflow_template)
        self.workflow_api.execute_workflow(
            template_id=workflow_template.id,
            workflow_name=workflow_name,
        )

        # Get the new workflow.
        # This is in a loop in case workflow execution takes non-trivial time.
        max_iterations = 10
        workflow = None

        for _ in range(max_iterations):
            workflows = self.workflow_api.get_active_workflows(
                self.space_id,
            )["In Progress"]

            for workflow in workflows:
                if workflow["name"] == workflow_name:
                    break

        self.assertIsNotNone(workflow)

        # Get the child elements to be completed.
        children = self.workflow_api.get_children(workflow_id=workflow["key"])

        # Complete all children.
        for child in children:
            self.workflow_api.complete(element_id=child["content"]["pk"])

        # Get children again after completing.
        children = self.workflow_api.get_children(workflow_id=workflow["key"])

        # Verify statuses of all children.
        expected_status = "complete"

        for child in children:
            status = child["content"]["status"]
            self.assertEqual(expected_status, status)

        # Get the workflow again.  Make sure it is in the "Complete" group.
        workflow = None
        workflows = self.workflow_api.get_active_workflows(
            self.space_id,
        )["Complete"]

        for workflow in workflows:
            if workflow["name"] == workflow_name:
                break

        self.assertIsNotNone(workflow)

    def _create_test_workflow(self):
        """
        Create a workflow to be used in various tests.

        Structure
        ---------
        W(A, {P(B) -> P(C) -> W(D, {P(E)}}),
        where the first values in parentheses are workflow names,
        W is a workflow, P is a process, curly braces indicate containership,
        and arrows indicate sequencing.

        Returns
        -------
        A dictionary with workflow names as keys, and dictionaries with keys
        "id" and "client_id" as values.
        """
        A = ht.api.workflow.Workflow(space_id=self.space_id, name="A")
        B = ht.api.workflow.Process(name="B", parent=A)
        C = ht.api.workflow.Process(name="C", parent=A)
        B.add_successor(C)
        D = ht.api.workflow.Workflow(name="D", parent=A)
        C.add_successor(D)
        E = ht.api.workflow.Process(name="E", parent=D)
        self.workflow_api.create_workflow(workflow=A)
        return {
            "A": {
                "id": A.id,
                "client_id": A.client_id,
            },
            "B": {
                "id": B.id,
                "client_id": B.client_id,
            },
            "C": {
                "id": C.id,
                "client_id": C.client_id,
            },
            "D": {
                "id": D.id,
                "client_id": D.client_id,
            },
            "E": {
                "id": E.id,
                "client_id": E.client_id,
            },
        }

    def test_delete(self):
        # Create a test workflow and get the root id.
        name_to_ids = self._create_test_workflow()
        root_id = name_to_ids["A"]["id"]

        # Make sure the root id can be found.
        templates = self.workflow_api.get_templates(space_id=self.space_id)
        template_ids = {template["key"] for template in templates}
        assert root_id in template_ids

        # Delete the root workflow.
        self.workflow_api.delete(element_id=root_id)

        # Make sure the root id cannot be found.
        templates = self.workflow_api.get_templates(space_id=self.space_id)
        template_ids = {template["key"] for template in templates}
        assert root_id not in template_ids

    def test_subworkflow_deletion(self):
        # Create a test workflow and get the root id.
        name_to_ids = self._create_test_workflow()
        root_id = name_to_ids["A"]["id"]

        # Make sure the root id can be found.
        templates = self.workflow_api.get_templates(space_id=self.space_id)
        template_ids = {template["key"] for template in templates}
        assert root_id in template_ids

        # Delete the subworkflow workflow.
        subworkflow_id = name_to_ids["D"]["id"]
        self.workflow_api.delete(element_id=subworkflow_id)

        # Get the root workflow.  Make sure the subworkflow cannot be found in
        # children or xml.
        root_workflow = self.workflow_api.get_document(document_id=root_id)
        assert subworkflow_id not in root_workflow["children"]
        subworkflow_client_id = name_to_ids["D"]["client_id"]
        assert subworkflow_client_id not in root_workflow["xml"]

    def test_process_deletion(self):
        # Create a test workflow and get the root id.
        name_to_ids = self._create_test_workflow()
        root_id = name_to_ids["A"]["id"]

        # Make sure the root id can be found.
        templates = self.workflow_api.get_templates(space_id=self.space_id)
        template_ids = {template["key"] for template in templates}
        assert root_id in template_ids

        # Delete the E process.
        process_id = name_to_ids["E"]["id"]
        self.workflow_api.delete(element_id=process_id)

        # Get the subworkflow that contains E (D).
        # Make sure the process cannot be found in children or xml.
        workflow_id = name_to_ids["D"]["id"]
        workflow = self.workflow_api.get_document(document_id=workflow_id)
        assert process_id not in workflow["children"]
        process_client_id = name_to_ids["E"]["client_id"]
        assert process_client_id not in workflow["xml"]
