"""Generate per-squad contact reports from CSV input."""

import csv
import sys

NAME_COLUMN = "Please provide your name."
PHONE_COLUMN = "Please provide your cell phone number."
EMAIL_COLUMN = "Please provide your email address."


def parse_squads(raw_squads):
    """Return a list of normalized squad names from a comma-separated field."""
    if not raw_squads:
        return []

    return [squad.strip() for squad in raw_squads.split(",") if squad.strip()]


def build_squad_report(csv_path):
    """Build a mapping of squad names to member contact details."""
    squads = {}

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            return squads

        squad_column = reader.fieldnames[-1]
        for row in reader:
            member = {
                "name": row.get(NAME_COLUMN, "").strip(),
                "phone": row.get(PHONE_COLUMN, "").strip(),
                "email": row.get(EMAIL_COLUMN, "").strip(),
            }

            for squad in parse_squads(row.get(squad_column, "")):
                squads.setdefault(squad, []).append(member)

    return squads


def format_squad_report(squads):
    """Format squad report output text."""
    lines = []
    for squad in sorted(squads):
        lines.append(f"Squad: {squad}")
        for member in squads[squad]:
            lines.append(
                f"- Name: {member['name']}, Cell: {member['phone']}, Email: {member['email']}"
            )
        lines.append("")

    return "\n".join(lines).rstrip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python main.py <path_to_csv>")

    print(format_squad_report(build_squad_report(sys.argv[1])))
