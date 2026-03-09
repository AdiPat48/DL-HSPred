"""
Comparative Analysis of Machine Learning Classifiers

Benchmarks 10 different machine learning algorithms against the custom Neural Network 
to establish a performance baseline for PPI hotspot prediction.

Algorithms Evaluated:
Random Forest, Gradient Boosting, SVM, Logistic Regression, KNN, 
Decision Trees, Naive Bayes, MLP (sklearn), AdaBoost, and XGBoost.

Methodology:
- Uses 10-fold Stratified Cross-Validation for robust performance estimation.
- Evaluates models on the independent BID dataset.
- Tracks Mean F1-Score and Mean MCC across all folds.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, f1_score, matthews_corrcoef

# Load and preprocess your data (as you've done before)
scaler = StandardScaler()
df = pd.read_csv('embedded_input.csv')
nonzero_reduced_matrix = df.iloc[:, 1:-1]
updated_labels = df.iloc[:, -1]

input_data = scaler.fit_transform(np.array(nonzero_reduced_matrix))
input_labels = np.array(updated_labels)


# Initialize and evaluate multiple classifiers with 10-fold cross-validation
classifiers = {
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, class_weight='balanced', random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42),
    'SVM': SVC(kernel='linear', class_weight='balanced', random_state=42),
    'Logistic Regression': LogisticRegression(class_weight='balanced', random_state=42),
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
    'Decision Tree': DecisionTreeClassifier(max_depth=5, class_weight='balanced', random_state=42),
    'Naive Bayes': GaussianNB(),
    'MLP Neural Network': MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42),
    'AdaBoost': AdaBoostClassifier(n_estimators=50, random_state=42),
    'XGBoost': XGBClassifier(objective='binary:logistic', scale_pos_weight=np.sum(input_labels == 0) / np.sum(input_labels == 1), random_state=42),
}

# Perform 10-fold cross-validation with F1-score and MCC, and print results for each classifier
for clf_name, clf in classifiers.items():
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)  # 10-fold cross-validation
    f1_scores = cross_val_score(clf, input_data, input_labels, cv=cv, scoring='f1')  # Using F1-score
    mcc_scores = cross_val_score(clf, input_data, input_labels, cv=cv, scoring='matthews_corrcoef')  # Using MCC
    
    print(f"{clf_name} Cross-Validation F1-scores: {f1_scores}")
    print(f"{clf_name} Mean CV F1-score: {f1_scores.mean()}")
    
    print(f"{clf_name} Cross-Validation MCC: {mcc_scores}")
    print(f"{clf_name} Mean CV MCC: {mcc_scores.mean()}")
    
    print("-" * 50)
    
    
    clf.fit(input_data, input_labels)
    
    """   
    Test the classifier on the BID  dataset for the final evaluation
        
    """  
    print (" **************************************************** " )
    print (" Performance on BID dataset:")
    print (" **************************************************** " )
    bid_data = pd.read_csv('embedded_BID_hotspots_nonhotspots_dataset.csv')
    test_data = scaler.transform(np.array(bid_data.iloc[:, 1:-1]))
    test_labels = np.array(bid_data.iloc[:, -1])
    predictions = clf.predict(test_data)
    f1score = f1_score(test_labels, predictions)
    mcc = matthews_corrcoef(test_labels, predictions)

    print(f"{clf_name} Test F1-score: {f1score}")
    print(f"{clf_name} Test MCC: {mcc}")

    report = classification_report(test_labels, predictions)
    print(f"{clf_name} Classification Report:\n{report}")
    print("-" * 50)
    
    print (" **************************************************** " )
