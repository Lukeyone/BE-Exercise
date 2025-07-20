# test_empty_position.py
# ----------------------------------------------------------
# Tests the "Empty Position" enhancement:
# If a worker or task has no position, the API should
# return a synthetic row named "Empty Position" with
# correctly rolled-up hours.
# ----------------------------------------------------------

from django.test import TestCase, Client

def is_empty_position_label(name: str) -> bool:
    return "No" in name and "Position" in name

class EmptyPositionTest(TestCase):
    # Loads test-only data from tests/fixtures/empty_position.json
    fixtures = ["empty_position.json"]

    def setUp(self):
        self.client = Client()

    def test_empty_position_row_exists(self):
        """
        The response from /api/table/ should include a row
        named "Empty Position" when unpositioned data exists.
        """
        rows = self.client.get("/api/table/").json()
        self.assertTrue(any(is_empty_position_label(r["name"]) for r in rows))

    def test_hours_roll_up(self):
        """
        The duration of unpositioned tasks should be correctly
        summed under the "Empty Position" row for each date.
        """
        rows = self.client.get("/api/table/").json()
        row = next(r for r in rows if is_empty_position_label(r["name"]))
        self.assertEqual(row["11 Jan"], 2)
        self.assertEqual(row["12 Jan"], 4)
