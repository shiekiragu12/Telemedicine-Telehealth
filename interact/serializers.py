from rest_framework import serializers
from account.serializers import UserSerializer
from .models import ChatMessage, ChatFile


class ChatFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatFile
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    created_on = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'appointment', 'sender', 'text', 'files', 'created_on']

        extra_kwargs = {
            "files": {
                "required": False
            }
        }

    def to_representation(self, instance):
        self.fields['sender'] = UserSerializer(many=False)
        self.fields['files'] = ChatFileSerializer(many=True)
        return super(ChatMessageSerializer, self).to_representation(instance)

    def get_created_on(self, obj):
        return obj.created_on.strftime("%b %Y %d | %I:%M%p")

    def create(self, validated_data, *args, **kwargs):
        files = self.initial_data.getlist('files_')

        files_arr = []
        if len(files) > 0 and files:
            for file_ in files:
                if not isinstance(file_, str):
                    file__ = ChatFile.objects.create(file=file_, file_type=file_.content_type)
                    files_arr.append(file__)
        files_ = [file.id for file in files_arr]
        validated_data['files'] = files_

        return super().create(validated_data, *args, **kwargs)

