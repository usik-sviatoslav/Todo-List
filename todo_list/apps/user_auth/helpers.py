from rest_framework_simplejwt.tokens import RefreshToken


def get_token_pair(user):
    token_pair = RefreshToken.for_user(user)
    return {
        "refresh": str(token_pair),
        "access": str(token_pair.access_token),  # type: ignore
    }
