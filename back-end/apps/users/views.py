from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserSignupSerializer
from .utils import generate_tokens
from .model import User
import jwt
from django.conf import settings
from apps.core.permissions import admin_or_user_required, user_required

@api_view(['POST'])
@permission_classes([AllowAny])
async def signup(request):
    """
    Create a new user account.
    
    Parameters:
    - username (string): required
    - email (string): required
    - password (string): required
    - birth_date (date): optional
    
    Returns:
    - user: User object
    - access_token: JWT access token
    - refresh_token: JWT refresh token
    """
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        access_token, refresh_token = generate_tokens(user)
        
        user.refresh_token = refresh_token
        await user.save()
        
        return Response({
            'user': UserSerializer(user).data,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
async def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    access_token, refresh_token = generate_tokens(user)
    
    user.refresh_token = refresh_token
    await user.save()
    
    return Response({
        'user': UserSerializer(user).data,
        'access_token': access_token,
        'refresh_token': refresh_token
    })

@api_view(['POST'])
@permission_classes([AllowAny])
async def refresh_token(request):
    refresh_token = request.data.get('refresh_token')
    
    if not refresh_token:
        return Response({
            'error': 'Refresh token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        user = await User.objects.get(user_id=payload['user_id'])
        
        if user.refresh_token != refresh_token:
            return Response({
                'error': 'Invalid refresh token'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        access_token, new_refresh_token = generate_tokens(user)
        
        user.refresh_token = new_refresh_token
        await user.save()
        
        return Response({
            'access_token': access_token,
            'refresh_token': new_refresh_token
        })
    except jwt.ExpiredSignatureError:
        return Response({
            'error': 'Refresh token has expired'
        }, status=status.HTTP_401_UNAUTHORIZED)
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response({
            'error': 'Invalid refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@user_required
async def logout(request):
    try:
        user = await User.objects.get(user_id=request.user_id)
        user.refresh_token = None
        await user.save()
        return Response({'message': 'Successfully logged out'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)