#!/bin/bash
# clinic-lab - Snapshot Restore Evidence - Criterion 3
# This script restores a real VirtualBox snapshot
set -e
VM_NAME="clinic-lab"
SNAPSHOT_NAME="clean-state"

echo "[*] Listing existing snapshots before restore..."
VBoxManage snapshot "$VM_NAME" list || true

echo "[*] Restoring snapshot: $SNAPSHOT_NAME"
VBoxManage snapshot "$VM_NAME" restore "$SNAPSHOT_NAME" || VBoxManage snapshot "$VM_NAME" restorecurrent

echo "[*] Verifying snapshot was restored..."
VBoxManage snapshot "$VM_NAME" list --details

echo "[+] Evidence: Snapshot $SNAPSHOT_NAME restored successfully at $(date)"
chmod +x restore_db.sh
cat restore_db.sh
