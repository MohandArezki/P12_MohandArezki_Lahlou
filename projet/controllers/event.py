from models.event import Event
from controllers.base import BaseManager
from views.event import EventView
from decorators import requires_signed_contract, requires_permissions


class EventManager(BaseManager):
    """
    Manager class for handling operations related to events.

    Inherits from BaseManager.

    Attributes:
        model: The Event model.
        view: The EventView class for handling views.
    """

    model = Event
    view = EventView

    @classmethod
    @requires_signed_contract
    def create(cls):
        """
        Create a new event.

        Requires the presence of a signed contract.

        Returns:
            None
        """
        return super().create()

    @classmethod
    @requires_signed_contract
    def update(cls, id=None):
        """
        Update an existing event.

        Args:
            id (Optional): The ID of the event to update.

        Requires the presence of a signed contract.

        Returns:
            None
        """
        return super().update(id=id)
