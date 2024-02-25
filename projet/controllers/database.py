import hashlib
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

from models.base import Base
from models.user import User
from views.database import DBView


class DBManager:
    """
    Class for managing database connections and operations.
    """

    credentials = None
    engine = None
    session = None
    headers = {"access_token":None, "refresh_token":None}
    connected_user = None
    activated_commercial = None
    activated_support = None
    activated_customer = None
    activated_contract = None
    activated_event = None

    @classmethod
    def init(cls, env):
        """
        Initialize the database manager with the specified environment.

        :param env: The environment (e.g., 'production', 'development').
        """
        cls.credentials = cls.load_config(env)
        try:
            cls.engine = create_engine(cls.url())
            cls.session = scoped_session(sessionmaker(bind=cls.engine))
            print("Connection established to the database. Please log in.")
        except Exception as e:
            print(f"Error establishing database connection: {e}")

    @classmethod
    def url(cls):
        """
        Property to construct the database URL.

        :return: The constructed database URL.
        """
        username = cls.credentials.get('username')
        password = cls.credentials.get('password')
        host = cls.credentials.get('host')
        database = cls.credentials.get('database')
        return f"postgresql://{username}:{password}@{host}/{database}"

    @classmethod
    def reset_data(cls):
        """
        Reset session data.
        """
        cls.headers = {"access_token":None, "refresh_token":None}
        cls.connected_user = None
        cls.activated_commercial = None
        cls.activated_support = None      
        cls.activated_customer = None
        cls.activated_contract = None
        cls.activated_event = None

    @classmethod
    def create(cls):
        from controllers.permission import PermissionManager

        """
        Create the database and initialize with initial data.
        """
        try:
            username, password = DBView.credentials()
            stored_password_hash = cls.credentials.get('password')
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if cls.credentials.get('username') != username or password_hash != stored_password_hash:
                raise Exception("Authentication failed. Invalid username or password.")

            print("Initializing database....")
            
            cls.drop_and_create_tables()
            # Create initial user data
            init_data_user = cls.credentials.get("init_data_user", {})
            user = User(
                fullname=init_data_user.get("fullname"),
                email=init_data_user.get("email"),
                password=init_data_user.get("password"),
                department=init_data_user.get("department")
                )

            # Add user to the session and commit
            with cls.session() as session:
                session.add(user)
                PermissionManager.set_permissions()
                session.commit()
                print("Initialization completed successfully.")                

        except Exception as e:
            print(f"Error: {e}") 
   
    @classmethod
    def drop_and_create_tables(cls):
        """
        Drop existing tables and create new ones.

        """
        Base.metadata.reflect(bind=cls.engine)
        Base.metadata.drop_all(bind=cls.engine)
        Base.metadata.create_all(cls.engine)
 
    @staticmethod
    def load_config(env):
        """
        Load the database configuration from a YAML file.

        :param env: The environment (e.g., 'production', 'development').
        :return: The database credentials.
        """
        try:
            print("Loading database configuration....")
            with open("config.yaml", 'r') as yaml_file:
                credentials = yaml.safe_load(yaml_file)[env]
            print("Database configuration loaded.")
            return credentials
        except FileNotFoundError as e:
            print(f"Error loading database configuration: {e}")
        except yaml.YAMLError as e:
            print(f"Error loading YAML from config file: {e}")

    @classmethod
    def info_activate(cls):
        """
        Get information about the activated entities.

        :return: Information about the activated entities.
        """
        info_activate = ""
        session = cls.session()

        try:
            # Refresh the activated_ instances within the active session
            for attr in ["activated_event", "activated_contract", "activated_customer", "activated_support", "activated_commercial"]:
                if getattr(cls, attr):
                    setattr(cls, attr, session.merge(getattr(cls, attr)))
            if cls.connected_user:
                if cls.connected_user.department=="C":
                    cls.activated_commercial=cls.connected_user
                elif cls.connected_user.department=="S":
                    DBManager.activated_support=cls.connected_user
            
            info_activate += f" [-] Connected User: {cls.connected_user}\n" if cls.connected_user else ""
            info_activate += f" [-] Commercial: {cls.activated_commercial}\n" if cls.activated_commercial else ""
            info_activate += f" [-] Support : {cls.activated_support}\n" if cls.activated_support else ""
            info_activate += f" [-] Customer: {cls.activated_customer}\n" if cls.activated_customer else ""
            info_activate += f" [-] Contract: {cls.activated_contract}\n" if cls.activated_contract else ""
            info_activate += f" [-] Event: {cls.activated_event}\n" if cls.activated_event else ""

        except Exception as e:
            print(f"Error getting information about activated entities: {e}")
            # Log the exception or handle it appropriately

        finally:
            # Close the session
            session.close()

        return info_activate


    @classmethod
    def get_current_object(cls):
        """
        Get the current activated object.

        :return: The current activated object.
        """
        object_mapping = {
            "event": cls.activated_event is not None,
            "contract": cls.activated_contract is not None,
            "customer": cls.activated_customer is not None,
            "user": cls.connected_user is not None,
            "database": not cls.connected_user is not None
        }

        object = next((key for key, value in object_mapping.items() if value), None)
        return object
