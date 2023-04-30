from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from rest_framework_simplejwt.tokens import RefreshToken
from .validators import letter_validator, number_validator, special_char_validator


class RegisterInputSerializer(serializers.Serializer):
    # first_name = serializers.CharField(max_length=100)
    # last_name = serializers.CharField(max_length=100)
    # email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(validators=[
        MinLengthValidator(limit_value=8),
        # letter_validator,
        # number_validator,
        # special_char_validator,
    ])
    confirm_password = serializers.CharField(max_length=100)

    def validate_username(self, username):
        if get_user_model().objects.filter(username=username).exists():
            raise serializers.ValidationError('username taken already')
        return username

    # def validate_email(self, email):
    #     if get_user_model().objects.filter(email=email).exists():
    #         raise serializers.ValidationError('email taken already')
    #     return email

    def validate(self, data):
        if not data.get('password') and not data.get('confirm_password'):
            raise serializers.ValidationError('please fill password and confirm password')
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('password and confirm password doesnt match')
        return data


class RegisterOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')



