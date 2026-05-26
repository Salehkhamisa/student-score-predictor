import pickle

with open('ml/encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

for name, enc in encoders.items():
    print(f'{name}: {list(enc.classes_)}')
