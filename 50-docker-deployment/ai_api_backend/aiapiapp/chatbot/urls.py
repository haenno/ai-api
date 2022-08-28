from django.urls import path
from aiapiapp.chatbot.views import ChatUuidNewAPIView, ChatUuidListAPIView, ChatInputAPIView, ChatTrainAPIView

app_name = 'aiapiapp'

urlpatterns = [
    path('listchatuuids/', ChatUuidListAPIView.as_view(), name='listchatuuids'),
    path('newchatuuid/', ChatUuidNewAPIView.as_view(), name='newchatuuid'),
    path('input/', ChatInputAPIView.as_view(), name='input'),
    path('train/', ChatTrainAPIView.as_view(), name='train'),
]
