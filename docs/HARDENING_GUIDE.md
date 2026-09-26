# Task 3 - Linux Host Hardening Guide

## Overview

This guide documents the security hardening performed on the Ubuntu clinic-lab host. The goal was to secure SSH access, restrict network access, disable unnecessary services, enable automatic security updates, and re-test the simulated login attack from Task 2.

## 1. SSH Hardening

OpenSSH Server was installed and enabled.

The SSH configuration was updated in:

/etc/ssh/sshd_config

The following security settings were applied:

PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no

The configuration was validated with:

sudo sshd -t

SSH was then restarted:

sudo systemctl restart ssh

The effective configuration was verified with:

sudo sshd -T | grep -E 'permitrootlogin|pubkeyauthentication|passwordauthentication'

## 2. SSH Key Authentication

An ED25519 SSH key pair was generated:

ssh-keygen -t ed25519

The public key was added to the authorized keys file:

cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys

Correct permissions were applied:

chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

Key-based authentication was tested using:

ssh vboxuser@localhost

The login completed successfully without password authentication.

## 3. Firewall Configuration

UFW was configured to deny incoming connections by default and allow outgoing connections:

sudo ufw default deny incoming
sudo ufw default allow outgoing

Only the required ports were permitted:

sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

The firewall was enabled:

sudo ufw enable

The configuration was verified using:

sudo ufw status

Only ports 22, 80 and 443 were allowed.

## 4. Disable Unnecessary Services

Unnecessary services were disabled to reduce the attack surface.

The following services were disabled:

- bluetooth.service
- cups.service
- cups-browsed.service
- avahi-daemon.service
- ModemManager.service

CUPS and Avahi triggering sockets were also disabled where applicable:

sudo systemctl disable --now cups.path cups.socket avahi-daemon.socket

The service states were checked using systemctl.

## 5. Automatic Security Updates

The unattended-upgrades package was verified and automatic security updates were enabled.

Configuration was performed using:

sudo dpkg-reconfigure -plow unattended-upgrades

The automatic-update configuration was verified in:

/etc/apt/apt.conf.d/20auto-upgrades

The configuration contained:

APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";

## 6. Re-Test the Task 2 Simulated Attack

The clinic application was started using:

python3 clinic_app_task2.py

The application listened on:

http://192.168.50.10:8000

Ten deliberately invalid login attempts were generated against the local authorized lab application.

Every attempt returned:

HTTP 401 Unauthorized

The new log entries were checked using:

tail -n 10 logs/clinic_access.log

All ten entries showed:

METHOD=POST
PATH=/login
STATUS=401
EVENT=FAILED_LOGIN

A final check confirmed that no successful login entries were produced by the ten simulated attack attempts.

## 7. Hardening Result

The Ubuntu host was hardened with:

- Root SSH login disabled
- SSH password authentication disabled
- SSH public-key authentication enabled
- UFW enabled
- Only ports 22, 80 and 443 permitted
- Unnecessary services disabled
- Automatic security updates enabled
- Simulated malicious login attempts re-tested
- No successful login entries produced during the re-test

## Ethical Scope

All security testing was performed against the locally hosted clinic application inside the authorized isolated clinic-lab environment. No external systems were targeted.
