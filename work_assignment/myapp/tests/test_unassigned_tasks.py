# test_unassigned_tasks.py
# ----------------------------------------------------------
# Tests the "Unassigned" row enhancement:
# If a task exists with no worker assignment, the API
# should include an "Unassigned" row and roll up its hours.
# ----------------------------------------------------------

from django.test import TestCase, Client

class UnassignedRowsTest(TestCase):
    # Loads test-only data from tests/fixtures/unassigned_tasks.json
    fixtures = ["unassigned_tasks.json"]

    def setUp(self):
        self.client = Client()

    def test_unassigned_row_present(self):
        """
        A row called "Unassigned" should be included
        whenever there are tasks with no Assignment.
        """
        last_row = self.client.get("/api/table/").json()[-1]
        self.assertEqual(last_row["name"], "Unassigned")

    def test_unassigned_hours_correct(self):
        """
        The unassigned row should correctly sum the hours
        of all tasks without a matching Assignment.
        """
        unassigned = next(r for r in self.client.get("/api/table/").json()
                          if r["name"] == "Unassigned")

        self.assertEqual(unassigned["11 Jan"], 11)  # 3+2+5+1
        self.assertEqual(unassigned["12 Jan"], 15)  # 4+3+2+6
        self.assertEqual(unassigned["13 Jan"], 3)   # 1+2
