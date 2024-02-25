from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for declarative SQLAlchemy models using class-based declarative syntax."""

    @declared_attr
    def __tablename__(cls):
        """Generate the table name based on the class name."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True,info={"label": "ID"})
    """Primary key column for the table."""
