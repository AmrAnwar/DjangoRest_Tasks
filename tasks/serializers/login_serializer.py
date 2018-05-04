from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.serializers import (
    CharField,
    EmailField,
    ValidationError,
)


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for Login
    user can login using his (Username or Email) and the password
    """
    username = CharField(required=False, allow_blank=True)
    email = EmailField(label='Email Address', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {"password":
            {
                "write_only": True,
            }
        }

    def validate(self, data):
        """
        check user data
        :param data:
        :return: 4 cases -:
            1- if not email or username, ValidationError("A username or email is required to login")
            2- if user doesn't exist, ValidationError("This username/email is not valid")
            3- check password failed, ValidationError("Incorrect credentials please try again")
            4- if all pass, return entered data again
        """
        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password", None)
        if not email and not username:
            raise ValidationError("A username or email is required to login")
        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again")
        data['username'] = user_obj.username
        data['email'] = user_obj.email
        return data
