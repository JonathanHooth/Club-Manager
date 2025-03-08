"""
Serializers for the user API View
"""

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _  # convention import name
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from clubs.models import Club
from core.abstracts.serializers import ModelSerializerBase


class UserClubNestedSerializer(serializers.ModelSerializer):
    """Represents nested club info for users."""

    id = serializers.IntegerField(source="club.id", read_only=True)
    name = serializers.CharField(source="club.name", read_only=True)
    # TODO: Add role, permissions

    class Meta:
        model = Club
        fields = [
            "id",
            "name",
        ]


class UserSerializer(ModelSerializerBase):
    """Serialzier for the user object."""

    email = serializers.EmailField()
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    clubs = UserClubNestedSerializer(
        source="club_memberships", many=True, required=False
    )

    class Meta:
        model = get_user_model()
        fields = [
            *ModelSerializerBase.default_fields,
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "clubs",
        ]
        # defines characteristics of specific fields
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    # override default create method to call custom create_user method
    def create(self, validated_data):
        """Cteate and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):  # override update method
        """Update and return user"""
        # instance: model instance being updated

        password = validated_data.pop(
            "password", None
        )  # get password from data, remove from dict. optional field
        user = super().update(instance, validated_data)  # users base update method

        if password:
            user.set_password(password)
            user.save()

        return user


# just base off normal serializer, no need for model serializer methods
class AuthTokenSerializer(serializers.Serializer):
    """Serialzer for the user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        # ensure text is hidden in browsable api
        style={"input_type": "password"},
        trim_whitespace=False,  # ensure doesn't trim, in case it's deliberate
    )

    # called at validation stage by views when data posted to view
    def validate(self, attrs):  # attrs: attributes
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),  # pass request context
            username=email,
            password=password,
        )  # returns user if user found
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(
                msg, code="authorization"
            )  # returns bad request
        attrs["user"] = user  # add user info to attributes, pass it back
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    """Display user token in API."""

    token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("token",)
