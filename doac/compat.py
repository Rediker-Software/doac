import random

try:
    random = random.SystemRandom()
except NotImplementedError:
    pass


def get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                               '0123456789'):
    return ''.join([random.choice(allowed_chars) for i in range(length)])


def get_user_model():
    """
    Get the user model that is being used.  If the `get_user_model` method
    is not available, default back to the standard User model provided
    through `django.contrib.auth`.
    """

    try:
        from django.contrib.auth import get_user_model
        
        return get_user_model()
    except ImportError:
        from django.contrib.auth.models import User
        
        return User

try:
    from django.utils import timezone
    
    now = timezone.now
except ImportError:
    from datetime import datetime
    
    now = datetime.now
