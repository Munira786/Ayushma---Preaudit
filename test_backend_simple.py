import subprocess
import time
import sys
import requests
import os

os.chdir(r'c:\Users\marry\OneDrive\Desktop\Ayushma')

# Start server with output visible for debugging
print('Starting backend server...')
server = subprocess.Popen(
    [sys.executable, 'run_backend.py'],
    cwd=r'c:\Users\marry\OneDrive\Desktop\Ayushma'
)

# Wait for it to start
print('Waiting for backend to initialize...')
time.sleep(5)

# Test it
try:
    print('Testing backend...')
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
    print('\n✅ Backend is working correctly!')
except Exception as e:
    print('❌ Error:', str(e))
finally:
    print('\nStopping backend...')
    server.terminate()
    try:
        server.wait(timeout=3)
    except:
        server.kill()
