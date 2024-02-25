from models.customer import Customer
from controllers.base import BaseManager
from views.customer import CustomerView
from decorators import requires_commercial


class CustomerManager(BaseManager):
    """
    Manager class for handling operations related to customers.

    Inherits from BaseManager.

    Attributes:
        model: The Customer model.
        view: The CustomerView class for handling views.
    """

    model = Customer
    view = CustomerView

    @classmethod
    @requires_commercial
    def create(cls):
        """
        Create a new customer.

        Requires the presence of commercial-related permissions.

        Returns:
            None
        """
        return super().create()

    @classmethod
    @requires_commercial
    def update(cls, id=None):
        """
        Update an existing customer.

        Args:
            id (Optional): The ID of the customer to update.

        Requires the presence of commercial-related permissions.

        Returns:
            None
        """
        return super().update(id=id)
