from django import template

register = template.Library()

@register.filter
def get_avatar(avatar_map, username):
    """
    Custom template filter to get avatar URL for a username from the avatar_map.
    Usage: {{ avatar_map|get_avatar:comment.author }}
    """
    if not avatar_map or not username:
        return ''
    return avatar_map.get(username, '')
