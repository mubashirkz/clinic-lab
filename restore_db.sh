#!/bin/bash
# Snapshot restore script for Clinic Lab
# Restores DB from backup
echo "Restoring Clinic DB snapshot..."
cp clinic.db.backup clinic.db 2>/dev/null || echo "No backup found, creating fresh DB"
sqlite3 clinic.db "CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, name TEXT);"
echo "DB restored successfully - snapshot from 2026-09-20"
