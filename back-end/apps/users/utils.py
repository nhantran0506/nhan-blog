import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_tokens(user):
    access_token_payload = {
        'user_id': str(user.user_id),
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'iat': datetime.utcnow()
    }
    
    refresh_token_payload = {
        'user_id': str(user.user_id),
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')
    
    return access_token, refresh_token 