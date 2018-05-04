from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField, ValidationError

from ..models import Task


class SimpleTaskModelSerializer(serializers.ModelSerializer):
    """
    Task Model Serializer
    """
    url = SerializerMethodField()

    class Meta:
        model = Task
        fields = ('pk', 'title', 'description', 'state',
                  'url')

    def get_url(self, obj):
        """
        :return: the full url , ex: 127.0.0.1:8000/tasks/1/
        """
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())


class TaskModelSerializer(serializers.ModelSerializer):
    """
    Task Model Serializer
    """
    state_display = SerializerMethodField()
    linked_task_data = SerializerMethodField()
    outer_task = SerializerMethodField()

    class Meta:
        model = Task
        fields = ('pk', 'user', 'title', 'description', 'linked_task', 'state',
                  'state_display', 'linked_task_data', 'outer_task',)
        read_only_fields = ('user',)
        extra_kwargs = {"linked_task":
            {
                "write_only": True,
            }
        }

    def get_state_display(self, obj):
        """
        SHOW THE STATE STRING ("NEW", "PROGRESS", "DONE")
        """
        return obj.get_state_display()

    def get_linked_task_data(self, obj):
        """
        shoe the linked task in SimpleTaskModelSerializer
        """
        if obj.linked_task:
            return SimpleTaskModelSerializer(obj.linked_task,
                                             context={'request': self.context.get('request')}).data
        return None

    def get_outer_task(self, obj):
        """
        check if the task was linked from another one, then render this one in SimpleTaskModelSerializer
        """
        try:
            if obj.outer_task:
                return SimpleTaskModelSerializer(obj.outer_task,
                                                 context={'request': self.context.get('request')}).data
        except AttributeError:
            return None

    def update(self, instance, validated_data):
        """
        Handle errors for each state
        all cases :
        1- raise << invalid state change , can only NEW << PROGRESS << DONE
        2- raise << invalid linked_task update, editable only in progress task
        3- raise << invalid edit in progress task
        4- raise << invalid edit Done task
        :return: the same method (update) if passes all cases
        """
        title = validated_data.get('title')
        description = validated_data.get('description')
        state = validated_data.get('state', instance.state)
        linked_task = validated_data.get('linked_task')

        if state != instance.state and state - instance.state != 1:
            raise ValidationError("Invalid state change")
        elif linked_task and state != 2:
            raise ValidationError("unable to update linked task, only valid for Progress state")
        elif (instance.state != 1 and
              (title or description)):
            raise ValidationError("Unable to update state, only valid in NEW state")
        elif instance.state == 3:
            raise ValidationError("Done state is not editable")

        return super(TaskModelSerializer, self).update(instance, validated_data)
