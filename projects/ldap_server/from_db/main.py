import sys
import uuid
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, create_engine
from sqlalchemy.dialects.postgresql import UUID  # or use sqlalchemy.types for generic UUID support
from sqlalchemy.orm import Session, declarative_base

from twisted.application import service
from twisted.internet.endpoints import serverFromString
from twisted.internet.protocol import ServerFactory
from twisted.python.components import registerAdapter
from twisted.python import log
from ldaptor.inmemory import ReadOnlyInMemoryLDAPEntry
from ldaptor.interfaces import IConnectedLDAPEntry
from ldaptor.protocols.ldap.ldapserver import LDAPServer

# SQLAlchemy base
Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    # Basic attributes
    id = Column(Integer, primary_key=True)
    uid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)  # UUID for unique user identification
    sAMAccountName = Column(String(255), unique=True, nullable=False)  # Pre-Windows 2000 logon name
    userPrincipalName = Column(String(255), unique=True, nullable=False)  # Logon name in email format (e.g., user@domain.com)
    first_name = Column(String(255), nullable=False)  # maps to givenName
    last_name = Column(String(255), nullable=False)  # maps to sn (surname)
    display_name = Column(String(255))  # maps to displayName
    email = Column(String(255), nullable=False)  # maps to mail

    # Organizational and contact attributes
    department = Column(String(255))  # maps to department
    company = Column(String(255))  # maps to company
    phone_number = Column(String(255))  # maps to telephoneNumber
    title = Column(String(255))  # maps to title (job title)

    # Security and account control attributes
    user_account_control = Column(Integer, default=512)  # maps to userAccountControl (default 512 for normal account)
    password = Column(LargeBinary)  # maps to unicodePwd
    pwd_last_set = Column(Integer)  # timestamp of the last time the password was set
    
    # Unique identifiers
    object_guid = Column(String(255), unique=True)  # maps to objectGUID
    object_sid = Column(String(255), unique=True)  # maps to objectSID
    primary_group_id = Column(Integer, default=513)  # maps to primaryGroupID (default 513 for Domain Users)
    
    # Location and address attributes
    street_address = Column(String(255))  # maps to streetAddress
    city = Column(String(255))  # maps to l (locality)
    state = Column(String(255))  # maps to st (state)
    postal_code = Column(String(255))  # maps to postalCode
    country_code = Column(String(3))  # maps to countryCode (e.g., US, UK)

    # Account status
    account_disabled = Column(Boolean, default=False)  # maps to part of userAccountControl

# Function to create the root LDAP tree from the domain
def create_ldap_tree_from_domain(domain):
    components = domain.split('.')

    # Create the top-level domain (TLD)
    root_dn = f"dc={components[-1]}"
    root = ReadOnlyInMemoryLDAPEntry(root_dn, {
        "dc": [components[-1]],
        "objectClass": ["dcObject"]
    })

    current_entry = root
    # Create each component of the domain
    for i in range(len(components) - 2, -1, -1):
        current_dn = f"dc={components[i]}"
        # Only the last component should have the 'organization' object class
        if i == 0:
            object_class = ["dcObject", "organization"]
        else:
            object_class = ["dcObject"]

        current_entry = current_entry.addChild(
            current_dn,
            {
                "dc": [components[i]],
                "objectClass": object_class
            }
        )

    return root, current_entry

# Tree class to build the tree from the database
class Tree:
    def __init__(self, db_engine, domain_name):
        self.db_engine = db_engine
        self.root = self.build_tree_from_db(domain_name)

    def build_tree_from_db(self, domain_name):
        """
        Building LDAP tree.
        Call this method if you need to reload data from the database.
        """
        root, tree = create_ldap_tree_from_domain(domain_name)
        people_dn = f"ou=people"
        users_tree = tree.addChild(people_dn, {
            "ou": ["people"],
            "objectClass": ["organizationalUnit"]
        })

        db_session = Session(self.db_engine)

        for user in db_session.query(User):
            user_dn = f"uid={user.uid}"
            users_tree.addChild(
                user_dn,
                {
                    "uid": [str(user.uid)],  # Convert UUID to string for LDAP
                    "sAMAccountName": [user.sAMAccountName],  # Add sAMAccountName
                    "userPrincipalName": [user.userPrincipalName],  # Add userPrincipalName
                    "givenName": [user.first_name],
                    "sn": [user.last_name],
                    "displayName": [user.display_name] if user.display_name else [],  # Optional field
                    "mail": [user.email],
                    "department": [user.department] if user.department else [],  # Optional field
                    "company": [user.company] if user.company else [],  # Optional field
                    "telephoneNumber": [user.phone_number] if user.phone_number else [],  # Optional field
                    "title": [user.title] if user.title else [],  # Optional field
                    "objectGUID": [user.object_guid],  # Add objectGUID
                    "objectSID": [user.object_sid],  # Add objectSID
                    "primaryGroupID": [str(user.primary_group_id)],  # Convert to string for LDAP
                    "streetAddress": [user.street_address] if user.street_address else [],  # Optional field
                    "l": [user.city] if user.city else [],  # Optional field
                    "st": [user.state] if user.state else [],  # Optional field
                    "postalCode": [user.postal_code] if user.postal_code else [],  # Optional field
                    "countryCode": [user.country_code] if user.country_code else [],  # Optional field
                    "userAccountControl": [str(user.user_account_control)],  # Convert to string for LDAP
                    "accountDisabled": [str(user.account_disabled)],  # Convert to string for LDAP
                    "objectClass": ["top", "person", "inetOrgPerson"],  # Standard object classes
                },
            )

        db_session.close()

        return root


class LDAPServerFactory(ServerFactory):
    protocol = LDAPServer

    def __init__(self, root):
        self.root = root

    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.debug = self.debug
        proto.factory = self
        return proto


def create_db(db):
    """Creating a database with a table of users and a couple of rows"""
    db_engine = create_engine(db)
    Base.metadata.bind = db_engine
    Base.metadata.create_all(db_engine)  # Create all tables

    db_session = Session(db_engine)

    # Check if the User table is empty
    if db_session.query(User).count() == 0:
        user1 = User(
            uid=uuid.uuid4(),  # Generate a new UUID
            sAMAccountName="first_example",  # Example sAMAccountName
            userPrincipalName="first@example.com",  # Example userPrincipalName
            first_name="First",
            last_name="Example",
            display_name="First Example",  # Example displayName
            email="first@example.com",
            department="Sales",  # Example department
            company="Example Corp",  # Example company
            phone_number="123-456-7890",  # Example phone number
            title="Sales Representative",  # Example job title
            object_guid=str(uuid.uuid4()),  # Generate a new objectGUID
            object_sid="S-1-5-21-1234567890-123456789-1234567890-1001",  # Example objectSID
            primary_group_id=513,  # Default for Domain Users
            street_address="123 Example St",  # Example address
            city="Example City",  # Example city
            state="EX",  # Example state
            postal_code="12345",  # Example postal code
            country_code="US",  # Example country code
            user_account_control=512,  # Default for normal account
            account_disabled=False  # Set account to enabled
        )

        user2 = User(
            uid=uuid.uuid4(),  # Generate a new UUID
            sAMAccountName="second_example",  # Example sAMAccountName
            userPrincipalName="second@example.com",  # Example userPrincipalName
            first_name="Second",
            last_name="Example",
            display_name="Second Example",  # Example displayName
            email="second@example.com",
            department="Marketing",  # Example department
            company="Example Corp",  # Example company
            phone_number="098-765-4321",  # Example phone number
            title="Marketing Manager",  # Example job title
            object_guid=str(uuid.uuid4()),  # Generate a new objectGUID
            object_sid="S-1-5-21-1234567890-123456789-1234567890-1002",  # Example objectSID
            primary_group_id=513,  # Default for Domain Users
            street_address="456 Example Ave",  # Example address
            city="Example City",  # Example city
            state="EX",  # Example state
            postal_code="12345",  # Example postal code
            country_code="US",  # Example country code
            user_account_control=512,  # Default for normal account
            account_disabled=False  # Set account to enabled
        )

        db_session.add(user1)
        db_session.add(user2)

        db_session.commit()

    db_session.close()

    return db_engine


if __name__ == "__main__":
    from twisted.internet import reactor

    if len(sys.argv) == 4:
        port = int(sys.argv[1])
        db = sys.argv[2]
        domain = sys.argv[3]
    else:
        port = 8080
        db = "sqlite:///ldap.sqlite"
        domain = "example.com"

    engine = create_db(db)

    # First of all, to show logging info in stdout :
    log.startLogging(sys.stderr)

    # Initialize the LDAP tree from the database
    tree = Tree(engine, domain)

    # Register the adapter so the server can get the tree
    registerAdapter(lambda x: x.root, LDAPServerFactory, IConnectedLDAPEntry)

    factory = LDAPServerFactory(tree.root)
    factory.debug = True

    application = service.Application("ldaptor-server")
    myService = service.IServiceCollection(application)

    serverEndpointStr = f"tcp:{port}"
    e = serverFromString(reactor, serverEndpointStr)
    d = e.listen(factory)

    reactor.run()
