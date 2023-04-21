import jwt
from datetime import datetime, timedelta

from ai_planet_assignment.settings import JwtConstants
from django.conf import settings

from users.models import User

class EncryptionHelper:
    # Encryption helper function for access token generation

    def __init__(self, user_id):
        self.user_id = user_id
        self.user = User.objects.get(user_id=self.user_id)
        self.token_secret = JwtConstants.TOKEN_SECRET
        self.algorithm = JwtConstants.JWT_ALGORITHM
        self.seconds = int(JwtConstants.JWT_EXP_DELTA_SECONDS)

    def create_access_token(self):
        try:
            payload = {
                "user_id": self.user_id.hex,
                "exp": datetime.utcnow() + timedelta(seconds=self.seconds),
            }

            access_token = jwt.encode(
                payload, self.token_secret, algorithm=self.algorithm
            )
            return access_token.decode("utf-8")
        except Exception as e:
            raise e