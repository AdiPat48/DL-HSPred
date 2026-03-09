"""
Deep Learning Hotspot Prediction Model 

Defines and trains the primary Multi-Layer Perceptron (MLP) for sequence-only 
PPI hotspot prediction.

Architecture:
- Input: 1562-dimensional ProteinBERT residue embeddings.
- Hidden Layers: 5 Dense layers (1024 -> 512 -> 256 -> 64 -> 32) with GELU activation.
- Regularization: Dropout (0.3) applied after each hidden layer.
- Output: Single unit with Sigmoid activation for binary classification.

Evaluation:
- Performs training on the primary dataset with stratified splitting.
- Validates final model performance using an independent test set (BID 2018 dataset).
- Reports metrics: F1 Score, Precision, Recall, and Matthews Correlation Coefficient (MCC).
"""

import tensorflow as tf
import random
from tensorflow import keras
from keras.layers import BatchNormalization, LayerNormalization, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.optimizers import Adam as adam
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.metrics import classification_report, f1_score, matthews_corrcoef
from sklearn.metrics import precision_recall_curve, auc, average_precision_score



# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)



# Load and preprocess your data (as you've done before)
scaler = StandardScaler()
df = pd.read_csv('embedded_input.csv')
nonzero_reduced_matrix = df.iloc[:, 1:-1]
updated_labels = df.iloc[:, -1]

input_data = scaler.fit_transform(np.array(nonzero_reduced_matrix))
input_labels = np.array(updated_labels)

# Split the data into training and testing sets with stratification
X_train, X_test, y_train, y_test = train_test_split(input_data, input_labels, test_size=0.2, random_state=42, stratify=input_labels)

# Create a Sequential model
model = keras.Sequential()

# Add input layer with the appropriate input shape
model.add(keras.layers.Input(shape=(X_train.shape[1],))) #1562

# Add hidden layers with BatchNormalization, LayerNormalization, l2 regularization, and Dropout
model.add(keras.layers.Dense(1024, activation='gelu'))

model.add(Dropout(0.3,seed=42))  # Add dropout with a dropout rate of 0.3
model.add(keras.layers.Dense(512, activation='gelu'))

model.add(Dropout(0.3,seed=42))
model.add(keras.layers.Dense(256, activation='gelu'))

model.add(Dropout(0.3,seed=42))
model.add(keras.layers.Dense(64, activation='gelu'))

model.add(Dropout(0.3,seed=42))
model.add(keras.layers.Dense(32, activation='gelu'))

model.add(Dropout(0.3,seed=42))

# Add the output layer with 1 unit (binary classification) and sigmoid activation function
model.add(keras.layers.Dense(1, activation='sigmoid'))

# Compile the model with the F1 score as the evaluation metric
model.compile(optimizer=adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()])

# Print the model summary
model.summary()

# Define a custom callback to print metrics during training
class PrintMetricsCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"Epoch {epoch + 1}/{self.params['epochs']} - loss: {logs['loss']:.4f} - acc: {logs['accuracy']:.4f} - precision: {logs['precision']:.4f} - recall: {logs['recall']:.4f} - val_loss: {logs['val_loss']:.4f} - val_acc: {logs['val_accuracy']:.4f} - val_precision: {logs['val_precision']:.4f} - val_recall: {logs['val_recall']:.4f}")

# Train the model on your training data with the custom callback
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=0, callbacks=[PrintMetricsCallback()])

# Predict probabilities on the test data
# y_pred_prob = model.predict(X_test)

# # Calculate the Precision-Recall curve
# precision, recall, thresholds = precision_recall_curve(y_test, y_pred_prob)

# # Calculate the area under the PR curve (AUC)
# pr_auc = auc(recall, precision)

# # Plot the PR curve
# plt.figure(figsize=(8, 6))
# plt.plot(recall, precision, color='darkorange', lw=2, label='PR curve (area = %0.2f)' % pr_auc)
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('Recall')
# plt.ylabel('Precision')
# plt.title('Precision-Recall Curve (PR)')
# plt.legend(loc='lower left')

# # Find the optimal threshold based on PR curve (F1 score maximization)
# f1_scores = 2 * (precision * recall) / (precision + recall)
# optimal_idx = np.argmax(f1_scores)
# optimal_threshold = thresholds[optimal_idx]

# # Print the optimal threshold
# print("Optimal Threshold (F1 score maximization):", optimal_threshold)

# # Optional: Calculate and print the average precision score
# average_precision = average_precision_score(y_test, y_pred_prob)
# print("Average Precision:", average_precision)

# # Show the plot
# plt.show()

# # Show the plot
# plt.savefig('PR_curve.png')










# Predict on the test data
y_pred = (model.predict(X_test) > 0.5).astype(int)

# Calculate the F1 score, precision, and recall
f1 = f1_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print (" **************************************************** " )
print(f"F1 Score: {f1 * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print (" **************************************************** \n\n" )

"""   
Test the classifier on the BID  dataset for the final evaluation
    
"""  
print (" **************************************************** " )
print (" Performance on BID dataset:")
print (" **************************************************** \n" )
bid_data = pd.read_csv('embedded_BID_hotspots_nonhotspots_dataset.csv')
test_data = scaler.transform(np.array(bid_data.iloc[:, 1:-1]))
test_labels = np.array(bid_data.iloc[:, -1])
predictions = (model.predict(test_data) > 0.5).astype(int)
f1score = f1_score(test_labels, predictions)
mcc = matthews_corrcoef(test_labels, predictions)

print(f"Test F1-score: {f1score}")
print(f"Test MCC: {mcc}")
print (" **************************************************** \n" )
report = classification_report(test_labels, predictions)
print(f"Classification Report:\n{report}")

print (" **************************************************** " )

