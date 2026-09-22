import urllib.request
import os
os.makedirs("Clinic-Evidence", exist_ok=True)

url = "http://127.0.0.1:8000"
print(f"Fetching {url}")
data = urllib.request.urlopen(url, timeout=5).read().decode()
with open("Clinic-Evidence/home.txt", "w") as f:
    f.write(data)
print(f"Saved Clinic-Evidence/home.txt {len(data)} bytes")

# try api
try:
    api_url = "http://127.0.0.1:8000/api/patients"
    data2 = urllib.request.urlopen(api_url, timeout=5).read().decode()
    with open("Clinic-Evidence/api.txt", "w") as f:
        f.write(data2)
    print(f"Saved api.txt {len(data2)} bytes")
except Exception as e:
    print(f"API not found (ok): {e}")
