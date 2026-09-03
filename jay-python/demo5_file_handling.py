# Jay - Demo 5: File Handling with JSON and CSV

import csv
import json
import os
import tempfile

STUDENTS = [
    {"name": "Jay", "subject": "Python", "score": 92},
    {"name": "Riya", "subject": "Python", "score": 85},
    {"name": "Amit", "subject": "Python", "score": 78},
    {"name": "Neha", "subject": "Python", "score": 96},
]


def write_json(path, records):
    """Write `records` to `path` as formatted JSON."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def read_json(path):
    """Read records back from the JSON file at `path`."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_csv(path, records):
    """Write `records` to `path` as CSV with a header row."""
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)


def read_csv(path):
    """Read rows back from the CSV file at `path`."""
    with open(path, "r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def summarize(records):
    """Return simple statistics for the student scores."""
    scores = [int(record["score"]) for record in records]
    return {
        "count": len(scores),
        "highest": max(scores),
        "lowest": min(scores),
        "average": round(sum(scores) / len(scores), 2),
    }


def main():
    print("=" * 40)
    print("  Jay - Demo 5: File Handling")
    print("=" * 40)

    work_dir = tempfile.mkdtemp(prefix="jay_demo_")
    json_path = os.path.join(work_dir, "students.json")
    csv_path = os.path.join(work_dir, "students.csv")

    write_json(json_path, STUDENTS)
    write_csv(csv_path, STUDENTS)
    print(f"Files created in: {work_dir}")

    json_records = read_json(json_path)
    csv_records = read_csv(csv_path)
    print(f"Records read from JSON: {len(json_records)}")
    print(f"Records read from CSV : {len(csv_records)}")

    print("\nStudent scores:")
    for record in sorted(json_records, key=lambda item: item["score"], reverse=True):
        print(f"  {record['name']:<8} {record['subject']:<8} {record['score']:>3}")

    print("\nSummary:")
    for key, value in summarize(csv_records).items():
        print(f"  {key:<8}: {value}")

    for path in (json_path, csv_path):
        os.remove(path)
    os.rmdir(work_dir)
    print(f"\nCleaned up temporary files in {work_dir}")


if __name__ == "__main__":
    main()
