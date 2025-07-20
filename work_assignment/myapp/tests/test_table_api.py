# myapp/tests/test_table_api.py
from django.test import Client, TestCase

# ---------- tiny fixture: strict edge‑case checks -----------------------

class TableTinyFixtureTest(TestCase):
    """
    Uses 'tiny.json' – minimal data set
    Quick assertions: row order, zero‑fill, edge rows.
    """
    fixtures = ["tiny.json"]

    def setUp(self):
        self.client = Client()
        self.cols = ["11 Jan", "12 Jan"]

    def rows(self):
        return self.client.get("/api/table/").json()

    def test_row_count_and_order(self):
        rows = self.rows()
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0]["name"], "Supervisor")
        self.assertEqual(rows[-1]["name"], "Unassigned")

    def test_unassigned_hours(self):
        unassigned = self.rows()[-1]
        self.assertEqual(unassigned["12 Jan"], 3)


# ---------- sample fixture: sanity‑check real‑world numbers -------------

class TableSampleFixtureTest(TestCase):
    """
    Uses the bigger 'sample.json' shipped with the repo.
    A couple of smoke tests to ensure the
    aggregation still works on realistic data volumes.
    """
    fixtures = ["sample.json"]

    def setUp(self):
        self.client = Client()
        # pull columns directly so test auto‑adapts if dates grow
        self.cols = self.client.get("/api/table/").json()[0].keys()

    def test_has_unassigned_row_or_not(self):
        """
        sample.json currently has NO truly unassigned tasks,
        so the last row shouldn't be 'Unassigned'.
        """
        last_row = self.client.get("/api/table/").json()[-1]
        self.assertNotEqual(last_row["name"], "Unassigned")

    def test_all_rows_have_all_columns(self):
        """
        Make sure every row contains every date column (zero‑filled allowed)
        so the front‑end never has to guard against missing keys.
        """
        data = self.client.get("/api/table/").json()
        for row in data:
            for col in self.cols:
                self.assertIn(col, row)
