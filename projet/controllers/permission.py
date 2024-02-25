from sqlalchemy.orm.exc import NoResultFound
from models.permission import Permission
from models.contract import Contract 
from decorators import requires_connection
from controllers.database import DBManager

class PermissionManager:
    """
    Class for managing permissions.
    """
    @classmethod
    def set_permissions(cls):
        permissions_data = [
            {"department": "M", "object": "User", "create": "1", "read": "1", "update": "1", "delete": "1"},
            {"department": "C", "object": "User", "read": "1", "update": "2"},
            {"department": "S", "object": "User", "read": "1", "update": "2"},

            {"department": "M", "object": "Customer", "create":"1", "read": "1", "update": "1", "delete": "1"},
            {"department": "C", "object": "Customer", "create": "1", "read": "1", "update": "2"},
            {"department": "S", "object": "Customer", "read": "1"},

            {"department": "M", "object": "Contract", "create": "1", "read": "1", "update": "1", "delete": "1"},
            {"department": "C", "object": "Contract", "create": "1", "read": "1", "update": "2"},
            {"department": "S", "object": "Contract", "read": "1", "update": "2"},

            {"department": "M", "object": "Event", "create": "1", "read": "1", "update": "1", "delete": "1"},
            {"department": "C", "object": "Event", "create": "1", "read": "1", "update": "2"},
            {"department": "S", "object": "Event", "read": "1", "update": "2"},
        ]
        try:
            session = DBManager.session()
            for data in permissions_data:
                for action in ["create", "read", "update", "delete"]:
                    if data.get(action):
                        permission = Permission(
                            department=data["department"],
                            object=data["object"],
                            action=action,
                            permission=data[action]
                        )
                        session.add(permission)
            session.commit()
        except:
             print(f"Error when setting permissions.")
    @staticmethod
    def _ownership_check(obj, inst_obj):
        """
        Perform ownership check for a specific object type.

        Args:
            obj: The object type.
            inst_obj: An instance of the object.

        Returns:
            bool: True if ownership check passes, False otherwise.
        """
        if obj.__name__ == "User":
            return DBManager.connected_user.id == inst_obj.id if inst_obj else False
        elif obj.__name__ == "Customer":
            return DBManager.activated_commercial.id == inst_obj.contact.id if inst_obj else False
        elif obj.__name__ == "Contract":
            return DBManager.activated_commercial.id == inst_obj.customer.contact.id if inst_obj else False
        elif obj.__name__ == "Event":
            if DBManager.activated_support:
                return(DBManager.activated_support.id == inst_obj.support.id)
            elif inst_obj.contract:
                return(DBManager.activated_commercial.id == inst_obj.contract.customer.contact.id)
        return False
    
    @classmethod
    @requires_connection
    def check_permissions(cls, obj, action, id_instance=None):
        """
        Check permissions for a user to perform a specific action on an object.

        Args:
            obj: The object on which the action is performed.
            action: The action to be performed (create, read, update, delete).
            id_instance: An optional ID of the instance.

        Returns:
            bool: True if the user has the required permissions, False otherwise.
        """
        session = DBManager.session()

        try:
            # Merge activated objects into the session
            for attr in ["activated_event", "activated_contract", "activated_customer", "activated_support", "activated_commercial"]:
                if getattr(DBManager, attr):
                    setattr(DBManager, attr, session.merge(getattr(DBManager, attr)))

            user = DBManager.connected_user

            if id_instance is not None:
                inst_obj = session.query(obj).filter_by(id=id_instance).one_or_none()
                if inst_obj is None:
                    print(f"{obj.__name__.capitalize()} with id {id_instance} not found.")
                    return False
            else:
                inst_obj = None

            print(f"Checking permissions for | User: {user} | Action: {action.capitalize()} | Object: {obj.__name__}{f' | Instance: {inst_obj}' if inst_obj else ''}.")

            # Check if USER can ACTION the OBJECT
            response = session.query(Permission).filter_by(department=user.department, object=obj.__name__, action=action).one()

            if response.permission == "1":
                print("User has the required authorization.")
                return True

            if response.permission == "2":
                if inst_obj is not None:
                    ownership_check = cls._ownership_check(obj, inst_obj)

                    if not ownership_check:
                        print(f"Ownership check failed. {action.upper()} permission is exclusive to the owner of {obj.__name__.upper()}.")
                    else:
                        return True
                else:
                    if obj.__name__ == "Event" and DBManager.activated_contract:
                        current_contract = session.query(Contract).filter_by(id=DBManager.activated_contract.id).one_or_none()

                        if current_contract and DBManager.activated_commercial.id != current_contract.customer.contact_id:
                            print(f"Ownership check failed. {action.upper()} permission is exclusive to the owner of Contract.")
                        else:
                            return True
                    else:
                        print(f"Ownership check failed. Please specify the id of {obj.__name__.upper()}")

        except NoResultFound:
            print(f"Permission not found for members of {user.department_name} to {action.upper()} {obj.__name__.upper()}.")
        except Exception as e:
            print(e)
        finally:
            session.close()

        return False
    