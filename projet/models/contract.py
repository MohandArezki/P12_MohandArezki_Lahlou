from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, Date, event
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.orm import relationship
from datetime import datetime

from models.base import Base


class Contract(Base):
    """
    Represents a contract in the system.

    Attributes:
    - total_amount: The total amount of the contract.
    - due_amount: The due amount of the contract.
    - signed: Indicates whether the contract is signed or not.
    - customer_id: Foreign key referencing the associated customer.
    - contract_date: The date when the contract was created.
    - customer: Relationship with the associated customer.
    - events: Relationship with the associated events.
    """
    contract_date = Column(Date, nullable=False, default=datetime.now, info={"label": "Date"})
    signed = Column(Boolean, nullable=False, default=False, info={"label": "Signed ?"})
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False, info={"label": "ID Customer"})
    total_amount = Column(Float(2), nullable=False, info={"label": "Total Amount"})
    due_amount = Column(Float(2), info={"label": "Due Amount"})
  

    customer = relationship("Customer", back_populates="contracts")

    events = relationship("Event", back_populates="contract",cascade="all, delete")

    def events_count(self, status=["Planned", "Ongoing","Passed"]):
        """Get the count of events ."""
        return sum(1 for event in self.events if event.status in status) 
    
    @property
    def contact(self):
        """Get the contact associated with the customer of this contract."""
        return self.customer.contact
    
    @property
    def state(self):
        """Get the state of the contract (signed or not signed)."""
        return "Signed" if self.signed else "Not Signed"
    
    def __repr__(self):
        """Return a string representation of the Contract."""
        return f'[{self.id}] '

    @staticmethod    
    def before_contract_update_listener(mapper, connection, target):
        """
        Event listener triggered before updating a Contract.

        Raises:
        - ValueError: If events are attached to a signed contract.
        """
        state = get_history(target, 'signed')
        original_signed = state.deleted[0] if state.deleted else state.added[0] if state.added else None
        if target.events and original_signed and not target.signed:
            raise ValueError("Cannot unsign a contract with attached events. To unsign, remove all attached events.")

# Attach the listener to the Contract class
event.listen(Contract, 'before_update', Contract.before_contract_update_listener)