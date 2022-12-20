from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import EmailCodes, User
from .permissions import IsAnonymous
from .serializers import SendCodeSerializer, RegistrationSerializer


class SendCodeAPIView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (IsAnonymous,)
    serializer_class = SendCodeSerializer
    queryset = EmailCodes.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        print(serializer.is_valid())
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.data)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegistrationAPIView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (IsAnonymous,)
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        username = data.get("username")
        email_modal = EmailCodes.objects.get(username=username)
        email = email_modal.email
        code = email_modal.code
        if str(code) == data.get("confirmation_code"):
            data = {"username": username, "email": email}
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Не верный код", status=status.HTTP_400_BAD_REQUEST)
