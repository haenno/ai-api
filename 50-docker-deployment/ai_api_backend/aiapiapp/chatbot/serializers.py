from rest_framework import serializers
from aiapiapp.models import ChatUuid, ChatDialogue


class ChatUuidSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUuid
        fields = '__all__'


class ChatTextInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatDialogue
        fields = '__all__'
