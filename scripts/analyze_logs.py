import re
import csv
import sys
from collections import Counter

LOG_FILE = "logs/clinic_access.log"
OUTPUT_FILE = "output/security_events.csv"

pattern = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"IP=(?P<ip>\S+) "
    r"METHOD=(?P<method>\S+) "
    r"PATH=(?P<path>\S+) "
    r"STATUS=(?P<status>\d+) "
    r"EVENT=(?P<event>\S+)"
)

events = []

try:
    with open(LOG_FILE, "r") as log:
        for line in log:
            match = pattern.search(line)

            if match:
                events.append(match.groupdict())

except FileNotFoundError:
    print(f"ERROR: Log file not found: {LOG_FILE}")
    sys.exit(1)

except PermissionError:
    print(f"ERROR: Log file is not readable: {LOG_FILE}")
    sys.exit(1)

except OSError as error:
    print(f"ERROR: Could not read log file: {error}")
    sys.exit(1)

failed_logins = [
    event for event in events
    if event["status"] in ("401", "403")
]

ip_counts = Counter(event["ip"] for event in failed_logins)

print("=== Clinic Security Log Analysis ===")
print(f"Total events: {len(events)}")
print(f"Failed login events: {len(failed_logins)}")

print("\nFailed attempts by IP:")
for ip, count in ip_counts.items():
    print(f"{ip}: {count}")

print("\nPotential brute-force sources:")
for ip, count in ip_counts.items():
    if count >= 10:
        print(f"ALERT: {ip} generated {count} failed login attempts")

with open(OUTPUT_FILE, "w", newline="") as csvfile:
    fields = ["timestamp", "ip", "method", "path", "status", "event"]

    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(failed_logins)

print(f"\nCSV report written to: {OUTPUT_FILE}")
