import requests

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYWxlaCIsImV4cCI6MTc3OTc4MzA5M30.-7-MvV9-G-EQavm-kd6-QplxObL1FRuNfFeUs_tPI28'
headers = {'Authorization': 'Bearer ' + token}
data = {
    'gender': 'male',
    'race_ethnicity': 'group C',
    'parental_level_of_education': 'some college',
    'lunch': 'standard',
    'test_preparation_course': 'none',
    'reading_score': 70,
    'writing_score': 68
}
r = requests.post('http://127.0.0.1:8000/api/predict', json=data, headers=headers)
print(r.status_code, r.json())
