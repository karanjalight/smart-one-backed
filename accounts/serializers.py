from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .models import CustomUser as User
from .utils import *
import random
import string
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives



class HelloView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello World!'}
        return Response(content)
    


def assign_user_to_admin_group(user):
    try:
        admin_group = Group.objects.get(name="Admin")
    except Group.DoesNotExist:
        # If the "Admin" group doesn't exist, create it
        admin_group = Group.objects.create(name="Admin")
        # Assign all permissions to the "Admin" group
        permissions = Permission.objects.all()
        admin_group.permissions.set(permissions)

    # Add the user to the "Admin" group
    user.groups.add(admin_group)


def generate_verification_code():
    # Generate a random 6-digit verification code
    return ''.join(random.choices(string.digits, k=6))


class UserSerializer(serializers.ModelSerializer):
    # date_joined = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    # restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), required=False)
    # restaurant_name = serializers.CharField(write_only=True, required=False)
    # last_login = serializers.CharField(read_only=True)
    verification_code = serializers.CharField(max_length=6, read_only=True)
    # role = serializers.SerializerMethodField()
    # profile_pic = serializers.SerializerMethodField()
    # title = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id", "email", "username", "name", "phone_number", "slug", "is_restaurant", "is_customer", "is_staff", "is_driver",
             'password',  'restaurant_name',   'verification_code'
        )
        extra_kwargs = {'password': {'write_only': True}}

    # def get_profile_pic_url(self, obj):
    #     if obj.profile_pic:
    #         return self.context['request'].build_absolute_uri(obj.profile_pic.url)
    #     return None

    # def get_role(self, obj):
    #     if obj.groups.exists():
    #         return obj.groups.first().name
    #     return None

    def create(self, validated_data):
        if validated_data['is_restaurant']:
            user = User(
                email=validated_data['email'],
                name=validated_data['name'].title(),
                is_restaurant=validated_data['is_restaurant'],
                is_customer=validated_data['is_customer'],
                phone_number=validated_data['phone_number'],
                is_active=True,
                is_driver=False
                # role = validated_data['role'],
                # title = validated_data['title']
            )
        else:
            user = User(
                email=validated_data['email'],
                name=validated_data['name'],
                is_restaurant=False,
                phone_number=validated_data['phone_number'],
                is_customer=False,
                is_driver=True,
                # restaurant = validated_data['restaurant']
            )
        user.set_password(validated_data['password'])
        # Generate the verification code and hash it
        verification_code = generate_verification_code()
        user.verification_code = verification_code        
        user.save()
        
        create_default_groups()
        assign_user_to_admin_group(user)

        if validated_data['is_restaurant']:
            c = Restaurant.objects.create(name=validated_data['restaurant_name'])
            user.restaurant = c
            user.save()

        code = verification_code

        
        # Email Functionality
        html_message = render_to_string("emails/verifyrestaurant.html",  {"code": code, "user":user.name})
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject='Verify Restaurant',
            body= plain_message,
            from_email="itisha Restaurant <settings.EMAIL_HOST_USER>",
            to= [user.email]
        )

        message.attach_alternative(html_message, 'text/html')
        message.send()
        #send activation email
        # send_verification_email(user.email, verification_code)

        return user
    



