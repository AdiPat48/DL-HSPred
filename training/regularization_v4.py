"""
Hyperparameter Grid Search and Regularization Benchmarking

A systematic exploration of the model's hyperparameter space to optimize 
classification performance and prevent overfitting.

Tested Parameters:
- Regularization Types: L1, L2, and None.
- Regularization Strengths: [0.01, 0.05, 0.1].
- Dropout Rates: [0.0, 0.3, 0.5].
- Learning Rates: [0.1, 0.01, 0.001].

The script logs the results of every combination and generates a 
Recall vs. F1-Score visualization to identify the optimal training configuration.
"""

import tensorflow as tf
from tensorflow import keras
from keras.layers import BatchNormalization, LayerNormalization, Dropout
from keras.optimizers import Adam as adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score
import matplotlib.pyplot as plt


#OUTPUT
with open('regularization_v4.log','w') as f:
	f.writelines("regularization_type,strength,dropout_rate,learning_rate,last_epoch log, f1 score,precision,recall\n")

# Load and preprocess your data 
scaler = StandardScaler()
df = pd.read_csv('embedded_input.csv')
nonzero_reduced_matrix = df.iloc[:, 1:-1]
updated_labels = df.iloc[:, -1]

input_data = scaler.fit_transform(np.array(nonzero_reduced_matrix))
input_labels = np.array(updated_labels)

# Split the data into training and testing sets with stratification
X_train, X_test, y_train, y_test = train_test_split(input_data, input_labels, test_size=0.2, random_state=42, stratify=input_labels)

# Define hyperparameter values to search over
regularization_types = ['l1', 'l2', 'none']
dropout_rates = [0.0, 0.3, 0.5]
l1_l2_strengths = [0.01, 0.05, 0.1]
learning_rates=[0.1, 0.01, 0.001]


results = []


# Define a custom callback to print metrics during training
class PrintMetricsCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"Epoch {epoch + 1}/{self.params['epochs']} - loss: {logs['loss']:.4f} - acc: {logs['accuracy']:.4f} - precision: {logs['precision']:.4f} - recall: {logs['recall']:.4f} - val_loss: {logs['val_loss']:.4f} - val_acc: {logs['val_accuracy']:.4f} - val_precision: {logs['val_precision']:.4f} - val_recall: {logs['val_recall']:.4f}")
        if epoch==(self.params['epochs']-1):
        	with open('regularization_v4.log','a') as f:
            		f.writelines(f"{log_str},")
        	

# Create an empty list to store results
results_list = []

for reg_type in regularization_types:
    for strength in l1_l2_strengths:
        for dropout_rate in dropout_rates:
            for learning_rate in learning_rates:
                with open('regularization_v4.log','a') as f:
                    f.writelines(f"{reg_type},{strength},{dropout_rate},{learning_rate},")

                if reg_type=='none':
                    strength=0.0


                # Create a Sequential model
                model = keras.Sequential()
                
                # Add input layer with the appropriate input shape
                model.add(keras.layers.Input(shape=(X_train.shape[1],))) #1562
                
                # Add hidden layers based on regularization type
                if reg_type=='l1':
                    kernel_regularizer=keras.regularizers.l1(strength)
                elif reg_type=='l2':
                    kernel_regularizer=keras.regularizers.l2(strength)


                # Add layers with L1 regularization
                model.add(keras.layers.Dense(1024, activation='gelu', kernel_regularizer=kernel_regularizer))
                model.add(BatchNormalization())
                model.add(LayerNormalization())
                model.add(Dropout(dropout_rate))
                model.add(keras.layers.Dense(512, activation='gelu', kernel_regularizer=kernel_regularizer))
                model.add(BatchNormalization())
                model.add(LayerNormalization())
                model.add(Dropout(dropout_rate))
                model.add(keras.layers.Dense(256, activation='gelu', kernel_regularizer=kernel_regularizer))
                model.add(BatchNormalization())
                model.add(LayerNormalization())
                model.add(Dropout(dropout_rate))
                model.add(keras.layers.Dense(64, activation='gelu', kernel_regularizer=kernel_regularizer))
                model.add(BatchNormalization())
                model.add(LayerNormalization())
                model.add(Dropout(dropout_rate))
                model.add(keras.layers.Dense(32, activation='gelu', kernel_regularizer=kernel_regularizer))
                model.add(BatchNormalization())
                model.add(LayerNormalization())
                model.add(Dropout(dropout_rate))
                
                # Add the output layer with 1 unit (binary classification) and sigmoid activation function
                model.add(keras.layers.Dense(1, activation='sigmoid'))
                
                # Compile the model with the F1 score as the evaluation metric
                model.compile(optimizer=adam(learning_rate=learning_rate), loss='binary_crossentropy', metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()])
                
                # Print the model summary
                model.summary()
                
                # Train the model on your training data with the custom callback
                history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=0, callbacks=[PrintMetricsCallback()])
                

                # Predict on the test data
                y_pred = (model.predict(X_test) > 0.5).astype(int)
                
                # Calculate precision, recall, and F1 score
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)
                
                with open('regularization_v4.log','a') as f:
                    f.writelines(f"{f1},{precision},{recall}\n")
                    
                # Append results to the list
                results_list.append({
                    'Regularization': reg_type,
                    'Strength': strength,
                    'Dropout Rate': dropout_rate,
                    'Learning Rate': learning_rate,
                    'Precision': precision,
                    'Recall': recall,
                    'F1 Score': f1
                })                    
                                    

# Create dataframes for results
results_df = pd.DataFrame(results_list)

# Set pandas option to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Print the entire dataframe
print(results_df)

# Reset pandas options to their default values (if needed)
# pd.reset_option('display.max_rows')
# pd.reset_option('display.max_columns')


# Visualize the results

# Create a figure for the combined plot
plt.figure(figsize=(20, 10))


# Iterate through different combinations of hyperparameters
for reg_type in regularization_types:
    for dropout_rate in dropout_rates:
        for strength in l1_l2_strengths:
            for learning_rate in learning_rates:
                subset = results_df[(results_df['Regularization'] == reg_type) & 
                                    (results_df['Dropout Rate'] == dropout_rate) & 
                                    (results_df['Strength'] == strength) &
                                    (results_df['Learning Rate'] == learning_rate)]
                
                if not subset.empty:
                    # Extract F1 Score and Recall values
                    f1_scores = subset['F1 Score'].values
                    recalls = subset['Recall'].values

                    # Plot F1 Score vs. Recall for the current combination
                    label = f'{reg_type} - Strength: {strength} - Dropout Rate: {dropout_rate} - Learning Rate: {learning_rate}'
                    plt.plot(recalls, f1_scores, marker='o', label=label)

# Add labels, title, legend, and grid
plt.xlabel('Recall')
plt.ylabel('F1 Score')
plt.title('F1 Score vs. Recall for Different Hyperparameter Combinations')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Show the combined plot
plt.show()
