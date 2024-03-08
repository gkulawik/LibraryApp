from dataclasses import dataclass, asdict
from typing import List, Optional

"""
To modify the library exercise to allow borrowing more than just books, we can extend the concept of the
Library Management System to include a wider range of resources such as books, DVDs, CDs, and magazines.
Here's how we can modify the requirements and structure:

Requirements:

    Create classes for library resources:
        Book: Represents a book with attributes like title, author, ISBN, genre, and availability status.
        DVD: Represents a DVD with attributes like title, director, genre, duration, and availability status.
        CD: Represents a CD with attributes like title, artist, genre, duration, and availability status.
        Magazine: Represents a magazine with attributes like title, publisher, publication date, genre,
        and availability status.

    Implement inheritance:
        Each resource class (Book, DVD, CD, Magazine) can inherit from a common base class (e.g., LibraryResource)
        that includes shared attributes and methods.
        Base class can contain common attributes such as title, genre, availability status,
        and methods for borrowing and returning resources.

    Encapsulate attributes and methods:
        Encapsulate attributes within classes, with accessors and mutators for necessary attributes.
        Define methods within classes for functionalities such as borrowing and returning resources.

    Functionalities to include:
        Add a resource to the library.
        Remove a resource from the library.
        Search for a resource by title, author/director/artist, or genre.
        Display available resources of each type (books, DVDs, CDs, magazines).
        Allow a member to borrow a resource.
        Allow a member to return a resource.
        Display borrowed resources for a member.
        Display library statistics (total number of resources, number of available resources,
        number of borrowed resources).

    Ensure error handling:
        Implement error handling for cases such as attempting to borrow a resource that is not available
        or returning a resource that was not borrowed.

    Optional additional features:
        Implement support for different types of library memberships (e.g., regular member, premium member)
        with varying borrowing limits.
        Integrate with a database for persistent storage of library resources and member information.
        Allow for fine-grained permission management (e.g., librarian vs. regular member vs. administrator).
        Implement notifications for overdue resources or upcoming due dates.
        """


@dataclass
class LibraryResource:
    title: str
    genre: str
    availability_status: bool


@dataclass
class Book(LibraryResource):
    author: str
    isbn: str


@dataclass
class Dvd(LibraryResource):
    director: str
    duration: str


class LibraryCollection:
    def __init__(self):
        self._books: List[Book] = []
        self._dvds: List[Dvd] = []

    def add_resource(self, new_resource: LibraryResource):
        if isinstance(new_resource, Book):
            self._books.append(new_resource)
        elif isinstance(new_resource, Dvd):
            self._dvds.append(new_resource)

    @property
    def books(self):
        return self._books

    @property
    def dvds(self):
        return self._dvds
