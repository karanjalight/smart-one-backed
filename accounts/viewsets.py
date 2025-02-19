from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status
from .utils import get_tokens_for_user
import json



class RegisterUserViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    """
    A simple ViewSet registering users.
    """

    def create(self, request, *args, **kwargs):
        picture = request.data.get('picture', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        return user
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

# class VerifyEmail(generics.GenericAPIView):
#     permission_classes = [AllowAny, ]

#     def post(self, request):
#         data = json.loads(request.body)
#         token = data['token']
#         uid = data['uid']
#         user = None
#         print('TOKEN', token)
#         print('UID', uid)
#         try:
#             if token is not None and uid is not None:
#                 uid = force_str(urlsafe_base64_decode(uid))
#                 user = User.objects.get(pk=uid)
#         # except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         except Exception as e:
#             user = None
#             print('USER DOES NOT EXIST', str(e))
            
#         if user is not None:
#             try:
#                 if user.is_active == False:
#                     if account_activation_token.check_token(user, token):
#                         user.is_active = True
#                         user.email_verified = True
#                         user.save()
#                         return Response({'success': 'Successfully activated'}, status=status.HTTP_200_OK)
#                     else:
#                         return Response({'invalid': 'Invalid token'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#                 else:
#                     return Response({'already': 'already activated'}, status=status.HTTP_226_IM_USED)
#             except Exception as e:
#                 print('TOKEN ERROR', str(e))
#                 return Response({'error': 'Invalid token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         # Return a response indicating that the user does not exist
#         return Response({'no_user': 'User does not exist'}, status=status.HTTP_200_OK)