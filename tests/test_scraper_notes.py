import unittest
from scraper import scraper_notes

class TestScraper(unittest.TestCase):
    def test_get_brands_and_countries(self):
        url = 'https://www.parfumo.com/Brands'
        result = scraper_notes.get_brands_and_countries(url)
        self.assertIsNotNone(result)  # Checks that something is returned
        self.assertGreater(len(result), 0)  # Checks that at least one brand is returned

    def test_get_perfumes(self):
        # Uses a sample brand_info for testing
        brand_info = ("A la Façon London", "United Kingdom", "https://www.parfumo.com/Brands/A_la_Facon_London")
        result = scraper_notes.get_perfumes(brand_info)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

    def test_get_notes(self):
        # Uses a sample perfume_info for testing
        perfume_info = ("A la Façon London", "United Kingdom", "https://www.parfumo.com/Perfumes/A_la_Facon_London/Casablanca_After_Shave")
        result = scraper_notes.get_notes(perfume_info)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
