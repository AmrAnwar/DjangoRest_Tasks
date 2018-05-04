from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Task(models.Model):
    """
    The Task Model, the instance states determined by the state field
    """
    STATES = (
        (1, 'NEW'),
        (2, 'PROGRESS'),
        (3, 'DONE'),
    )
    user = models.ForeignKey(User,
                             related_name="task_user", on_delete=models.CASCADE)
    linked_task = models.OneToOneField("tasks.Task",
                                       related_name="outer_task", null=True, blank=True)

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    state = models.IntegerField(choices=STATES, default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        :return: for ex: /tasks/1
        """
        return reverse("tasks-detail", args=[self.pk])
