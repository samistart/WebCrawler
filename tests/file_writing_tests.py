import unittest
import file_writing


class FileWritingTests(unittest.TestCase):
    def test_get_file_location_should_remove_file_name_and_slash(self):
        file_path = 'go_cardless/images/flags/NL-flag-icon@2x.png'
        file_location = file_writing.get_file_location(file_path)
        file_location_should_equal = 'go_cardless/images/flags'
        self.assertEqual(file_location_should_equal, file_location)

    def test_get_file_path_removes_slash_and_adds_file_extension(self):
        project_name = 'go_cardless'
        page_url = 'https://gocardless.com/de-de/faq/dashboard/'
        file_path = file_writing.get_file_path(project_name, page_url)
        file_path_should_equal = 'go_cardless/de-de/faq/dashboard.html'
        self.assertEqual(file_path_should_equal, file_path)