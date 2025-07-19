from django.test import TestCase, Client

class TableAPITest(TestCase):
    fixtures = ["fixtures/sample.json"]  # relative to the tests/ directory

    def setUp(self):
        self.client = Client()

    def test_table_output(self):
        resp = self.client.get("/api/table/")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        # expected columns
        expected_cols = {"name", "11 Jan", "12 Jan"}
        for row in data:
            self.assertTrue(expected_cols.issubset(row.keys()))

        # row order: position then workers
        self.assertEqual(data[0]["name"], "Position 1")
        self.assertIn(data[1]["name"], {"Worker 1", "Worker 2"})

        # numeric checks
        pos_row = data[0]
        self.assertEqual(pos_row["11 Jan"], 7)
        self.assertEqual(pos_row["12 Jan"], 8)   # matches fixture sums
