from dataclasses import dataclass, field, asdict
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


class Memberships(Enum):
    REGULAR = 1
    PREMIUM = 2


class Library:
    def __init__(self):
        self._resources = []
        self._members = []

    def add_resource(self, new_resource: LibraryResource, quantity_to_add: int):
        if not isinstance(new_resource, LibraryResource):
            raise TypeError("The resource must be of type derived from type LibraryResource, e.g., Book!")
        if not quantity_to_add > 0:
            raise ValueError("If you're adding a resource, you must add at least 1 item!")
        if len(self._resources) > 0:
            # If the resource already exists in the library, simply add more copies of it
            resource_already_exists = False
            resource_attributes = asdict(new_resource)
            for resource in self._resources:
                match = all(getattr(resource, key, None) == value for key, value in resource_attributes.items())
                if match:
                    resource.quantity += quantity_to_add
                    resource_already_exists = True
                    break
            if not resource_already_exists:
                new_resource.quantity = quantity_to_add
                new_resource.availability_status = True
                latest_assigned_id = (max(resource.id for resource in self._resources)) + 1
                new_resource.id = latest_assigned_id
                self._resources.append(new_resource)
        else:
            new_resource.quantity = quantity_to_add
            new_resource.availability_status = True
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

    def remove_resources(self, quantity_to_remove: int, **criteria):
        """
        Remove the resource from the library. You must specify the number of copies of the item you want to remove
        and provide criteria to identify the resource you want to remove, e.g., its title or ID.
        If you remove all existing copies, the resource becomes unavailable.
        :param quantity_to_remove: Number of copies to be removed.
        :param criteria: Information to identify the resource you want to remove, e.g., its title or ID.
        :return:
        """
        removed_any_items = False
        for resource in self._resources:
            match = any(getattr(resource, key, None) == value for key, value in criteria.items())
            if match:
                if quantity_to_remove < resource.quantity:
                    resource.quantity = resource.quantity - quantity_to_remove
                    print(f"Removed {quantity_to_remove} items")
                    removed_any_items = True
                elif quantity_to_remove > resource.quantity:
                    raise ValueError("Can't remove more items than there are in the library!")
                else:
                    # If you remove all copies, the resource becomes unavailable
                    resource.quantity = 0
                    resource.availability_status = False
                    removed_any_items = True
        if not removed_any_items:
            raise KeyError("Didn't find any resources matching your criteria!")

    def create_member(self, name, membership_status):
        if len(self._members) > 0:
            user_id = (max(member.id for member in self._members)) + 1
        else:
            user_id = 1
        if membership_status is Memberships.PREMIUM:
            borrowing_limit = 4
        else:
            borrowing_limit = 2
        new_member = Member(name, self, membership_status, user_id, borrowing_limit)
        self._members.append(new_member)
        return new_member

    def check_out_resources(self, member, requested_resources_ids: list[int]) -> list[int]:
        # Initial checks before searching the library.
        # Can this member borrow any resources at all?
        if member.borrowing_limit < 1:
            raise Exception("You can't borrow any more resources. Return something first!")
        # Are they trying to borrow more resources than their current borrowing limit?
        if member.borrowing_limit < len(requested_resources_ids):
            raise Exception(f"You can't borrow more resources than your current borrowing "
                            f"limit= {member.borrowing_limit}. \n"
                            "Try borrowing less items or return something first!")
        borrowed_resources_ids = []
        found_any_resources = False
        # Search the library resources looking for the resources the member is trying to borrow
        for requested_resource_id in requested_resources_ids:
            found_requested_resource = False
            for resource in self._resources:
                if getattr(resource, "id") == requested_resource_id:
                    found_any_resources = True
                    found_requested_resource = True
                    print(f"Found the resource you wanted to borrow: ID= {requested_resource_id}")
                    # Check if the found resource is available
                    if resource.availability_status:
                        borrowed_resources_ids.append(resource.id)
                        resource.quantity -= 1
                        print("You've now borrowed this resource")
                        if resource.quantity < 1:
                            resource.availability_status = False
                    else:
                        print("But this resource is currently unavailable")
                    # Stop searching the resources as soon as the requested resource is found in the library
                    break
            if not found_requested_resource:
                print(f"Didn't find the resource you wanted to borrow: ID= {requested_resource_id}")
        if not found_any_resources:
            raise KeyError("Didn't find any of the resources you wanted to borrow!")
        return borrowed_resources_ids

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

    @property
    def available_books(self):
        available_books = []
        for book in self.books:
            if getattr(book, "availability_status"):
                available_books.append(book)
        return available_books

    @property
    def available_dvds(self):
        available_dvds = []
        for dvd in self.dvds:
            if getattr(dvd, "availability_status"):
                available_dvds.append(dvd)
        return available_dvds

    @property
    def available_cds(self):
        available_cds = []
        for cd in self.cds:
            if getattr(cd, "availability_status"):
                available_cds.append(cd)
        return available_cds

    @property
    def available_magazines(self):
        available_magazines = []
        for magazine in self.magazines:
            if getattr(magazine, "availability_status"):
                available_magazines.append(magazine)
        return available_magazines


class Member:
    def __init__(self, name: str, library: Library, membership_status: Memberships, user_id: int, borrowing_limit: int):
        self._name = name
        self._library = library
        self._membership_status = membership_status
        self._user_id = user_id
        self._borrowing_limit = borrowing_limit
        self._borrowed_resources_ids = []  # List of borrowed resources' IDs from the library

    def borrow_resources(self, resources_ids: list[int]):
        """
        Borrow resources by identifying resources to borrow by their unique IDs.
        It's possible to borrow multiple resources at once.
        Member can borrow only 1 copy of each resource.
        :param resources_ids: List of resources' IDs
        :return:
        """
        # Check if the list isn't empty.
        if len(resources_ids) < 1:
            raise KeyError("You must specify at least 1 resource ID you want to borrow.")
        # Check if the list doesn't contain duplicate IDs as it's possible to borrow only 1 copy of each resource.
        # A set in Python automatically removes any duplicate values:
        if not len(resources_ids) == len(set(resources_ids)):
            raise KeyError("You can borrow only 1 copy of each resource. Please enter unique resource IDs.")
        # Check if the member isn't trying to borrow a copy of a resource they've already borrowed
        for already_borrowed_resource_id in self._borrowed_resources_ids:
            for resource_to_borrow_id in resources_ids:
                if already_borrowed_resource_id == resource_to_borrow_id:
                    raise KeyError("You can only borrow 1 copy of each library resource. "
                                   f"You've already borrowed this item: ID= {already_borrowed_resource_id}")

        # Access a method from the library and pass the member instance as the first argument
        # so the library can access this member's attributes
        new_borrowed_resources_ids = self.library.check_out_resources(self, resources_ids)
        if len(new_borrowed_resources_ids) > 0:
            self._borrowing_limit -= len(new_borrowed_resources_ids)
            for new_resource_id in new_borrowed_resources_ids:
                self._borrowed_resources_ids.append(new_resource_id)

    @property
    def user_id(self):
        return self._user_id

    @property
    def borrowing_limit(self):
        return self._borrowing_limit

    @property
    def library(self):
        return self._library

    @property
    def borrowed_resources_ids(self):
        return self._borrowed_resources_ids

    def __str__(self):
        return f"{self._name}, {self._membership_status.name} member"
