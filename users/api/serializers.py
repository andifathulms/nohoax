from rest_framework import serializers
from django.db import transaction
from users.models import user as User

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['name', 'email', 'nohp', 'password','confirm_password']
        extra_kwargs = {
            'password': {'write_only' : True}
        }

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self):
        user = User(
                email=self.validated_data['email'],
                name=self.validated_data['name'],
                nohp=self.validated_data['nohp'],
            )
        pwd = self.validated_data['password']
        pwd2 = self.validated_data['confirm_password']

        if pwd != pwd2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(pwd)
        user.save()
        return user

class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()