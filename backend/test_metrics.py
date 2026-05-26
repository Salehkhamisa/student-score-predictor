import requests

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYWxlaCIsImV4cCI6MTc3OTc4MzA5M30.-7-MvV9-G-EQavm-kd6-QplxObL1FRuNfFeUs_tPI28'
headers = {'Authorization': 'Bearer ' + token}
r = requests.get('http://127.0.0.1:8000/api/metrics', headers=headers)
print(r.status_code, r.json())
