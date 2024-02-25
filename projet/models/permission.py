from sqlalchemy import Column, Enum, UniqueConstraint

from models.base import Base

PERMISSIONS = {
    '0': 'No Permission',
    '1': 'Authorized',
    '2': 'Owner Authorization Required'
}

class Permission(Base):
    """
    Represents a permission in the system.

    Attributes:
    - department: The department associated with the permission.
    - object: The object for which the permission is granted.
    - action: The action for which the permission is granted.
    - permission: The level of permission (0, 1, or 2).

    UniqueConstraint:
    - Ensures uniqueness of the combination of department, object, and action.

    Methods:
    - __repr__: Returns a string representation of the Permission.
    """

    __table_args__ = (
        UniqueConstraint('department', 'object', 'action', name='uq_department_object_action'),
    )

    department = Column(Enum('M', 'S', 'C', name='department'), nullable=False)
    object = Column(Enum('User', 'Customer', 'Contract', 'Event', name='Object'), nullable=False)
    action = Column(Enum('create', 'read', 'update', 'delete', name='Action'), nullable=False)
    permission = Column(Enum('0', '1', '2', name='Permission'), nullable=False)

    def __repr__(self):
        """
        Return a string representation of the Permission.
        """
        return f"Department: {self.department} | Object: {self.object} | action: {self.action} | Permission: {PERMISSIONS.get(self.permission)}"
