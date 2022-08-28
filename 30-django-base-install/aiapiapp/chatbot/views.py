from distutils.log import error
import json
import uuid
from rest_framework.generics import ListAPIView, CreateAPIView
from aiapiapp.models import ChatUuid, ChatDialogue
from aiapiapp.chatbot.serializers import ChatUuidSerializer, ChatTextInputSerializer
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework import authentication, permissions

from chatbot import get_new_uuid, singlechat, train


class ChatUuidListAPIView(ListAPIView):
    model = ChatUuid
    serializer_class = ChatUuidSerializer
    queryset = ChatUuid.objects.all().order_by('-created')


class ChatUuidNewAPIView(CreateAPIView):
    model = ChatUuid
    serializer_class = ChatUuidSerializer
    queryset = ChatUuid.objects.all()

    def post(self, request, *args, **kwargs):
        request.data["chatuuid"] = get_new_uuid()

        if request.data["agreed"] != "Einverstanden":
            return Response(data="If 'agreed' is not 'Einverstanden' you can not use the services.",
                            status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)


class ChatInputAPIView(CreateAPIView):
    model = ChatDialogue
    serializer_class = ChatTextInputSerializer

    def post(self, request, *args, **kwargs):
        try:
            textinput = str(request.data["input"])
            if type(textinput) is not str and\
                    len(textinput) < 1:
                raise error

            chatuuid = uuid.UUID(request.data["chatuuid"])
            if type(chatuuid) is not uuid.UUID and\
                    len(chatuuid) != 36:
                raise error

        except:
            return Response(data="Please provide a valid UUID for the conversation and a input text to answer to.",
                            status=status.HTTP_400_BAD_REQUEST)

        answer = json.loads(singlechat(chatuuid, textinput))

        request.data["probability"] = float(answer["probability"])
        request.data["understood"] = bool(answer["understood"])
        request.data["output"] = str(answer["output"])

        return self.create(request, *args, **kwargs)


class ChatTrainAPIView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Returns the console output from the training process.
        Only Admin Users can start the training.
        """
        trainoutput = train()
        
        return Response(data=str(trainoutput), status=status.HTTP_200_OK)
