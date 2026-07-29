import requests

r = requests.post(
    'http://localhost:8002/users',
    data={'username': 'user@pardis.ac.ir', 'password': 'Demo@12345'},
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
)
tok = r.json()['access_token']
h = {'Authorization': 'Bearer ' + tok}
g = requests.get('http://localhost:8002/power-records/cal_graph4', headers=h)
print('GRAPH4:', g.status_code, g.text)
c = requests.get('http://localhost:8002/power-records/cal8', headers=h).json()
print('investment(saving, x1000 Toman):', c.get('investment'))
