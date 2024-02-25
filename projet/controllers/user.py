"""
Class for managing user-related operations.
"""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from decorators import requires_permissions
import hashlib
import pyinputplus as pyip

from models.user import User
from controllers.authenticate import AuthManager
from controllers.base import BaseManager
from controllers.database import DBManager
from views.user import UserView

class UserManager(BaseManager):
    """
    Class for managing user-related operations.
    """
    model = User
    view  = UserView

    @classmethod
    def logout(cls, confirm=True):
        """
        Log out the current user.

        Raises:
            Exception: If the user doesn't confirm the logout.
        """
        if confirm:
            if pyip.inputYesNo(" Confirme logout ? (Y/N): ", default="N") == "no":
                return
        DBManager.reset_data()
        print(" User disconnected successfully.")

    @classmethod
    def login(cls, email):
        """
        Log in a user with the provided email.

        Args:
            email: The email of the user to log in.

        Raises:
            Exception: If authentication fails or the user is already connected.
        """
        try:
            if DBManager.connected_user is not None:
                print(f" {DBManager.connected_user} is connected. Disconnect first.")
                return
            
            password = cls.view.authenticate(email)
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            session = DBManager.session()
       
            query = session.query(User)
            user = query.filter_by(email=email, password=password_hash).one()
            print(f" User {user} authenticated successfully.")
            DBManager.connected_user = user
           
            access_token, refresh_token = AuthManager.generate_tokens(DBManager.connected_user.id)
            DBManager.headers = {"access_token":access_token, "refresh_token": refresh_token}           
           
        except NoResultFound:
            print(" Authentication failed. Invalid credentials.")
        except SQLAlchemyError as e:
            print(f" Error during user authentication: {e}")
    
    @classmethod
    def activate(cls, id=None):
        result=super().activate(id=id)
        if result :
            if result.department == "C":
                DBManager.activated_commercial = result
            elif result.department=="S":
                DBManager.activated_support = result
            else:
                print("You can not activate a Manager. You have to connect as Manager.")   
    
    @classmethod
    @requires_permissions("read")
    def deactivate(cls):
        if DBManager.activated_support:
            DBManager.activated_support = None
        elif DBManager.activated_commercial :
            DBManager.activated_commercial = None
    