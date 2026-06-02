from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskAPITests(APITestCase):
    def setUp(self):
        self.task_data = {
            'title': 'Test DRF Task',
            'description': 'This is a test description',
            'status': 'todo',
            'priority': 'medium'
        }
        self.task = Task.objects.create(**self.task_data)
        self.list_url = reverse('task-list')
        self.detail_url = reverse('task-detail', kwargs={'pk': self.task.id})

    def test_create_task(self):
        """Ensure we can create a new task object."""
        data = {
            'title': 'New Task Title',
            'description': 'New task description',
            'status': 'in_progress',
            'priority': 'high'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(id=response.data['id']).title, 'New Task Title')

    def test_get_tasks_list(self):
        """Ensure we can retrieve a list of tasks."""
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.task.title)

    def test_get_single_task_detail(self):
        """Ensure we can retrieve a single task detail."""
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_update_task(self):
        """Ensure we can update an existing task."""
        data = {
            'title': 'Updated Task Title',
            'description': 'Updated task description',
            'status': 'done',
            'priority': 'low'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task Title')
        self.assertEqual(self.task.status, 'done')

    def test_delete_task(self):
        """Ensure we can delete a task."""
        response = self.client.delete(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
