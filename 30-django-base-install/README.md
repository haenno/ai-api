# django-base-install

The contents of this folder are based on my own notes <https://github.com/haenno/public-krams/blob/main/django-rest-notes.md> and the experience I made while developing a browser RPG adventure for a previous exam <https://github.com/tstsrv-de/rpg>.

## Useage

This folder provides a ready to use installation of Django with the AI-Application allready included. You can also make your own, clean install with the steps described in the next part. But if you just want to test it, take these steps:

1. Install Python and Pipenv.
2. Install depencys with ``pipenv install``.
3. Take the following steps to initialize and start Django:

    ```bash
    pipenv run python manage.py makemigrations
    pipenv run python manage.py migrate --run-syncdb    
    pipenv run python manage.py createsuperuser
    pipenv run python manage.py collectstatic --noinput 
    pipenv run python -m chatbot -t
    pipenv run daphne -b 0.0.0.0 -p 8000 aiapiproject.asgi:application
    ```

4. Open the backend on <http://127.0.0.1:8000>.




## The installation process

1. Install Python and Pipenv.
2. Create a ``Pipfile`` in the main folder with the following contents:

    ```toml
    [[source]]
    url = "https://pypi.org/simple"
    verify_ssl = true
    name = "pypi"

    [packages]

    Django = "==4.1" # Django itself 
    djangorestframework = "==3.13.1" # Django toolkit for rest api
    drf-yasg = "==1.21.3" # Swagger for Django / OpenAPI 2.0 fits perfectly
    django-cors-headers = "==3.13.0" # for cross site access from a frontend
    daphne = "==3.0.2" # to serve django 
    whitenoise = "==6.2.0" # to serve static files
    tzdata = "==2022.2" # to fix depency error on some systems

    # for the chatbot module
    numpy = "==1.23.2" 
    nltk = "==3.7"
    HanTa = "==0.2.0" # 0.2.1 does not work well at this time, fallback to 0.2.0
    torch = "==1.12.1"

    [dev-packages]

    [requires]
    python_version = "3"

    ```

3. Then install the packeages with runnig ``pipenv install``.

4. Create the Django project with the command ``pipenv run django-admin startproject aiapiproject .`` in the same folder.

5. Next create the Django app with ``pipenv run django-admin startapp aiapiapp``.

6. Add and/or change lines in the `settings.py` in porject folder `aiapiproject`:

    ```python
    import os # for staticfiles

    # fill the list
    ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

    # add the lines on the bottom to the list
    INSTALLED_APPS = [
        ...
        'aiapiapp', # the ai-app itself
        'rest_framework', # Django toolkit for a rest api
        'drf_yasg', # Swagger for Django / OpenAPI 2.0 will do just fine
        'corsheaders', # for configure acces from a frontend
    ]


    # Pay attention to the order:
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware', # add cors as the first line
        ...
        'django.middleware.security.SecurityMiddleware', # look out for this line and insert whitenoise below
        'whitenoise.middleware.WhiteNoiseMiddleware', # for static files
        ...

    # add the following to the bottom of the file

    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly', # for later use
            'rest_framework.permissions.AllowAny',
        ]
    }

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # for staticfiles

    CORS_ORIGIN_ALLOW_ALL=True

    # for later use
    # CORS_ORIGIN_WHITELIST = [
    #     'http://localhost:8000',
    #     'http://127.0.0.1:8000'
    # ]

    ```

7. Add and/or change lines in the `urls.py` also in the porject folder `aiapiproject`:

    ```python
    from django.urls import include, re_path
    from django.http import HttpResponse # for index page

    # for swagger: start
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    schema_view = get_schema_view(
        openapi.Info(
            title="AI-API",
            default_version='v1',
            description="A webservice for access to a AI-Application.",
            terms_of_service="https://github.com/haenno/ai-api",
            contact=openapi.Contact(email="haenno@web.de"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    # for swagger: end

    urlpatterns = [
        path('', lambda request: HttpResponse('<html><body><p><h1>This is the backend of an \
            AI-API-Application</h1><b>Proceed to</b>         <a href="doc/">doc</a>, \
            <a href="redoc/">redoc</a>, <a href="spec.json">spec.json</a>         \
            or <a href="spec.yaml">spec.yaml</a> for more details to this API.<br>\
            <br>Check <a href="https://github.com/haenno/ai-api">github.com/haenno/ai-api</a>\
            for the project documentation.</p></body></html>'), name='index'),  # for index page
        path('admin/', admin.site.urls),
        re_path(r'^spec(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0), name='schema-json'),  # for swagger
        path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),  # for swagger
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),  # for swagger
        path('api/v1/', include('aiapiapp.chatbot.urls')),
    ]

    ```

8. Create a folder ``staticfiles`` in the base directory (same as the file manage.py).

9. Create an API endpoint that creates and gives us a UUID. First, create a new folder in the APP directory `aiapiapp\chatbot\`.

10. Then create new files in that folder:
    1. A empty `__init__.py`.
    2. A file `serializers.py` with:

        ```python
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
        ```

    3. A file `urls.py` with:

        ```python
        from django.urls import path
        from aiapiapp.chatbot.views import ChatUuidNewAPIView, ChatUuidListAPIView, ChatInputAPIView, ChatTrainAPIView

        app_name = 'aiapiapp'

        urlpatterns = [
            path('listchatuuids/', ChatUuidListAPIView.as_view(), name='listchatuuids'),
            path('newchatuuid/', ChatUuidNewAPIView.as_view(), name='newchatuuid'),
            path('input/', ChatInputAPIView.as_view(), name='input'),
            path('train/', ChatTrainAPIView.as_view(), name='train'),
        ]

        ```

    4. A file `views.py` with:

        ```python
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


        ```

11. Then some changes in the files in the APP directory ``aiapiapp``:
    1. In the `admin.py` add:

        ```python
        from aiapiapp.models import ChatUuid, ChatDialogue
        admin.site.register(ChatUuid)
        admin.site.register(ChatDialogue)

        ```

    2. In the `models.py` add:

        ```python
        import uuid
        class ChatUuid(models.Model):
            chatuuid = models.UUIDField(unique=True, default=uuid.uuid4,
                                        editable=False, help_text="The UUID for a Chatbot conversation.")
            created = models.DateTimeField(auto_now_add=True)
            agreed = models.TextField(
                blank=True, help_text="If user agreed to the service terms (http://...), send 'Einverstanden'.")

            def __str__(self):
                return str(self.chatuuid)


        class ChatDialogue(models.Model):
            chatuuid = models.UUIDField(blank=False)
            created_at = models.DateTimeField(auto_now_add=True)
            updated_at = models.DateTimeField(auto_now=True)
            input = models.TextField(blank=False)
            probability = models.FloatField(blank=True)
            understood = models.BooleanField(blank=True)
            output = models.TextField(blank=True)

            def __str__(self):
                return str(self.input)
        ```

12. Then copy over the chatbot AI-Application module folder. Here it was the contents of ``chatbot``-Folder in ``20-prepared-ai-app``. Copy it in the folder, that contains the ``manage.py``-File.

13. Then initialize Django with the following coammnds. Note the superuser credentials! 

    ```bash
    pipenv run python manage.py makemigrations
    pipenv run python manage.py migrate
    pipenv run python manage.py createsuperuser
    pipenv run python manage.py collectstatic --noinput 
    pipenv run python -m chatbot -t
    ```

14. The finally start Django by running ``pipenv run daphne -b 0.0.0.0 -p 8000 aiapiproject.asgi:application`` and open <http://127.0.0.1:8000>.

## License

MIT License: Copyright (c) 2022 Henning 'haenno' Beier, haenno@web.de, <https://github.com/haenno/ai-api>
