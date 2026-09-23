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
