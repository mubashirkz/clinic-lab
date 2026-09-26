# Before-and-After Security Demo

## Purpose

Demonstrate simulated invalid login attempts and their logs
before and after Linux host hardening in the authorised lab.

## Before Hardening: Task 2

The original log records from 2026-09-25 contain 16 failed
login attempts returning HTTP 401.

Evidence:
- [Task 2 findings](../reports/findings.md)
- [Incident report](../reports/brute_force_report.md)
- [Security logs](../logs/clinic_access.log)

## After Hardening: Tasks 3 and 4

Task 3 applied SSH restrictions, enabled UFW, disabled
unnecessary services and enabled automatic security updates.

The Task 3 retest recorded ten failed login attempts on
2026-09-26 at 04:21:43 in the application log.

The Task 4 demo was also executed successfully:
- Ten requests returned HTTP 401.
- Ten new FAILED_LOGIN records were verified.
- The script reported PASS.
- A timestamped JSON evidence file was saved in output/.

Evidence:
- [Hardening guide](HARDENING_GUIDE.md)
- [Security checklist](SECURITY_CHECKLIST.md)
- [Demo script](../scripts/demo_login.py)
- [Saved results](../output/)

## Repeat the Demo

Run these commands inside the Ubuntu VM.

Terminal 1:

```bash
cd ~/clinic-lab
python3 clinic_app_task2.py
```

Leave the application running.

Terminal 2:

```bash
cd ~/clinic-lab
python3 scripts/demo_login.py
```

Expected result:

```text
Attempt 1: HTTP 401
...
Attempt 10: HTTP 401
New failed-login records: 10
PASS
Evidence saved to: .../output/demo-after-<timestamp>.json
```

The script generates dummy credentials for each request.
It does not save the submitted passwords.

Each run appends ten events to the application log and creates
a new JSON result. Avoid other login requests during the demo
because the script checks exactly ten new log records.

A connection error is a failed test, not proof of a rejected login.

## Short Presentation Script

1. Show the Task 2 findings and original failed-login records.
2. Explain the host controls listed in the hardening guide.
3. Run the Task 4 demo.
4. Show the ten HTTP 401 responses and PASS result.
5. Open the generated JSON file to show the saved evidence.
6. Explain the limitation below.

## Interpretation and Limitations

The application rejects every login request by design.
Both the before and after tests therefore return HTTP 401.

This demonstrates repeatable failed-login behaviour and logging
after host hardening. It does not prove that hardening changed
web authentication or implemented brute-force prevention.

SSH and firewall controls are documented separately in the
hardening guide. Real staff authentication, rate limiting,
account lockout and HTTPS remain outside this lab implementation.
