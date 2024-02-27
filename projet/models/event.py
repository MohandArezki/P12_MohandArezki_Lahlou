from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship,validates
from datetime import datetime

from models.base import Base

class Event(Base):
    """
    Represents an event in the system.

    Attributes:
    - name: The name of the event.
    - date_start: The start date and time of the event.
    - date_end: The end date and time of the event.
    - location: The location of the event.
    - attendees: The number of attendees at the event.
    - notes: Additional notes about the event.
    - contract_id: Foreign key referencing the associated contract.
    - support_id: Foreign key referencing the associated user providing support.

    Relationships:
    - contract: Relationship with the associated contract.
    - support: Relationship with the associated user providing support.
    """

    name = Column(String(50), nullable=False,info={"label": "Event"})
    date_start = Column(DateTime,info={"label": "Start Date"})
    date_end = Column(DateTime,info={"label": "End Date"})
    location = Column(String(50),info={"label": "Location"})
    attendees = Column(Integer,info={"label": "Attendees"})
    notes = Column(String(255),info={"label": "Note"})    
    contract_id = Column(Integer, ForeignKey('contract.id'), nullable=False)
    support_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    
    support = relationship('User', back_populates='events')
    contract = relationship('Contract', back_populates='events')
    @property
    def status(self):
        """Get the status of the event (Planned, Ongoing, or Passed)."""
        now = datetime.now()
        return (
            "Planned" if self.date_start > now else
            "Ongoing" if self.date_start <= now <= self.date_end else
            "Passed"
        )
   
    @validates('contract')
    def validate_contract(self, key, contract):        
        if contract and not contract.signed:
            raise ValueError("The contracted must be signed before attaching events.")
        return contract 
    
    @validates('support')
    def validate_support(self, key, contact):        
        if contact and contact.department != 'S':
            raise ValueError("The associated user must be from support department.")
        return contact
   
    def __repr__(self):
        """Return a string representation of the Event."""
        return f'[{self.id}] - {self.name[:20]}...'
    
    @property
    def full_repr(self):
        """Return a string representation of the Event."""
        return f'[{self.id}] - {self.name}'