from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


from ..models import Task
from ..serializers import TaskModelSerializer


class TaskModelViewSet(viewsets.ModelViewSet):
    """
    Task Model View Set
    """
    http_method_names = ('get', 'post', 'head', 'patch', 'put',)
    serializer_class = TaskModelSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('state',)

    def get_queryset(self):
        """
        :return: tasks for the auth user
        """
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        save user in a task serializer
        """
        serializer.save(user=self.request.user, linked_task=None, state=1)
