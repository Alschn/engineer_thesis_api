from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


def get_tokens_for_user(user: User) -> tuple[str, str]:
    """
    Returns access and refresh token pair.
    access, refresh = get_tokens_for_user(user)
    """
    refresh = get_token_for_user(user)
    return str(refresh.access_token), str(refresh)


def get_token_for_user(user: User) -> RefreshToken:
    return RefreshToken.for_user(user)
