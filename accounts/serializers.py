from rest_framework import serializers
from .models import User, Profile, Phone, Address
from rest_framework.authtoken.models import Token


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = [
            'id',
            'profile',
            'ddi',
            'ddd',
            'number',
        ]

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            'id',
            'profile',
            'postalcode',
            'street_name',
            'street_number',
            'complement',
            'neighborhood',
            'city',
            'state',
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_staff',
            'is_active',
            'is_trusty',
            'date_joined',
            'url',
        ]
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)
    phone = PhoneSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'cpf',
            'rg',
            'birthday',
            'civil_status',
            'phone',
            'address',
        ]
