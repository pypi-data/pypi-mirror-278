from calendar import timegm
from datetime import datetime, timezone

import jwt
from django.contrib.auth import get_user_model

from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings


def jwt_get_secret_key(payload=None):
    """
    For enhanced security you may want to use a secret key based on user.

    This way you have an option to logout only this user if:
        - token is compromised
        - password is changed
        - etc.
    """
    if api_settings.JWT_GET_USER_SECRET_KEY:
        User = get_user_model()  # noqa: N806
        if api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER:
            username = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(payload)
        else:
            username_field = get_username_field()
            username = payload.get(username_field)
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            raise jwt.InvalidTokenError()
        else:
            return str(api_settings.JWT_GET_USER_SECRET_KEY(user))
    return api_settings.JWT_SECRET_KEY


def jwt_payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)

    payload = {
        "username": username,
        "exp": timegm(
            (
                datetime.now(timezone.utc) + api_settings.JWT_EXPIRATION_DELTA
            ).utctimetuple()
        ),
    }

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload["orig_iat"] = timegm(datetime.now(timezone.utc).utctimetuple())

    if api_settings.JWT_AUDIENCE is not None:
        payload["aud"] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload["iss"] = api_settings.JWT_ISSUER

    return payload


def jwt_get_username_from_payload_handler(payload):
    """
    Override this function if username is formatted differently in payload
    """
    return payload.get("username")


def jwt_encode_handler(payload):
    key = api_settings.JWT_PRIVATE_KEY or jwt_get_secret_key(payload)
    return jwt.encode(payload, key, api_settings.JWT_ALGORITHM)


def jwt_decode_handler(token):
    options = {
        "verify_exp": api_settings.JWT_VERIFY_EXPIRATION,
        "verify_signature": api_settings.JWT_VERIFY,
    }
    # get user from token, BEFORE verification, to get user secret key
    unverified_payload = jwt.decode(token, None, options={"verify_signature": False})
    secret_key = jwt_get_secret_key(unverified_payload)
    return jwt.decode(
        token,
        api_settings.JWT_PUBLIC_KEY or secret_key,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithms=[api_settings.JWT_ALGORITHM],
    )


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    return {"token": token}
