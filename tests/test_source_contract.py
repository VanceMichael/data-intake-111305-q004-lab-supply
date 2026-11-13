import hashlib
import json
import unittest

from lab_supply.client import Client
from lab_supply.decoding import parse_page, records as decode_records
from lab_supply.origin import load_scenario, serve


class SourceContractTests(unittest.TestCase):
    def test_domain_observations_preserve_source_distinctions(self):
        scenario = load_scenario()
        records = scenario["source_records"]
        with serve(scenario) as origin:
            client = Client(origin.base_url)
            self.assertEqual(records[0]["sku"], records[1]["sku"])
            self.assertNotEqual(records[0]["supplier"], records[1]["supplier"])
            self.assertNotEqual(records[0]["package"], records[1]["package"])
            self.assertEqual(records[0]["supplier"], records[2]["supplier"])
            self.assertNotEqual(records[0]["valid_from"], records[2]["valid_from"])

    def test_every_record_has_the_declared_source_identity(self):
        scenario = load_scenario()
        for record in scenario["source_records"]:
            for field in scenario["identity_fields"]:
                self.assertIn(field, record)
                self.assertNotEqual(str(record[field]).strip(), "")


if __name__ == "__main__":
    unittest.main()
