"""Unit tests for squad report generation."""

import os
import tempfile
import unittest

from main import build_squad_report, format_squad_report, parse_squads


class TestSquadReport(unittest.TestCase):
    def test_parse_squads(self):
        self.assertEqual(
            parse_squads("Ain’t No Mountain High Enough - Hiking, Serenity Squad"),
            ["Ain’t No Mountain High Enough - Hiking", "Serenity Squad"],
        )

    def test_build_and_format_squad_report(self):
        csv_content = """Timestamp,Please provide your name.,Please provide your cell phone number.,Please provide your email address.,"So, what are you waiting for? SquaDDle Up! Select the squads that inspire you most. There’s no limit to how many squads you can join, but we ask that you actively participate to support and respect the efforts of our amazing squad leaders. "
2/7/2026 10:50:27,Jernei Johnson,5204605363,jerneij2@gmail.com,"Ain’t No Mountain High Enough - Hiking, Serenity Squad, Grad-U-Waites Squad, Pretty in Twenty"
2/7/2026 11:10:27,Ada Lovelace,1234567890,ada@example.com,"Serenity Squad"
"""
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            tmp.write(csv_content)
            csv_path = tmp.name

        try:
            report = build_squad_report(csv_path)
            self.assertIn("Serenity Squad", report)
            self.assertEqual(len(report["Serenity Squad"]), 2)
            self.assertEqual(
                report["Serenity Squad"][0]["email"],
                "jerneij2@gmail.com",
            )

            output = format_squad_report(report)
            self.assertIn("Squad: Serenity Squad", output)
            self.assertIn("Name: Jernei Johnson", output)
            self.assertIn("Cell: 5204605363", output)
            self.assertIn("Email: ada@example.com", output)
        finally:
            os.unlink(csv_path)


if __name__ == "__main__":
    unittest.main()
