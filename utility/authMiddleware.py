from users.models import User
import jwt
from rest_framework import status
from ai_planet_assignment.settings import JwtConstants
from rest_framework.response import Response
import uuid
import sentry_sdk

def is_authenticated(function):
    def wrap(request, *args, **kwargs):
        try:
            # print(f"HTTP_USER_AGENT - {request.META['HTTP_USER_AGENT']}")
            token = request.headers["Authorization"]
            # Decode payload
            payload = jwt.decode(
                token,
                JwtConstants.TOKEN_SECRET,
                algorithms=JwtConstants.JWT_ALGORITHM,
            )
            request.user_id = uuid.UUID(payload["user_id"])
            # Will raise 401 error if user does not exist
            request.user = User.objects.get(user_id=request.user_id)

            if not User.objects.filter(user_id = request.user_id).exists():
                return Response({"error": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            # Token is valid pass the request
            try:
                response = function(request, *args, **kwargs)
                response_code = getattr(response, "status_code", None)
                if response_code >= 400:
                    with sentry_sdk.push_scope() as scope:
                        scope.user = {"user_id": str(request.user.user_id)}
                        sentry_sdk.capture_exception(
                            Exception(str(getattr(response, "data", None)))
                        )

                return response
            except Exception as e:
                with sentry_sdk.push_scope() as scope:
                    scope.user = {"user_id": str(request.user.user_id)}
                    sentry_sdk.capture_exception(e)
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            return Response(
                {"error": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    return wrap