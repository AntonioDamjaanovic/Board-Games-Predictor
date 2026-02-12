import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler, MultiLabelBinarizer
import numpy as np

# Load the trained model
with open("app/models_data/model_pipeline.pkl", "rb") as f:
    saved = pickle.load(f)

model = saved['model']
numeric_columns = saved['numeric_columns']
mechanics_columns = saved['mechanics_classes']
domains_columns = saved['domains_classes']

def predict_games(df):
    df = df.copy()
    
    # --- Numeric columns ---
    for col in numeric_columns:
        if col not in df.columns:
            df[col] = 0
    df_numeric = df[numeric_columns].copy()
    df_numeric = df_numeric.fillna(df_numeric.median())
    scaler = MinMaxScaler()
    df_numeric_scaled = pd.DataFrame(scaler.fit_transform(df_numeric), columns=numeric_columns, index=df.index)
    
    # --- Mechanics multi-label ---
    df['Mechanics'] = df['Mechanics'].fillna("Unknown")
    mechanics_lists = df['Mechanics'].apply(lambda x: [i.strip() for i in x.split(',')])
    mlb_mechanics = MultiLabelBinarizer(classes=[c.replace('Mechanics_', '') for c in mechanics_columns])
    df_mechanics = pd.DataFrame(mlb_mechanics.fit_transform(mechanics_lists), columns=mechanics_columns, index=df.index)
    
    # --- Domains multi-label ---
    df['Domains'] = df['Domains'].fillna("Unknown")
    domains_lists = df['Domains'].apply(lambda x: [i.strip() for i in x.split(',')])
    mlb_domains = MultiLabelBinarizer(classes=[c.replace('Domains_', '') for c in domains_columns])
    df_domains = pd.DataFrame(mlb_domains.fit_transform(domains_lists), columns=domains_columns, index=df.index)
    
    # Combine features
    X_new = pd.concat([df_numeric_scaled, df_mechanics, df_domains], axis=1)
    
    # Predict
    return model.predict(X_new).tolist()
