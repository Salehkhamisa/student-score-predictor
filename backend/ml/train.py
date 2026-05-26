import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv('../.env')

MONGODB_URL = os.getenv('MONGODB_URL')

print('Loading dataset...')
df = pd.read_csv('data/students.csv')

print('Dataset shape:', df.shape)
print(df.head())

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print('Columns:', df.columns.tolist())

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

categorical_cols = ['gender', 'race/ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    short_name = col.replace('/', '_').replace(' ', '_')
    encoders[short_name] = le

print('Feature engineering done')

X = df[['gender', 'race/ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course', 'reading_score', 'writing_score']]
y = df['math_score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print('Training model...')
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f'R2 Score: {r2:.4f}')
print(f'MAE: {mae:.4f}')
print(f'RMSE: {rmse:.4f}')

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

print('Model and encoders saved!')

try:
    client = MongoClient(MONGODB_URL)
    db = client['studentdb']
    metrics_collection = db['metrics']
    metrics_collection.insert_one({
        'r2_score': round(r2, 4),
        'mae': round(mae, 4),
        'rmse': round(rmse, 4),
        'model_name': 'RandomForestRegressor'
    })
    print('Metrics saved to MongoDB!')
except Exception as e:
    print(f'MongoDB error (skipping): {e}')
