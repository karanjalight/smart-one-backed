from django.contrib.auth.models import Permission, Group

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



def create_default_groups():
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    editor_group, _ = Group.objects.get_or_create(name="Editor")

    # Assign necessary permissions admin group
    admin_permissions = Permission.objects.all()
    admin_group.permissions.set(admin_permissions)

    #Assign editor permissions as needed
    editor_permissions = Permission.objects.all()
    editor_group.permissions.set(editor_permissions)



class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = get_user_model().objects.get(email=request.data['email'])
            # update_last_login(None, user)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except TokenError as e:
            raise InvalidToken(e.args[0])