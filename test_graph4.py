import os

import requests

backend_url = os.getenv('BACKEND_URL', 'http://localhost:8002').rstrip('/')
email = os.getenv('TEST_EMAIL')
password = os.getenv('TEST_PASSWORD')
if not email or not password:
    raise SystemExit('Set TEST_EMAIL and TEST_PASSWORD before running this smoke test.')

r = requests.post(
    f'{backend_url}/users',
    data={'username': email, 'password': password},
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
)
tok = r.json()['access_token']
h = {'Authorization': 'Bearer ' + tok}
g = requests.get('http://localhost:8002/power-records/cal_graph4', headers=h)
print('GRAPH4:', g.status_code, g.text)
c = requests.get('http://localhost:8002/power-records/cal8', headers=h).json()
print('investment(saving, x1000 Toman):', c.get('investment'))
