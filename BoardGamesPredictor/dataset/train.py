import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, MultiLabelBinarizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
import pickle
import numpy as np

# Load dataset
df = pd.read_csv("dataset/BGG_Data_Set.csv", encoding="latin1")

# Drop columns we truly don't need
df = df.drop(columns=["ID", "Name", "BGG Rank"])

# Separate features and target
X = df.drop(columns=["Rating Average"])
y = df["Rating Average"]

# Identify numeric columns
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns

# Columns to handle as multi-label text
multilabel_cols = ['Mechanics', 'Domains']

# Preprocessing for numeric columns
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', MinMaxScaler())
])

# Preprocessing for multi-label text columns
def multilabel_transformer(df, column_name):
    """Return a DataFrame with multi-label binarized columns"""
    df_col = df[column_name].fillna("Unknown").apply(lambda x: [i.strip() for i in x.split(',')])
    mlb = MultiLabelBinarizer()
    return pd.DataFrame(mlb.fit_transform(df_col), columns=[f"{column_name}_{c}" for c in mlb.classes_], index=df.index)

# Apply multi-label encoding
X_mechanics = multilabel_transformer(X, 'Mechanics')
X_domains = multilabel_transformer(X, 'Domains')

# Drop original multi-label columns
X_numeric = X.drop(columns=multilabel_cols)

# Scale numeric features
X_numeric[numeric_cols] = numeric_transformer.fit_transform(X_numeric[numeric_cols])

# Combine all features
X_processed = pd.concat([X_numeric, X_mechanics, X_domains], axis=1)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, test_size=0.3, random_state=42
)

# Train model
model = GradientBoostingRegressor(
    learning_rate=0.05,
    n_estimators=500,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(np.mean((y_test - y_pred)**2))
mae = np.mean(np.abs(y_test - y_pred))
r2 = r2_score(y_test, y_pred)
rae = np.sum(np.abs(y_test - y_pred)) / np.sum(np.abs(y_test - np.mean(y_test)))

print(f"RMSE: {rmse}")
print(f"MAE: {mae}")
print(f"R²: {r2}")
print(f"RAE: {rae}")

# Save the trained model
with open("model_pipeline.pkl", "wb") as f:
    pickle.dump({
        'model': model,
        'numeric_columns': numeric_cols.tolist(),
        'mechanics_classes': X_mechanics.columns.tolist(),
        'domains_classes': X_domains.columns.tolist()
    }, f)

print("Model trained and saved as model_pipeline.pkl")
