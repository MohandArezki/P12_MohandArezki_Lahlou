import jwt
from datetime import datetime, timedelta
from controllers.database import DBManager

class AuthManager:
    """
    Class for managing authentication using JWT tokens.
    """

    secret_key = 'ljklòasd89ew654@@XOPljklsd874_w654=)$£!;ç'
    refresh_secret_key = '874_w65ljklòasd=sd89e)$£!;çòas' 

    @classmethod
    def validate_token(cls):
        """
        Validate the JWT token.

        Raises:
            Exception: If no connection is detected or if the token is invalid or missing.
        """
        access_token = DBManager.headers.get("access_token")
        refresh_token = DBManager.headers.get('refresh_token')

        if not access_token:
            response, msg = False, "No connection detected. Please log in first. Type <help login> for more details"
        elif not cls.verify_token(access_token):
            new_access_token = cls.refresh_token(refresh_token)
            if new_access_token:
                DBManager.headers['access_token'] = f'Bearer {new_access_token}'
                response, msg = True, "Token checked. Refreshed."
            else:
                response, msg = False, "Invalid or missing token. Access denied."
        else:
            response, msg = True, "Token checked. Still valid."
        print(msg)
        if not response:
            DBManager.reset_data()  
 
        return response

    @classmethod
    def generate_tokens(cls, user_id, expiration_minutes=30, refresh_expiration_days=1):
        """
        Generate both access and refresh tokens.
        :param user_id: The user ID to include in the tokens.
        :param expiration_minutes: The expiration time for the access token in minutes.
        :param refresh_expiration_days: The expiration time for the refresh token in days.
        :return: A tuple containing the generated access token and refresh token.
        """
        access_expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        refresh_expiration_time = datetime.utcnow() + timedelta(days=refresh_expiration_days)

        access_payload = {
            'user_id': user_id,
            'exp': access_expiration_time
        }
        refresh_payload = {
            'user_id': user_id,
            'exp': refresh_expiration_time
        }

        access_token = jwt.encode(access_payload, cls.secret_key, algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, cls.refresh_secret_key, algorithm='HS256')

        return access_token, refresh_token

    @classmethod
    def verify_token(cls, access_token):
        """
        Verify the JWT token.

        :param token: The JWT token to verify.
        :return: The payload if the token is valid, None otherwise.
        """
        try:
            payload = jwt.decode(access_token, cls.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError: 
            print("Token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid token.")
        return None

    @classmethod
    def refresh_token(cls, refresh_token):
        """
        Refresh the access token using a refresh token.

        :param refresh_token: The refresh token to use for token refreshing.
        :return: The new access token if refresh is successful, None otherwise.
        """
        try:
            payload = jwt.decode(refresh_token, cls.refresh_secret_key, algorithms=['HS256'])
            user_id = payload['user_id']
            return cls.generate_tokens(user_id)[0]  # Returning the new access token
        except jwt.ExpiredSignatureError:
            print("Refresh token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid refresh token.")
        return None


