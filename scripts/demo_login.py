import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import (
    Request, build_opener, HTTPRedirectHandler, ProxyHandler
)

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "logs/clinic_access.log"
URL = "http://192.168.50.10:8000/login"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    start = LOG.stat().st_size if LOG.exists() else 0
    opener = build_opener(ProxyHandler({}), NoRedirect())
    statuses = []

    print("Clinic lab: after-hardening login demonstration")
    print("Testing ten dummy invalid login attempts.\n")

    for attempt in range(1, 11):
        data = urlencode({
            "username": "demo-" + secrets.token_hex(6),
            "password": secrets.token_urlsafe(24)
        }).encode()

        request = Request(
            URL,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            method="POST"
        )

        try:
            with opener.open(request, timeout=5) as response:
                status = response.status
        except HTTPError as error:
            status = error.code
            error.close()
        except (URLError, OSError):
            status = None

        statuses.append(status)
        print(f"Attempt {attempt}: HTTP {status or 'CONNECTION ERROR'}")

    new_lines = []
    if LOG.exists() and LOG.stat().st_size >= start:
        with LOG.open("rb") as stream:
            stream.seek(start)
            new_lines = stream.read().decode(
                "utf-8", errors="replace"
            ).splitlines()

    failures = [
        line for line in new_lines
        if "METHOD=POST PATH=/login STATUS=401 EVENT=FAILED_LOGIN"
        in line
    ]

    passed = (
        statuses == [401] * 10
        and len(failures) == 10
        and len(new_lines) == 10
    )

    timestamp = datetime.now(timezone.utc)
    result = {
        "time_utc": timestamp.isoformat(),
        "phase": "after hardening",
        "target": URL,
        "http_statuses": statuses,
        "new_log_entries": new_lines,
        "passed": passed,
        "limitation": (
            "The login endpoint always rejects requests. "
            "This test verifies responses and logging, "
            "not a change in authentication or host settings."
        )
    }

    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    filename = output / (
        "demo-after-"
        + timestamp.strftime("%Y%m%dT%H%M%S%fZ")
        + ".json"
    )
    filename.write_text(json.dumps(result, indent=2) + "\n")

    print(f"\nNew failed-login records: {len(failures)}")
    print("PASS" if passed else "FAIL - review responses and logs")
    print(f"Evidence saved to: {filename}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
