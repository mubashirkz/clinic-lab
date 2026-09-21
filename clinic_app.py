import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from html import escape

DB = "clinic.db"
HOST = "0.0.0.0"
PORT = 8000

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient TEXT NOT NULL,
            doctor TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]

    if count == 0:
        test_data = [
            ("Ali Hassan", "Dr. Sara Ahmed", "2026-09-22", "09:00",
             "Routine check-up", "Confirmed"),
            ("Mariam Khan", "Dr. Omar Faisal", "2026-09-22", "10:30",
             "Follow-up consultation", "Confirmed"),
            ("John Test", "Dr. Sara Ahmed", "2026-09-23", "14:00",
             "General consultation", "Pending")
        ]

        conn.executemany("""
            INSERT INTO appointments
            (patient, doctor, appointment_date, appointment_time, reason, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, test_data)

    conn.commit()
    conn.close()

class ClinicHandler(BaseHTTPRequestHandler):

    def send_html(self, html, status=200):
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            conn = get_db()
            appointments = conn.execute(
                "SELECT * FROM appointments ORDER BY appointment_date, appointment_time"
            ).fetchall()
            conn.close()

            rows = ""

            for a in appointments:
                rows += f"""
                <tr>
                    <td>{a['id']}</td>
                    <td>{escape(a['patient'])}</td>
                    <td>{escape(a['doctor'])}</td>
                    <td>{escape(a['appointment_date'])}</td>
                    <td>{escape(a['appointment_time'])}</td>
                    <td>{escape(a['reason'])}</td>
                    <td>{escape(a['status'])}</td>
                </tr>
                """

            page = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Secure Clinic Appointment System</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 40px;
                        background: #f4f6f8;
                    }}
                    .header {{
                        background: #243447;
                        color: white;
                        padding: 25px;
                        border-radius: 8px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        background: white;
                        margin-top: 25px;
                    }}
                    th, td {{
                        padding: 12px;
                        border: 1px solid #ddd;
                        text-align: left;
                    }}
                    th {{
                        background: #e9ecef;
                    }}
                    .network {{
                        margin-top: 15px;
                        padding: 12px;
                        background: #e8f5e9;
                        border-radius: 5px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Secure Clinic Appointment System</h1>
                    <p>Isolated Cybersecurity Training Laboratory</p>
                </div>

                <div class="network">
                    <strong>Lab Network:</strong>
                    192.168.50.10 — CLINIC-LAB Internal Network
                </div>

                <h2>Appointment Records</h2>

                <table>
                    <tr>
                        <th>ID</th>
                        <th>Patient</th>
                        <th>Doctor</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Reason</th>
                        <th>Status</th>
                    </tr>
                    {rows}
                </table>
            </body>
            </html>
            """

            self.send_html(page)

        else:
            self.send_html("<h1>404 - Not Found</h1>", 404)

if __name__ == "__main__":
    init_db()
    print("Clinic Appointment System starting...")
    print(f"Listening on http://192.168.50.10:{PORT}")
    print("Press Ctrl+C to stop.")
    server = HTTPServer((HOST, PORT), ClinicHandler)
    server.serve_forever()
