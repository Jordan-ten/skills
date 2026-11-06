#!/usr/bin/env python3
"""Build the scenario overview page from an overview data file.

Usage: build_overview.py <overview.json> <output.html>

Reads the data file, checks it, escapes every text value, and puts it in the
HTML template (assets/overview-template.html). Exit code 1 when the data has an
error. Warnings (for example a task that is in no parcours) go to stderr and do
not stop the build.
"""
import html
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "overview-template.html"
PRIORITIES = {"must", "should", "could"}
TAGS = {"limite", "confirmer", "decide", "ajout", "verifier"}


def check(data):
    """Return (errors, warnings) for the data."""
    errors, warnings = [], []

    pitch = data.get("pitch", {})
    for key in ("title", "artifactTitle", "summary"):
        if not pitch.get(key):
            errors.append(f"pitch.{key} is missing")
    if not data.get("issueBaseUrl"):
        errors.append("issueBaseUrl is missing")

    lot_ids = {lot.get("id") for lot in data.get("lots", [])}
    if not lot_ids:
        errors.append("lots is empty")

    task_numbers = []
    for task in data.get("tasks", []):
        number = task.get("n")
        label = f"task {number}"
        task_numbers.append(number)
        if task.get("lot") not in lot_ids:
            errors.append(f"{label}: lot {task.get('lot')!r} is not in lots")
        if task.get("p") not in PRIORITIES:
            errors.append(f"{label}: p must be one of {sorted(PRIORITIES)}")
        if not task.get("title"):
            errors.append(f"{label}: title is missing")
        if not task.get("scen"):
            errors.append(f"{label}: no scenario")
        for index, scenario in enumerate(task.get("scen", []), start=1):
            if not scenario.get("sit") or not scenario.get("res"):
                errors.append(f"{label}, scenario {index}: sit and res are both needed")
            for tag in scenario.get("tags", []):
                if tag not in TAGS:
                    errors.append(f"{label}, scenario {index}: unknown tag {tag!r}")
    if len(task_numbers) != len(set(task_numbers)):
        errors.append("task numbers are not unique")
    if not task_numbers:
        errors.append("tasks is empty")

    used_in_parcours = set()
    parcours_ids = []
    for parcours in data.get("parcours", []):
        parcours_ids.append(parcours.get("id"))
        for index, step in enumerate(parcours.get("steps", []), start=1):
            label = f"parcours {parcours.get('id')}, step {index}"
            if not step.get("sit") or not step.get("res"):
                errors.append(f"{label}: sit and res are both needed")
            if not step.get("tasks"):
                errors.append(f"{label}: tasks is empty")
            for number in step.get("tasks", []):
                used_in_parcours.add(number)
                if number not in task_numbers:
                    errors.append(f"{label}: task {number} does not exist")
    if len(parcours_ids) != len(set(parcours_ids)):
        errors.append("parcours ids are not unique")
    if not parcours_ids:
        errors.append("parcours is empty")

    for task in data.get("tasks", []):
        if task["n"] not in used_in_parcours:
            warnings.append(f"task {task['n']} is in no parcours")
        if task.get("p") == "must" and not task.get("ticket"):
            warnings.append(f"task {task['n']} is a Must with no ticket")
    return errors, warnings


def escape_strings(value):
    """Escape every string in the data, so it is safe in innerHTML and attributes."""
    if isinstance(value, str):
        return html.escape(value, quote=True)
    if isinstance(value, list):
        return [escape_strings(item) for item in value]
    if isinstance(value, dict):
        return {key: escape_strings(item) for key, item in value.items()}
    return value


def render(data):
    template = TEMPLATE.read_text(encoding="utf-8")
    safe = escape_strings(data)
    payload = json.dumps(safe, ensure_ascii=False).replace("</", "<\\/")
    title = html.escape(data["pitch"]["artifactTitle"], quote=True)
    return template.replace("__ARTIFACT_TITLE__", title).replace("__OVERVIEW_DATA__", payload)


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors, warnings = check(data)
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    Path(sys.argv[2]).write_text(render(data), encoding="utf-8")
    musts = sum(1 for task in data["tasks"] if task["p"] == "must")
    tickets = sum(1 for task in data["tasks"] if task.get("ticket"))
    print(
        f"ok: {len(data['tasks'])} tasks ({musts} Must), {tickets} with a ticket, "
        f"{len(data['parcours'])} parcours -> {sys.argv[2]}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
