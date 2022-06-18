from dataclasses import dataclass, field
from abc import ABC


@dataclass
class UserInterface(ABC):
    '''
    Interface for the user Class, can't be instantiated.
    '''
    username: str
    salt: str = field(default_factory=str)
    hash: str = field(default_factory=str)
    email_address: str = field(default_factory=str)

@dataclass
class User(UserInterface):
    '''
    User class can be instantiated with just the user name,
    default field values initilise remaining atributes required by the
    Authorisation Manager.
    '''
    username: str
    salt: str = field(default_factory=str)
    hash: str = field(default_factory=str)
    email_address: str = field(default_factory=str)