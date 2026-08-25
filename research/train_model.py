import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Configuration
input_file = "synthetic_training_data.csv"
model_file = "alzheimer_rf_model.pkl"

def train_model():
    print("Loading training data...")
    df = pd.read_csv(input_file)
    
    # Features & Target
    X = df[['Age', 'Sex', 'FamilyHistory', 'rs429358', 'rs7412', 'rs3851179']]
    y = df['Diagnosis']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy on Test Set: {acc:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature Importance
    print("\nFeature Importances:")
    for name, score in zip(X.columns, rf.feature_importances_):
        print(f"  {name}: {score:.4f}")
        
    # Save Model
    with open(model_file, 'wb') as f:
        pickle.dump(rf, f)
    print(f"\nModel saved to {model_file}")

if __name__ == "__main__":
    train_model()
