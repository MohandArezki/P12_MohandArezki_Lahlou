from faker import Faker
import hashlib

from controllers.database import DBManager
from models.user import User
from models.customer import Customer
from models.contract import Contract
from models.event import Event


def create_fake_users(session, user_count=5, department='M'):
    """
    Create fake users.

    Args:
        session: SQLAlchemy session object.
        user_count (int): Number of users to create.
        department (str): Department of the users.

    Returns:
        list: List of created users.
    """
    fake = Faker('en_US')
    users = []
    i=1
    for _ in range(user_count):
        
        fullname=fake.name()[:30]
        user = User(
            fullname=fullname,
            email = f"{'commercial' if department=='C' else 'support' if department=='S' else 'manager'}_{i}@epic.com",
            password=hashlib.sha256("password".encode()).hexdigest(),
            department=department
        )
        session.add(user)
        users.append(user)
        i+=1

    session.commit()
    return users

def create_fake_customers(session, customer_count=30, users=None):
    """
    Create fake customers.

    Args:
        session: SQLAlchemy session object.
        customer_count (int): Number of customers to create.
        users (list): List of users to associate with customers.

    Returns:
        list: List of created customers.
    """
    fake = Faker('en_US')
    customers = []

    for _ in range(customer_count):
        customer = Customer(
            name=fake.name()[:30],
            company=fake.company()[:30],
            phone=fake.phone_number()[:15],
            email = fake.safe_email()[-30:],
            contact=fake.random_element(elements=users)
        )
        session.add(customer)
        customers.append(customer)

    session.commit()
    return customers

def create_fake_contracts(session, contract_count=50, customers=None):
    """
    Create fake contracts.

    Args:
        session: SQLAlchemy session object.
        contract_count (int): Number of contracts to create.
        customers (list): List of customers to associate with contracts.

    Returns:
        list: List of created contracts.
    """
    fake = Faker('en_GB')
    contracts = []

    for _ in range(contract_count):
        contract_date = fake.date_between(start_date='-1y', end_date='today')
        total_amount = fake.random_int(min=6000, max=10000)
        due_amount = total_amount - fake.random_int(min=500, max=total_amount)
        contract = Contract(
            contract_date=contract_date,
            total_amount=total_amount,
            due_amount=due_amount,
            signed=fake.pybool(),
            customer_id=fake.random_element(elements=[c.id for c in customers]),
        )
        if not contract.signed:
            contract.due_amount = total_amount
        else:
            contracts.append(contract)

        session.add(contract)

    session.commit()
    return contracts

def create_fake_events(session, event_count=100, contracts=None, supports=None):
    """
    Create fake events.

    Args:
        session: SQLAlchemy session object.
        event_count (int): Number of events to create.
        contracts (list): List of contracts to associate with events.
        supports (list): List of users to use as supports.

    Returns:
        list: List of created events.
    """
    fake = Faker('en_US')

    for _ in range(event_count):
        contract = fake.random_element(elements=contracts)
        event = Event(
            name=fake.text(max_nb_chars=50),
            date_start=fake.date_time_between(start_date='now', end_date='+30d'),
            date_end=fake.date_time_between(start_date='+31d', end_date='+60d'),
            location=fake.city(),
            attendees=fake.random_int(min=1, max=500),
            notes=fake.text(max_nb_chars=255),
            contract_id=contract.id,
            support=fake.random_element(elements=supports) if supports else None,
            contract=contract
        )
        session.add(event)
        session.commit()

def create_fake(session):
    """
    Create fake data for the CRM system.

    Args:
        session: SQLAlchemy session object.
    """
    
    print("Creating fake users...")
    managers = create_fake_users(session, user_count=3, department='M')
    commercials = create_fake_users(session, user_count=5, department='C')

    print("Fake users created successfully.")

    print("Creating fake customers...")
    customers = create_fake_customers(session, customer_count=10, users=commercials)
    print("Fake customers created successfully.")

    print("Creating fake contracts...")
    contracts = create_fake_contracts(session, contract_count=100, customers=customers)
    print("Fake contracts created successfully.")

    print("Creating fake events...")
    supports = create_fake_users(session, user_count=5, department='S')
    create_fake_events(session, event_count=200, contracts=contracts, supports=supports)
    print("Fake events created successfully.")

    print("Fake data generation completed.")

if __name__ == "__main__":
    DBManager.init("production")
    DBManager.create()
    create_fake(DBManager.session())
