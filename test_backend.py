import subprocess
import time
import sys
import requests

# Start server
print('Starting backend server...')
server = subprocess.Popen([sys.executable, 'run_backend.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for it to start
time.sleep(3)

# Test it
try:
    response = requests.post('http://127.0.0.1:8000/audit', files={
        'clinical_notes': ('test.txt', b'burn 35 TBSA major injury', 'text/plain'),
        'hospital_bill': ('bill.txt', b'Total: 50000, Code: BM001B', 'text/plain')
    }, timeout=5)
    print('✅ Backend is responding!')
    print('Status Code:', response.status_code)
    result = response.json()
    print('Predicted Package:', result.get('predicted_package'))
    severity = result.get('severity_detected')
    print('Severity:', str(severity) + '%')
    claimed = result.get('claimed_amount')
    print('Claimed Amount: ₹' + str(claimed))
    status = result.get('validation', {}).get('status')
    print('Validation Status:', status)
except Exception as e:
    print('❌ Error:', str(e))
finally:
    server.terminate()
    server.wait()
