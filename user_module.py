from dataclasses import dataclass, field
from abc import ABC


@dataclass
class UserInterface(ABC):
    username: str
    salt: str = field(default_factory=str)
    hash: str = field(default_factory=str)
    email_address: str = field(default_factory=str)

@dataclass
class User(UserInterface):
    username: str
    salt: str = field(default_factory=str)
    hash: str = field(default_factory=str)
    email_address: str = field(default_factory=str)