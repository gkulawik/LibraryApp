from dataclasses import dataclass, field
from typing import List, Any
from enum import Enum
from operator import attrgetter

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
    availability_status: bool = field(default=False)
    quantity: int = field(default=0)
    id: int = field(default=0)


@dataclass
class Book(LibraryResource):
    # Define fields with default values or leave them to be set in __post_init__
    # This is a workaround as all fields in a dataclass that have a default value must come after those without
    author: str = field(default=None)  # Temporarily set a default, will be replaced
    isbn: str = field(default=None)  # Temporarily set a default, will be replaced

    def __post_init__(self):
        # Assert to ensure no default values are used accidentally
        assert self.author is not None, "Author is required"
        assert self.isbn is not None, "ISBN is required"


@dataclass
class Dvd(LibraryResource):
    director: str = field(default=None)  # Temporarily set a default, will be replaced
    duration: str = field(default=None)  # Temporarily set a default, will be replaced

    def __post_init__(self):
        # Assert to ensure no default values are used accidentally
        assert self.director is not None, "Director is required"
        assert self.duration is not None, "Duration is required"


@dataclass
class Cd(LibraryResource):
    artist: str = field(default=None)  # Temporarily set a default, will be replaced
    duration: str = field(default=None)  # Temporarily set a default, will be replaced

    def __post_init__(self):
        # Assert to ensure no default values are used accidentally
        assert self.artist is not None, "Artist is required"
        assert self.duration is not None, "Duration is required"


@dataclass
class Magazine(LibraryResource):
    publisher: str = field(default=None)  # Temporarily set a default, will be replaced
    publication_date: str = field(default=None)  # Temporarily set a default, will be replaced

    def __post_init__(self):
        # Assert to ensure no default values are used accidentally
        assert self.publisher is not None, "Publisher is required"
        assert self.publication_date is not None, "Publication date is required"


# class Memberships(Enum):
#     REGULAR = 1
#     PREMIUM = 2


class Library:
    def __init__(self):
        self._resources = []

    def add_resource(self, new_resource: LibraryResource, quantity: int):
        if not isinstance(new_resource, LibraryResource):
            raise TypeError("The resource must be of type derived from type LibraryResource, e.g., Book!")
        if not quantity > 0:
            raise ValueError("If you're adding a resource, you must add at least 1 item!")
        # While adding a new resource, it becomes available for people to borrow
        new_resource.quantity = quantity
        new_resource.availability_status = True
        # The new resource also gets its unique ID number
        if len(self._resources) > 0:
            latest_assigned_id = (max(resource.id for resource in self._resources)) + 1
            new_resource.id = latest_assigned_id
        else:
            new_resource.id = 1
        self._resources.append(new_resource)

    def find_resources(self, **keywords) -> List[Any]:
        """
        Return a list of resources that match the criteria entered by user, e.g., title = "Harry Potter".
        """
        results = []
        for resource in self._resources:
            # The default value None prevents AttributeError from being raised if one of the objects in the list
            # doesn't have an attribute specified in kwargs.
            match = any(getattr(resource, key, None) == value for key, value in keywords.items())
            if match:
                results.append(resource)
        return results

    # def remove_resource(self, resource_to_remove: LibraryResource, quantity: int):
    #     if not isinstance(resource_to_remove, LibraryResource):
    #         raise TypeError("The resource must be of type derived from type LibraryResource, e.g., Book!")
    #     # If you remove all quantity, remove the resource completely

    @property
    def resources(self):
        return self._resources

    @property
    def books(self):
        """
        Filter the list of all resources looking for Book objects.
        :return: A list of all Book objects
        """
        book_resources = filter(lambda x: isinstance(x, Book), self._resources)
        return list(book_resources)

    @property
    def dvds(self):
        """
        Filter the list of all resources looking for DVD objects.
        :return: A list of all DVD objects
        """
        dvd_resources = filter(lambda x: isinstance(x, Dvd), self._resources)
        return list(dvd_resources)

    @property
    def cds(self):
        """
        Filter the list of all resources looking for CD objects.
        :return: A list of all CD objects
        """
        cd_resources = filter(lambda x: isinstance(x, Cd), self._resources)
        return list(cd_resources)

    @property
    def magazines(self):
        """
        Filter the list of all resources looking for Magazine objects.
        :return: A list of all Magazine objects
        """
        magazine_resources = filter(lambda x: isinstance(x, Magazine), self._resources)
        return list(magazine_resources)