from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,event
from sqlalchemy.orm import relationship,validates

from datetime import datetime

from models.base import Base


class Customer(Base):
    """
    Represents a customer in the system.

    Attributes:
    - name: The name of the customer.
    - email: The email address of the customer.
    - phone: The phone number of the customer.
    - company: The company name of the customer.
    - created_date: The date when the customer was created.
    - updated_date: The date when the customer was last updated.
    - contact_id: Foreign key referencing the associated user.

    Relationships:
    - contact: Relationship with the associated user.
    - contracts: Relationship with the associated contracts.
    """

    name = Column(String(30), nullable=False,info={"label": "Name"})
    email = Column(String(30), nullable=False, unique=True,info={"label": "Email"})
    phone = Column(String(15), nullable=True, info={"label": "Phone number"})
    company = Column(String(30), nullable=False,info={"label": "Company name"})
    created_date = Column(DateTime, default=datetime.now,info={"label": "Created on"})
    updated_date = Column(DateTime, onupdate=datetime.now,info={"label": "Updated on"})
    contact_id = Column(Integer, ForeignKey('user.id'), nullable=False, info={"label": "Contact ID"})

    contact = relationship("User", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer",cascade="all, delete")
    
    def contracts_count(self, signed=[True, False]):
        """Get the count of contracts associated with the customer."""
        return sum(1 for contract in self.contracts if contract.signed in signed)

    def contracts_total_amount(self, signed=[True, False]):
        """Get the total amount of contracts associated with the customer."""
        return sum(contract.total_amount for contract in self.contracts if contract.signed in signed)

    def contracts_due_amount(self, signed=[True, False]):
        """Get the due amount of contracts associated with the customer."""
        return sum(contract.due_amount for contract in self.contracts if contract.signed in signed)
        
    def events_count(self, status=["Planned", "Ongoing","Passed"]):
        """Count events associated with the customer."""
        return sum(1 for contract in self.contracts for event in contract.events if event.status in status)
    
    def __repr__(self):
        """Return a string representation of the Customer."""
        return f'[{self.id}] - {self.name}'

    @validates('contact')
    def validate_commercial_contact(self, key, contact):
        """
        Validate that the associated user is from commercial department.

        Args:
        key: The key of the attribute being validated.
        contact: The associated user.

        Returns:
        User: The associated user.

        Raises:
        ValueError: If the associated user is not from commercial department.
        """
        if contact and contact.department != 'C':
            raise ValueError("The associated user must be from commercial department.")
        return contact

    def before_delete_listener(self, mapper, connection, target):
        """
        Listener to prevent deletion of a customer with associated contracts.

        Args:
        mapper: The mapper in use.
        connection: The connection being used.
        target: The customer to be deleted.

        Raises:
        ValueError: If the customer has associated contracts.
        """
        contracts_count = len(target.contracts)
        if contracts_count > 0:
            # Avoid cascade deleting
            raise ValueError(f"The customer is attached to {contracts_count} contract(s).\n"
                             f"Reassign the contracts to other customers or delete them and retry.")

# Attach the listeners to the Customer class
event.listen(Customer, 'before_delete', Customer().before_delete_listener)