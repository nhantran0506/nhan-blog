import jwt
from django.conf import settings
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from functools import wraps
from apps.users.model import User, UserRole

def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

async def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, JsonResponse({'error': 'No token provided'}, status=401)
    
    try:
        token = auth_header.split(' ')[1]
        payload = await sync_to_async(verify_token)(token)
        
        if payload is None:
            return None, JsonResponse({'error': 'Invalid token'}, status=401)
        
        user = await User.objects.get(user_id=payload.get('user_id'))
        return user, None
    except (IndexError, User.DoesNotExist):
        return None, JsonResponse({'error': 'Invalid token or user'}, status=401)

def admin_required(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        user, error_response = await get_user_from_token(request)
        if error_response:
            return error_response
            
        if user.role != UserRole.ADMIN.name:
            return JsonResponse({'error': 'Admin access required'}, status=403)
        
        request.user = user
        return await func(request, *args, **kwargs)
    return wrapper

def user_required(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        user, error_response = await get_user_from_token(request)
        if error_response:
            return error_response
        
        request.user = user
        return await func(request, *args, **kwargs)
    return wrapper

def admin_or_user_required(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        user, error_response = await get_user_from_token(request)
        if error_response:
            return error_response
        
        if user.role not in [UserRole.ADMIN.name, UserRole.USER.name]:
            return JsonResponse({'error': 'Access denied'}, status=403)
            
        request.user = user
        return await func(request, *args, **kwargs)
    return wrapper
        