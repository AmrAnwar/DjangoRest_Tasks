import json

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ..models import Task
from ..factories import TaskFactory


class TestViewTask(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(
            username='tester',
            email='amranwar945@gmail.com',
        )
        self.user.set_password('password')
        self.user.save()
        self.client.login(username="tester", password="password")
        self.task = TaskFactory.create(user=self.user)
        self.task_list_url = reverse("tasks-list")
        self.task_url = self.task.get_absolute_url()
        TaskFactory.create_batch(20)
        self.task_create_data = {
            "title": "hello there",
            "description": "it's me"
        }
        self.update_data = {
            "title": "hello there :v",
            "description": "it's me again"
        }
        self.task_data_linked_task = {
            "linked_task": 2,
        }

    def test_get_list(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)

    def test_get_detail(self):
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        count = Task.objects.count()
        response = self.client.post(self.task_list_url, json.dumps(self.task_create_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(count+1, Task.objects.count())

    def test_update(self):
        # state 1 NEW
        response = self.client.patch(self.task_url, json.dumps(self.update_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(self.task_url, json.dumps(self.task_data_linked_task),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        forbidden_data_state = {
            "state": 3
        }
        response = self.client.patch(self.task_url, json.dumps(forbidden_data_state),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        valid_data_state = {
            "state": 2
        }
        response = self.client.patch(self.task_url, json.dumps(valid_data_state),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # state 2 PROGRESS

        response = self.client.patch(self.task_url, json.dumps(self.task_create_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(self.task_url, json.dumps(self.task_data_linked_task),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

        forbidden_data_state = {
            "state": 1
        }
        response = self.client.patch(self.task_url, json.dumps(forbidden_data_state),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        valid_data_state = {
            "state": 3
        }
        response = self.client.patch(self.task_url, json.dumps(valid_data_state),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # state 3 DONE

        response = self.client.patch(self.task_url, json.dumps(self.task_create_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(self.task_url, json.dumps(self.task_data_linked_task),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        forbidden_data_state = {
            "state": 1
        }
        response = self.client.patch(self.task_url, json.dumps(forbidden_data_state),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        forbidden_data_state = {
            "state": 2
        }
        response = self.client.patch(self.task_url, json.dumps(forbidden_data_state),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_forbidden_delete(self):
        response = self.client.delete(self.task_url)
        self.assertEqual(response.status_code, 405)
