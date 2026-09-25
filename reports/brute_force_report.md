# Clinic Lab Security Incident Report

## Incident
Simulated Brute-Force Login Activity

## Environment
This investigation was performed only inside the authorized clinic-lab environment.

Target:
- Application: Clinic Appointment System
- IP Address: 192.168.50.10
- Port: 8000
- Login Endpoint: /login
- Environment: VirtualBox isolated laboratory

## Detection Summary
The security log analysis identified repeated failed authentication attempts against the clinic login endpoint.

Total parsed events: 16

Failed login events: 16

Source IP:
192.168.50.10

HTTP Method:
POST

HTTP Status:
401 Unauthorized

Event:
FAILED_LOGIN

## Timeline
An initial failed login was recorded at:

2026-09-25 05:56:29

A burst of 15 additional failed login attempts occurred at approximately:

2026-09-25 06:02:44

## Detection
The Python log analysis script detected 16 failed login attempts from the same source IP.

Detection result:

ALERT: 192.168.50.10 generated 16 failed login attempts

The laboratory detection threshold was 10 failed authentication events.

## Evidence
Raw log:
logs/clinic_access.log

Parsed security events:
output/security_events.csv

Analysis script:
scripts/analyze_logs.py

## Assessment
The rapid sequence of repeated failed authentication attempts is consistent with the simulated brute-force activity intentionally generated for this laboratory exercise.

## Recommended Mitigations
- Implement login rate limiting.
- Temporarily lock accounts after repeated failed attempts.
- Monitor repeated HTTP 401 authentication failures.
- Generate alerts when failed-login thresholds are exceeded.
- Use strong authentication controls.
- Review authentication logs regularly.

## Ethical Scope
All testing was performed against the locally hosted clinic application in the authorized clinic-lab environment.

No external systems were targeted.
