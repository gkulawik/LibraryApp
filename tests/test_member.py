import pytest
from LibraryApp.src.library import Library, Book, Dvd, Memberships


class TestMember:

    @pytest.fixture
    def setup_data(self):
        self.library1 = Library()

        self.book1 = Book(title="The Lord of the Rings - Trilogy",
                          genre="fantasy fiction",
                          author="J.R.R. Tolkien",
                          isbn="978-0261103252")

        self.book2 = Book(title="The hobbit, or There and back again",
                          genre="fantasy fiction",
                          author="J.R.R. Tolkien",
                          isbn="978-0007458424")

        self.dvd1 = Dvd(title="Gladiator",
                        genre="historical fiction",
                        director="Ridley Scott",
                        duration="2h 18min")

        self.library1.add_resource(new_resource=self.book1, quantity_to_add=2)
        self.library1.add_resource(new_resource=self.book2, quantity_to_add=2)
        self.library1.add_resource(new_resource=self.dvd1, quantity_to_add=2)
        self.member1 = self.library1.create_member(name="Jane Doe", membership_status=Memberships.PREMIUM)

        return self.library1, self.member1

    def test_borrow_empty_list_of_resources(self, setup_data):
        """
        Trying to borrow resources without providing any resource ID raises a KeyError
        """
        with pytest.raises(KeyError):
            self.member1.borrow_resources([])

    def test_borrow_already_borrowed_resource(self, setup_data):
        """
        Trying to borrow a resource the member has already borrowed raises a KeyError
        """
        self.member1.borrow_resources([1])
        with pytest.raises(KeyError):
            self.member1.borrow_resources([1])

    def test_borrow_duplicate_resources(self, setup_data):
        """
        Trying to borrow more than 1 copy of a given resource raises a KeyError
        """
        with pytest.raises(KeyError):
            self.member1.borrow_resources([1, 2, 1])

    def test_borrow_unavailable_resources(self, setup_data):
        """
        Trying to borrow unavailable resources doesn't raise any errors; the member gets to borrow just the resources
        that are available; for unavailable ones they get a print statement.
        """
        # Removing all copies of a resource making it unavailable
        self.library1.remove_resources(quantity_to_remove=2, title="The Lord of the Rings - Trilogy")
        # The removed book doesn't appear on a list of available library books
        assert self.library1.available_books == [Book(title='The hobbit, or There and back again',
                                                      genre='fantasy fiction',
                                                      availability_status=True,
                                                      quantity=2,
                                                      id=2,
                                                      author='J.R.R. Tolkien',
                                                      isbn='978-0007458424')]
        # The member simply gets to borrow just the available resources
        self.member1.borrow_resources([2, 1])
        assert self.member1.borrowed_resources_ids == [2]

    def test_borrow_resource_that_does_not_exist_in_library(self, setup_data):
        """
        Trying to borrow a resource that doesn't exist in a library raises a KeyError
        """
        with pytest.raises(KeyError):
            self.member1.borrow_resources([21])

    def test_borrow_multiple_resources(self, setup_data):
        """
        Borrowing a few resources from a library
        """
        self.member1.borrow_resources([1, 3])
        assert self.member1.borrowed_resources_ids == [1, 3]
        assert self.member1.borrowed_resources_details == [{'title': 'The Lord of the Rings - Trilogy',
                                                            'genre': 'fantasy fiction',
                                                            'author': 'J.R.R. Tolkien',
                                                            'isbn': '978-0261103252'},
                                                           {'title': 'Gladiator',
                                                            'genre': 'historical fiction',
                                                            'director': 'Ridley Scott',
                                                            'duration': '2h 18min'}]
        assert self.library1.resources == [Book(title='The Lord of the Rings - Trilogy',
                                                genre='fantasy fiction',
                                                availability_status=True,
                                                quantity=1,
                                                id=1,
                                                author='J.R.R. Tolkien',
                                                isbn='978-0261103252'),
                                           Book(title='The hobbit, or There and back again',
                                                genre='fantasy fiction',
                                                availability_status=True,
                                                quantity=2,
                                                id=2,
                                                author='J.R.R. Tolkien',
                                                isbn='978-0007458424'),
                                           Dvd(title='Gladiator',
                                               genre='historical fiction',
                                               availability_status=True,
                                               quantity=1,
                                               id=3,
                                               director='Ridley Scott',
                                               duration='2h 18min')]

    def test_return_empty_list_of_resources(self, setup_data):
        """
        Trying to return resources without providing any resource ID raises a KeyError
        """
        with pytest.raises(KeyError):
            self.member1.return_resources([])

    def test_return_more_items_than_borrowed(self, setup_data):
        """
        Trying to return more items than the member has borrowed raises a KeyError
        """
        self.member1.borrow_resources([2])
        with pytest.raises(KeyError):
            self.member1.return_resources([1, 2])

    def test_return_resources_that_were_not_borrowed(self, setup_data):
        """
        Trying to return resources that the member hasn't borrowed raises a KeyError
        """
        self.member1.borrow_resources([2])
        with pytest.raises(KeyError):
            self.member1.return_resources([1])

    def test_return_multiple_resources(self, setup_data):
        """
        Returning multiple library resources that have previously been borrowed
        """
        self.member1.borrow_resources([1, 2])
        self.member1.return_resources([1, 2])
        assert self.member1.borrowed_resources_ids == []


