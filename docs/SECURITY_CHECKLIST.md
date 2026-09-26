# Security Checklist

This checklist summarises the hardening completed in Task 3.
Implementation details are in [HARDENING_GUIDE.md](HARDENING_GUIDE.md).

## SSH Security
- [x] Disabled root SSH login.
- [x] Enabled public-key authentication.
- [x] Disabled password authentication.
- [x] Disabled keyboard-interactive authentication.
- [x] Tested ED25519 key-based login.
- [x] Set .ssh permissions to 700 and authorized_keys to 600.
- [x] Validated SSH configuration using sudo sshd -t.

## Firewall
- [x] Enabled UFW.
- [x] Denied incoming connections by default.
- [x] Allowed outgoing connections.
- [x] Allowed incoming TCP ports 22, 80 and 443 only.

## Unnecessary Services
- [x] Disabled Bluetooth.
- [x] Disabled CUPS and cups-browsed.
- [x] Disabled Avahi.
- [x] Disabled ModemManager.
- [x] Disabled CUPS and Avahi activation sockets where present.

## Security Updates
- [x] Enabled automatic package-list updates.
- [x] Enabled automatic upgrades using unattended-upgrades.

## Attack Re-Test
- [x] Repeated ten simulated invalid login attempts.
- [x] All ten attempts returned HTTP 401 Unauthorized.
- [x] All ten attempts were logged as FAILED_LOGIN.
- [x] No successful login events appeared in the retest.

## Scope and Limitations
Testing was performed in the authorised clinic lab.

The application's login endpoint always rejects requests.
The retest demonstrates failed requests and logging; it does
not prove that host hardening changed application authentication.

Real user authentication, login rate limiting and HTTPS
are not implemented.
