from sqlalchemy import Column, String, Enum, event

from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import get_history
import pyinputplus as pyip

from models.base import Base


DEPARTMENTS = {'M': 'Management Department', 'C': 'Commercial Department', 'S': 'Support Department'}

class User(Base):
    """
    Represents a user in the system.

    Attributes:
    - fullname: The full name of the user.
    - email: The email address of the user (unique).
    - password: The hashed password of the user.
    - department: The department to which the user belongs.

    Relationships:
    - customers: One-to-Many relationship with Customer model.
    - events: One-to-Many relationship with Event model.

    Methods:
    - department_name: Returns the name of the user's department.
    - get_customers_count: Returns the count of customers associated with the user.
    - get_contracts_count: Returns the count of contracts associated with the user.
    - get_events_count: Returns the count of events associated with the user.
    - __repr__: Returns a string representation of the User.
    """
    
    fullname = Column(String(30), nullable=False, info={"label": "Fullname"})
    email = Column(String(30), nullable=False, unique=True, info={"label": "Email"})
    password = Column(String(100), nullable=False, info={"label": "Password"})
    department = Column(Enum('M', 'S', 'C', name='department'), nullable=False, info={"label": "Department"})

    customers = relationship("Customer", back_populates="contact", cascade="all, delete")
    events = relationship("Event", back_populates="support")
 
    @property
    def department_name(self):
        """Returns the name of the user's department."""
        return DEPARTMENTS.get(self.department, 'Unknown Department')
      
    def customers_count(self):
        """Returns the count of customers associated with the user."""
        return len(self.customers)   
     
    def supported_events_count(self, status=["Planned", "Ongoing", "Passed"]):
        return sum(1 for event in self.events if event.status in status)

    def contracts_count(self, signed=[True, False]):
        return sum(customer.contracts_count(signed) for customer in self.customers)

    def contracts_total_amount(self, signed=[True, False]):
        return sum(customer.contracts_total_amount(signed) for customer in self.customers)

    def contracts_due_amount(self, signed=[True, False]):
        return sum(customer.contracts_due_amount(signed) for customer in self.customers)

    def events_count(self, status=["Planned", "Ongoing", "Passed"]):
        return sum(customer.events_count(status) for customer in self.customers)

    def __repr__(self):
        """Returns a string representation of the User."""
        return f"[{self.id}] - {self.fullname}"

    @staticmethod
    def _handle_department_change(target: 'User', original_department: str):
        """
        Handle the logic for department changes.

        Args:
        - target: The User instance.
        - original_department: The original department before the change.

        Raises:
        - ValueError: If there are assigned customers or supported events.
        """
        if original_department == 'C':
            assigned_customers = target.customers_count()
            if assigned_customers > 0:
                raise ValueError(f"The user is from the commercial department. "
                                 f"He has ({assigned_customers}) assigned customers.\n"
                                 f"Reassign the customers for another user or delete them and retry.")

        elif original_department == 'S':
            supported_events = target.supported_events_count()
            if supported_events > 0:
                continue_revoke = input(f"The user supports ({supported_events}) events. "
                                         f"Continue with revoking all assignments? (Y/N): ")
                if continue_revoke.lower() == "y":
                    for event in target.events:
                        event.support_id = None
                else:
                    raise ValueError("Operation cancelled")

    @staticmethod
    def before_update_listener(mapper, connection, target: 'User'):
        """
        Listener to handle actions before updating a User.

        Args:
        - mapper: The mapper in use.
        - connection: The connection being used.
        - target: The User to be updated.
        """
        try:
            state = get_history(target, 'department')
            original_department = state.deleted[0] if state.deleted else state.added[0] if state.added else None
            if target.department != original_department:
                User._handle_department_change(target, original_department)
        except ValueError as e:
            print(f"Error before update: {e}")

    @staticmethod
    def before_delete_listener(mapper, connection, target: 'User'):
        """
        Listener to handle actions before deleting a User.

        Args:
        - mapper: The mapper in use.
        - connection: The connection being used.
        - target: The User to be deleted.
        """
        try:
            User._handle_department_change(target, target.department)
        except ValueError as e:
            print(f"Error before delete: {e}")
            # prevent deletion
            raise

# Attach the listeners to the User class
event.listen(User, 'before_delete', User.before_delete_listener)
event.listen(User, 'before_update', User.before_update_listener)