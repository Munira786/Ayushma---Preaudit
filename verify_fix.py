import requests

url = "http://127.0.0.1:8000/audit"
files = {
    "clinical_notes": ("clinical_notes.txt", b"Burn 35% TBSA", "text/plain"),
    "discharge_summary": ("discharge.txt", b"Summary", "text/plain"),
    "photographs": ("photo.txt", b"Photo placeholder", "text/plain"),
    "hospital_bill": ("bill.txt", b"Total: 38500, Code: BM001B", "text/plain")
}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
