from rest_framework.serializers import ModelSerializer

from .models import AppConfig, Contact, Blog, Reply, Topic


class AppConfigSerializer(ModelSerializer):
    class Meta:
        model = AppConfig
        fields = '__all__'


class ContactSerializer(ModelSerializer):

    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email', 'subject', 'message', 'read']

        extra_kwargs = {
            'name': {
                'required': False,
            },
            'phone_number': {
                'required': False,
            },
            'email': {
                'required': False,
            },
            'subject': {
                'required': False,
            },
            'message': {
                'required': False,
            },
        }


class TopicsSerializer(ModelSerializer):

    class Meta:
        model = Topic
        fields = '__all__'


class BlogSerializer(ModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'


class ReplySerializer(ModelSerializer):

    class Meta:
        model = Reply
        fields = '__all__'
