## Criterion 1: Network Isolation Proof - Lab You Are Allowed To Break

All work occurs in this lab or on authorized systems.

**Network Configuration:**
- VM Host-Only Adapter: enp0s3 = 192.168.50.10/24 (Host-Only network vboxnet0)
- Subnet Mask: 255.255.255.0 (/24)
- Default Gateway: NONE on 192.168.50.0/24 - No route to internet
- NAT Adapter (management only): enp0s8 = 10.0.3.15/24, gateway 10.0.3.2 for git push only

**IP Route Proof (real output from `ip route show`):**


**Firewall / Binding Rules:**
- clinic_app.py: HOST = "192.168.50.10" (binds ONLY to Host-Only, not 0.0.0.0)
- PORT = 8000
- Traffic on 192.168.50.10 stays VM <-> Host only, cannot leave lab
- No default gateway on Host-Only subnet proves isolation
- Commands: `ip route`, `ip route show`, `ip addr`
default via 10.0.3.2 dev enp0s8 proto dhcp src 10.0.3.15 metric 100
10.0.3.0/24 dev enp0s8 proto kernel scope link src 10.0.3.15 metric 100
192.168.50.0/24 dev enp0s3 proto kernel scope link src 192.168.50.10 metric 101

Ethical use: This lab is for authorized security testing only.

I used a VM snapshot to return to a known state; the hardest part was confirming network isolation without external traffic and fixing the sqlite db permission, I left out docker method.

All work occurs in this lab or on authorized systems.

## Task 2 - Suspicious Application Log Analysis

This task simulates failed login attempts against the locally hosted clinic application and analyzes the generated security logs.

### Run the Analysis

From the clinic-lab directory, run:

python3 scripts/analyze_logs.py

The script reads:

logs/clinic_access.log

and creates:

output/security_events.csv

### Interpreting the Output

The script identifies HTTP 401 and 403 authentication failures, extracts the source IP address and timestamp, and counts failed login attempts by IP.

A source IP with 10 or more failed login attempts is flagged as potential brute-force activity.

During this lab, 192.168.50.10 generated 16 failed login attempts and was flagged as a potential brute-force source.

The detailed findings are stored in:

reports/findings.md

### Error Handling

The script handles missing, unreadable, and other inaccessible log-file errors and exits with an error message instead of crashing unexpectedly.

### Ethical Scope

All testing was performed against the locally hosted clinic application inside the authorized isolated clinic-lab environment. No external systems were targeted.


## Task 3 - Linux Host Hardening

This task hardens the clinic-lab Ubuntu host and verifies that simulated malicious login attempts do not result in successful authentication.

### SSH Hardening

The OpenSSH server was configured with:

- PermitRootLogin no
- PubkeyAuthentication yes
- PasswordAuthentication no
- KbdInteractiveAuthentication no

SSH key-based authentication was tested successfully using an ED25519 key.

### Firewall Hardening

UFW was enabled with a default deny policy for incoming traffic.

Only the following required ports are allowed:

- 22/tcp - SSH
- 80/tcp - HTTP
- 443/tcp - HTTPS

### Disabled Unnecessary Services

The following unnecessary services were disabled:

- bluetooth.service
- cups.service
- cups-browsed.service
- avahi-daemon.service
- ModemManager.service

CUPS and Avahi triggering sockets were also disabled where applicable.

### Automatic Security Updates

Automatic security updates were enabled using unattended-upgrades.

The configuration enables daily package-list updates and unattended upgrades.

### Attack Re-Test

The simulated failed-login attack from Task 2 was repeated after hardening.

Ten login attempts were sent to the local clinic application. All ten attempts returned HTTP 401 Unauthorized and were recorded as EVENT=FAILED_LOGIN.

No successful login entries were found in the ten attack attempts.

### Result

The host was hardened by restricting SSH authentication, enabling UFW, disabling unnecessary services, and enabling automatic security updates. The repeated login simulation produced no successful authentication entries.

### Ethical Scope

All testing was performed against the locally hosted clinic application inside the authorized isolated clinic-lab environment.
