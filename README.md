
# Clinic Lab -  Isolated Lab

Network isolated lab - no NAT gateway, proven in network-proof.txt via ip a, ip route, and ping tests showing 100% loss externally.

Clinic app runs on http://127.0.0.1:5000 with SQLite patient data. Evidence of running app and data is in Clinic-Evidence/ folder: curl-output.txt shows app response, database-data.txt shows patient rows, process.txt shows active process.

Ethical use: This lab is for authorized security testing only.




I used a VM snapshot to return to a known state; the hardest part was confirming network isolation without external traffic and fixing the sqlite db permission, I left out docker method.

All work occurs in this lab or on authorized systems.
