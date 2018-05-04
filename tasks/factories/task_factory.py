import factory
from django.contrib.auth.models import User
from ..models import Task


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = Task

    user = factory.Iterator(User.objects.all())

    title = factory.Faker('text')
    description = factory.Faker('text')
