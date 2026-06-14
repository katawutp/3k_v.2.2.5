from django import template
from ..models import Follow
from django.contrib.auth.models import AnonymousUser

register = template.Library()

@register.simple_tag
def is_following(user, this_user):
    """Safe template tag to check if user follows this_user"""
    # Handle AnonymousUser and unauthenticated
    if not user or not user.is_authenticated:
        return False
    
    # Handle SimpleLazyObject for follower (Django's lazy evaluation)
    if hasattr(user, '_wrapped'):
        user = user._wrapped
    
    # Handle SimpleLazyObject for the user being followed
    if hasattr(this_user, '_wrapped'):
        this_user = this_user._wrapped
    
    # Final safety check
    if not user.pk or isinstance(user, AnonymousUser):
        return False
    
    # Query the database
    return Follow.objects.filter(follower=user, following=this_user).exists()