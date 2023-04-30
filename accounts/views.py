from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterInputSerializer, RegisterOutputSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

CustomUser = get_user_model()


class RegisterView(APIView):

    @extend_schema(request=RegisterInputSerializer, responses=RegisterOutputSerializer)
    def post(self, request):
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = CustomUser.objects.create_user(username=data['username'], password=data['password'])
        context = {'request': request}
        return Response(RegisterOutputSerializer(user, context).data, status=status.HTTP_201_CREATED)
