from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from controllers.database import DBManager
from decorators import requires_permissions
from controllers.filter import FilterManager

class BaseManager:
    """Base class for managing objects."""
    
    def __init__(self, model, view):
        """
        Initialize the BaseManager.

        Args:
            model: The model class associated with the manager.
            view: The view class associated with the manager.
        """
        self.model = model
        self.view = view
    
    @classmethod
    @requires_permissions("read")
    def display(cls, filter=[], mode=None):
        """
        View method to display data based on filters and mode.

        Args:
            filter (Optional): A filter argument for querying data.
            mode (Optional): The display mode ('list' or 'expand').

        Raises:
            Exception: If an error occurs during the viewing process.
        """
        try:
            session = DBManager.session()
       
            obj_model = cls.model
            expr_filter = ()
            msg, expr_filter = FilterManager.parse_filter_arguments(object=obj_model, filter_arg=filter)
            
            data = session.query(obj_model).filter(and_(*expr_filter)).order_by(obj_model.id).all()
            
            title = f" Used filter ({msg})"
            cls.view.list(data, title) if mode == "list" else cls.view.expand(data, title)
        except Exception as e:
            print(f"Error displaying: {e}")
        finally:
            session.close()

    @classmethod
    @requires_permissions("read")
    def activate(cls, id=None):
        """
        Activate an object by setting it as the activated object in DBManager.

        Args:
            id (Optional): The ID of the object to activate.

        Raises:
            NoResultFound: If no object is found with the given ID.
            Exception: If an error occurs during the activation process.
        """
        try:
            session = DBManager.session

            # Get the model and query the object by ID
            obj_model = cls.model
            obj_instance = session.query(obj_model).filter(obj_model.id == id).one()

            # Set the activated object in DBManager
            setattr(DBManager, f"activated_{obj_model.__name__.lower()}", obj_instance)
        except NoResultFound:
            print("Activation failed. Data not found.")
            obj_instance=None
        except Exception as e:
            print(f"Error activating {obj_model.__name__}: {e}")
            obj_instance=None
        finally:
            # Remove the session
            session.close()
        
        return obj_instance

    @classmethod
    @requires_permissions("read")
    def deactivate(cls):
        """
        Deactivate the currently activated object by setting it to None in DBManager.
        """
        obj_model = cls.model
        setattr(DBManager, f"activated_{obj_model.__name__.lower()}", None)
    
    @classmethod
    @requires_permissions("delete")
    def delete(cls, id=None):
        """
        Delete an object by its ID.

        Args:
            id (Optional): The ID of the object to delete.

        Raises:
            NoResultFound: If no object is found with the given ID.
            SQLAlchemyError: If an error occurs during the deletion process.
        """
        try:
            session = DBManager.session()
            obj_model = cls.model
            obj_instance = session.query(obj_model).filter(obj_model.id == id).one()
            session.delete(obj_instance)
            session.commit()
            
            activated_object = getattr(DBManager, f"activated_{obj_model.__name__.lower()}", None)

            if activated_object and getattr(obj_instance, 'id', None) == getattr(activated_object, 'id', None):
                setattr(DBManager, f"activated_{obj_model.__name__.lower()}", None)

            print(f"{obj_model.__name__.lower()} {obj_instance} deleted successfully.")
        except NoResultFound:
            print(f"{obj_model.__name__} not found!")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting {obj_model.__name__.lower()}: {e}")
        finally:
            # Remove the scoped session
            session.close()

    @classmethod
    @requires_permissions("create")
    def create(cls):
        """
        Create a new object.

        Raises:
            SQLAlchemyError: If an error occurs during the creation process.
        """
        try:
            # Use a scoped session
            session = DBManager.session()
            
            # Get the model and call the class method to create/update
            obj_model = cls.model
            obj_instance = cls.view.create_update()

            # Add to the session and commit
            session.add(obj_instance)
            session.commit()

            print(f"{obj_model.__name__} '{obj_instance}' created successfully.")
        except Exception as e:
            # Rollback on error
            session.rollback()
            print(f"Error creating {obj_model.__name__}: {e}")
        finally:
            # Remove the session
            session.close()

    
    @classmethod
    @requires_permissions("update")
    def update(cls, id=None):
        """
        Update an object by its ID.

        Args:
            id (Optional): The ID of the object to update.

        Raises:
            NoResultFound: If no object is found with the given ID.
            SQLAlchemyError: If an error occurs during the update process.
        """
      
        try:
            # Use a scoped session
            session = DBManager.session()
            obj_model = cls.model
            obj_instance = session.query(obj_model).filter(obj_model.id == id).one()
            obj_instance = cls.view.create_update(obj_instance)
            session.commit()
            print(f"{cls.model.__name__} '{obj_instance}' updated successfully.")

            active_instance = getattr(DBManager, f"activated_{cls.model.__name__.lower()}", None)
            if active_instance and active_instance.id == id:
                cls.activate(id=id)
        except NoResultFound:
            print(f"{cls.model.__name__} not found!")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating {cls.model.__name__}: {e}")
        finally:
            # Remove the scoped session
            session.close()
