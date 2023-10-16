from rest_framework import serializers
from django.contrib.auth.models import User
# from rest_framework.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2',]
        extra_kwargs = {'password': {'write_only': True}}

    # Override save() method
    def save(self):
        # print(self.validated_data)
        # >> OrderedDict([('username', 'user1'), ('email', '@gmail.com'), ('password', '1234'), ('password2', '123')])

        # Check if password == password2
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'error': 'p1 and p2 must be the same'})

        # Check if email is already existed
        email = self.validated_data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists'})

        # Create User model instance
        new_user_account = User(
            username=self.validated_data['username'], email=email)
        new_user_account.set_password(password)
        new_user_account.save()

        return new_user_account
