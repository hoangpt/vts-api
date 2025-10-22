from typing import Optional
from mod.user_mgmt.user_service import UserService
import bcrypt
import jwt
from datetime import datetime, timedelta

# Secret key for JWT (should be stored securely in environment variables)
SECRET_KEY = "your_secret_key"

class UserAuth:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, username_or_email: str, password: str) -> Optional[str]:
        """
        Authenticate a user using their username or email and password.

        Args:
            username_or_email (str): The username or email of the user.
            password (str): The user's password.

        Returns:
            Optional[str]: A JWT token if authentication is successful, None otherwise.
        """
        user = self.user_service.get_user_by_username_or_email(username_or_email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = self._generate_jwt(user)
            return token
        return None

    def _generate_jwt(self, user: UserDTO) -> str:
        """
        Generate a JWT token for the authenticated user.

        Args:
            user (UserDTO): The authenticated user.

        Returns:
            str: A JWT token.
        """
        payload = {
            "sub": user.id,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    def check_permission(self, user_id: int, required_role: str) -> bool:
        """
        Check if a user has the required role to perform an action.

        Args:
            user_id (int): The ID of the user to check.
            required_role (str): The required role (e.g., "admin").

        Returns:
            bool: True if the user has the required role, False otherwise.
        """
        user = self.user_service.get_user_by_id(user_id)
        return user.role == required_role

    def logout(self, token: str) -> bool:
        """
        Logout a user by invalidating their token (not implemented in this example).

        Args:
            token (str): The JWT token to invalidate.

        Returns:
            bool: True if logout is successful, False otherwise.
        """
        # Token invalidation logic would go here (e.g., using a token blacklist)
        return True
