import pytest
from LibraryApp.src.library import Library, Book, Dvd, Cd, Magazine, Member, Memberships


class TestLibrary:

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

        return self.library1, self.book1, self.book2, self.dvd1,

    def test_add_book_resource(self, setup_data):
        """
        Adding 4 copies of a book
        """
        self.library1.add_resource(self.book1, 4)
        assert self.library1.resources == [Book(title='The Lord of the Rings - Trilogy',
                                                genre='fantasy fiction',
                                                availability_status=True,
                                                quantity=4,
                                                id=1,
                                                author='J.R.R. Tolkien',
                                                isbn='978-0261103252')]

    def test_add_unsupported_resource(self, setup_data):
        """
       Adding a resource of not supported type, e.g., a list, should throw a TypeError
       """
        self.book_of_list_type = ["Book"]
        with pytest.raises(TypeError):
            self.library1.add_resource(self.book_of_list_type, 5)

    def test_add_negative_number_of_books(self, setup_data):
        """
        Adding less than 1 book should throw a ValueError
        """
        with pytest.raises(ValueError):
            self.library1.add_resource(self.book1, -1)

    def test_add_the_same_book_twice(self, setup_data):
        """
        Adding the same book twice should only increase the number of available copies,
        not create an additional library resource
        """
        self.library1.add_resource(self.book1, 4)
        self.library1.add_resource(self.book1, 1)
        assert self.library1.resources == [Book(title='The Lord of the Rings - Trilogy',
                                                genre='fantasy fiction',
                                                availability_status=True,
                                                quantity=5,
                                                id=1,
                                                author='J.R.R. Tolkien',
                                                isbn='978-0261103252')]

    def test_find_resources_by_title(self, setup_data):
        """
        Looking for resources by the title. Should return a list with a single book on it.
        """
        self.library1.add_resource(self.book1, 2)
        self.library1.add_resource(self.dvd1, 2)
        self.library1.add_resource(self.book2, 3)
        assert self.library1.find_resources(title="The hobbit, or There and back again") == [Book \
                                                                         (title="The hobbit, or There and back again",
                                                                          genre="fantasy fiction",
                                                                          availability_status=True,
                                                                          quantity=3,
                                                                          id=3,
                                                                          author="J.R.R. Tolkien",
                                                                          isbn="978-0007458424")]

    def test_find_resources_by_author(self, setup_data):
        """
        Looking for resources by the author. Should return a list with 2 books on it.
        """
        self.library1.add_resource(self.book1, 2)
        self.library1.add_resource(self.dvd1, 2)
        self.library1.add_resource(self.book2, 3)
        print(self.library1.resources)
        assert self.library1.find_resources(author="J.R.R. Tolkien") == [Book \
                                                                         (title='The Lord of the Rings - Trilogy',
                                                                          genre='fantasy fiction',
                                                                          availability_status=True,
                                                                          quantity=2,
                                                                          id=1,
                                                                          author='J.R.R. Tolkien',
                                                                          isbn='978-0261103252'),
                                                                     Book \
                                                                         (title="The hobbit, or There and back again",
                                                                          genre="fantasy fiction",
                                                                          availability_status=True,
                                                                          quantity=3,
                                                                          id=3,
                                                                          author="J.R.R. Tolkien",
                                                                          isbn="978-0007458424")]

    def test_remove_single_copy_of_a_resource(self, setup_data):
        """
        Removing a single copy of a book.  Should only decrease its quantity.
        """
        self.library1.add_resource(self.book1, 2)
        self.library1.add_resource(self.book2, 3)
        self.library1.remove_resources(quantity_to_remove=1, title="The Lord of the Rings - Trilogy")
        assert self.library1.resources == [Book(title='The Lord of the Rings - Trilogy',
                                                genre='fantasy fiction',
                                                availability_status=True,
                                                quantity=1,
                                                id=1,
                                                author='J.R.R. Tolkien',
                                                isbn='978-0261103252'),
                                           Book \
                                               (title="The hobbit, or There and back again",
                                                genre="fantasy fiction",
                                                availability_status=True,
                                                quantity=3,
                                                id=2,
                                                author="J.R.R. Tolkien",
                                                isbn="978-0007458424")]

    def test_remove_all_copies_of_a_resource(self, setup_data):
        """
        Removing all copies of a book.  Should make the book unavailable with 0 copies of the item.
        """
        self.library1.add_resource(self.book1, 2)
        self.library1.add_resource(self.book2, 3)
        self.library1.remove_resources(quantity_to_remove=2, title="The Lord of the Rings - Trilogy")
        assert self.library1.resources == [Book(title='The Lord of the Rings - Trilogy',
                                                genre='fantasy fiction',
                                                availability_status=False,
                                                quantity=0,
                                                id=1,
                                                author='J.R.R. Tolkien',
                                                isbn='978-0261103252'),
                                           Book \
                                               (title="The hobbit, or There and back again",
                                                genre="fantasy fiction",
                                                availability_status=True,
                                                quantity=3,
                                                id=2,
                                                author="J.R.R. Tolkien",
                                                isbn="978-0007458424")]

    def test_create_member(self, setup_data):
        """
        Creating a Premium member.
        """
        self.library1.create_member(name="John Doe", membership_status=Memberships.PREMIUM)
        assert len(self.library1.members) == 1
        assert str(self.library1.members[0]) == "John Doe, PREMIUM member"


if __name__ == '__main__':
    pytest.main(['-v', 'test_library.py'])
