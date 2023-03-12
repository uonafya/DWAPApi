from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import re
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage
import threading
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('groups', 'first_name', 'last_name',
                  'username', 'email', 'phone', 'password')

    def test_thread(selft):
        print("sending email...")

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            username=validated_data['username'])
        selectedroles = validated_data['groups']
        user.set_password(validated_data['password'])
        user.is_staff = False
        user.save()
        if selectedroles:
            roles = Group.objects.filter(name__in=selectedroles)
            for role in roles:
                user.groups.add(role)
            user.save()
        # Send confirmation email
        config = EmailConfig.objects.first()
        print(config)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        subject = 'Confirm your registration'
        message = render_to_string('authmanagement/confirm_email.html', {
            'user': user,
            'uid': uid,
            'token': token,
        })
        try:
            print(config.email_password)
            print(user.email)
            backend = EmailBackend(host=config.email_host, port=config.email_port, username=config.from_email,
                                   password=config.email_password, use_tls=config.use_tls, fail_silently=config.fail_silently)
            myemail = EmailMessage(subject=subject, body=message,
                                   from_email=config.from_email, to=[user.email,], connection=backend)
            # schedule in a thread
            email_thread = threading.Thread(target=myemail.send)
            print("Starting email thread..")
            email_thread.start()
            print("Email sent!")
        except Exception as e:
            print("send mail error:{}".format(e))
        Token.objects.create(user=user)
        return user
