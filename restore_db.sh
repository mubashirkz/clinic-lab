#!/bin/bash
echo "Restoring Clinic DB snapshot..."
sqlite3 clinic.db "CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, name TEXT);"
