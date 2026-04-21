#!/usr/bin/env python3
"""Generate per-squad contact reports from CSV input."""

import argparse
import csv
import io
import sys

NAME_COLUMN = "Please provide your name."
PHONE_COLUMN = "Please provide your cell phone number."
EMAIL_COLUMN = "Please provide your email address."


def parse_squads(raw_squads):
    """Return a list of normalized squad names from a comma-separated field."""
    if not raw_squads:
        return []

    return [squad.strip() for squad in raw_squads.split(",") if squad.strip()]


def format_phone_display(raw):
    """Format a phone value as (NPA) NXX-XXXX when it looks like NANP; else return stripped text."""
    if not raw:
        return ""
    stripped = raw.strip()
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) == 11 and digits[0] == "1":
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    if len(digits) == 7:
        return f"{digits[:3]}-{digits[3:]}"
    return stripped


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
    name_hdr, phone_hdr, email_hdr = "Name", "Phone", "Email"
    lines = []
    for squad in sorted(squads):
        lines.append(f"Squad: {squad}")
        members = sorted(squads[squad], key=lambda m: m["name"].casefold())
        if not members:
            lines.append("")
            continue

        phones_fmt = [format_phone_display(m["phone"]) for m in members]
        w_name = max(len(name_hdr), *(len(m["name"]) for m in members))
        w_phone = max(len(phone_hdr), *(len(p) for p in phones_fmt))
        w_email = max(len(email_hdr), *(len(m["email"]) for m in members))

        lines.append(
            f"  {name_hdr:<{w_name}}  {phone_hdr:<{w_phone}}  {email_hdr:<{w_email}}"
        )
        lines.append(
            f"  {'-' * w_name}  {'-' * w_phone}  {'-' * w_email}"
        )
        for member, phone_out in zip(members, phones_fmt):
            lines.append(
                f"  {member['name']:<{w_name}}  {phone_out:<{w_phone}}  "
                f"{member['email']:<{w_email}}"
            )
        lines.append("")

    return "\n".join(lines).rstrip()


def format_squad_report_csv(squads):
    """Format one squad per block: title line, then member rows as CSV; blank line between squads."""
    blocks = []
    for squad in sorted(squads):
        lines = [f"Squad: {squad}"]
        members = sorted(squads[squad], key=lambda m: m["name"].casefold())
        if members:
            buf = io.StringIO()
            writer = csv.writer(buf, lineterminator="\n")
            writer.writerow(["Name", "Phone", "Email"])
            for m in members:
                writer.writerow(
                    [
                        m["name"],
                        format_phone_display(m["phone"]),
                        m["email"],
                    ]
                )
            lines.append(buf.getvalue().rstrip("\n"))
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks).rstrip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate per-squad contact reports from CSV input."
    )
    parser.add_argument("csv_path", help="Path to the source CSV file")
    parser.add_argument(
        "--csv",
        action="store_true",
        dest="csv_style",
        help="Emit squad blocks with CSV member rows (blank line between squads)",
    )
    args = parser.parse_args()

    squads = build_squad_report(args.csv_path)
    if args.csv_style:
        print(format_squad_report_csv(squads))
    else:
        print(format_squad_report(squads))
