import pytest
from LibraryApp.src.library import Library, Book


class TestLibrary:

    @pytest.fixture
    def setup_data(self):
        self.library1 = Library()
        self.book1 = Book(title="The Lord of the Rings - Trilogy",
                          genre="fantasy fiction",
                          author="J.R.R. Tolkien",
                          isbn="978-0261103252")
        return self.library1, self.book1

    def test_add_book_resource(self, setup_data):
        """
        Adding 4 books
        """
        self.library1.add_resource(self.book1, 4)
        assert self.library1.resources == [Book(title='The Lord of the Rings - Trilogy',
                                                genre='fantasy fiction',
                                                availability_status=True,
                                                quantity=4,
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


if __name__ == '__main__':
    pytest.main(['-v', 'test_library.py'])
