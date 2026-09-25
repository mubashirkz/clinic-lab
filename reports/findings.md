# Clinic Security Incident Findings

## Summary
A simulated brute-force login attack was performed against the locally hosted clinic application.

## Detection
The log analysis identified 16 failed login attempts.

## Top Suspicious IP Addresses

1. 192.168.50.10
   - Failed attempts: 16
   - Timestamp: 2026-09-25 05:56:29 to 2026-09-25 06:02:44
   - HTTP Status: 401
   - Attack Type: Simulated brute-force login attack

Only one source IP was observed during this laboratory simulation, so there are no additional malicious IP addresses to report.

## Evidence
Raw log:
logs/clinic_access.log

Parsed CSV:
output/security_events.csv

Analysis script:
scripts/analyze_logs.py

## Conclusion
The repeated HTTP 401 authentication failures from 192.168.50.10 are consistent with the simulated brute-force activity performed in the isolated laboratory environment.
