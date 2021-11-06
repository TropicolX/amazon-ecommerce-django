from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import UserProfile

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.db.utils import IntegrityError

# Create your views here.


class Register(APIView):
    ''' For registering a user '''

    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            password = request.data['password']

            validate_password(password=password)

            user = UserProfile.objects.create_user(
                email=email, first_name=first_name, last_name=last_name, password=password)

            refresh = RefreshToken.for_user(user)

            return Response(data={'detail': 'User created successfully', 'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}}, status=status.HTTP_201_CREATED)

        except KeyError:
            raise ParseError(data={
                             "detail": "Provide a valid email, first_name, last_name, and password"}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            raise ParseError(data={'detail': " ".join(e)},
                             status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': "A user with this email already exists"})

        except Exception as ex:
            raise serializers.ValidationError(
                {'detail': "Can't complete this request. Ensure the data posted is in the correct format."})


class Login(APIView):
    ''' For logging in a user.'''

    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            password = request.data['password']
            user = UserProfile.objects.get(email=email)
            if not check_password(password, user.password):
                return Response(data={"detail": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)

            return Response(data={'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}}, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            raise NotFound({"detail": "Email not found"})

        except KeyError:
            raise ParseError({"detail": "Provide 'email' and 'password'"})

        except Exception as ex:
            raise serializers.ValidationError(
                {'detail': "Can't complete this request. Ensure the data posted is in the correct format."})


class BlacklistTokenView(APIView):
    '''Blacklist a user's refresh token'''

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(data={'detail': "Token blacklisted successfully"}, status=status.HTTP_200_OK)

        except KeyError:
            raise ParseError({"detail": "Provide a refresh token"})


class ChangePassword(APIView):
    """ For Changing user password """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            current_password = request.data['current_password']
            new_password = request.data['new_password']

            if not check_password(current_password, user.password):
                return Response(data={"detail": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

            validate_password(new_password)
            user.set_password(new_password)
            user.save()

            return Response({'detail': 'User password updated successfully'})

        except KeyError:
            raise ParseError({"detail": "Provide a valid password"})

        except ValidationError as e:
            raise ParseError({'detail': " ".join(e)})

        except Exception as ex:
            raise ParseError(
                {'detail': "Can't complete this request. Ensure the data posted is in the correct format."})
