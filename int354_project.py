# -*- coding: utf-8 -*-
"""int354 project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cvzy9-iIQPp3FtLjWwzhGnPxRYlKO39A

Import libraries
"""

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

"""Load the dataset"""

dataset = pd.read_csv("/content/qsar_fish_toxicity.csv")
dataset.head(10)

"""Data Summarization and Visualization"""

dataset.info()

"""Generate the descriptive statistics of the dataset"""

dataset.describe()

"""Calculate the correlation of each columns with the LC50"""

dataset.corr(method="pearson")

"""Show the histogram plot of each variables"""

dataset.hist(figsize=(20, 20), layout=(4, 4));

"""Data Preparation

Split the target and features in the dataset
"""

X = dataset.drop(["LC50 [-LOG(mol/L)]"], axis=1)
y = pd.DataFrame(dataset["LC50 [-LOG(mol/L)]"].copy())

"""Split the dataset into training and testing set"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42)

"""Define the scaler"""

scaler = StandardScaler()

"""Model Training"""

knn_result = []

for k in range (2, 10):
    clf = Pipeline([
        ("scaler", scaler),
        ("knn", KNeighborsRegressor(n_neighbors=k))
        ])
    clf.fit(X_train, y_train)
    cross_val = cross_val_score(clf, X, y, cv=10)
    cross_val_avg = cross_val.mean()
    knn_result.append(cross_val_avg)
    print(f"R-Squared for k = {k} : {cross_val_avg:.3f}")

"""Visualize the R-Squared result"""

plt.figure(figsize=(20,6))
plt.plot([i for i in range(2, 10)], knn_result)
plt.xlabel("k Neighbors")
plt.ylabel("R-Squared Score")
plt.title("k-Nearest Neighbors")
plt.show()

"""Create a KNN model and evaluate the model on the training set"""

knn = KNeighborsRegressor(n_neighbors=8).fit(X_train,y_train)
knn_training_pred = knn.predict(X_train)
knn_training_rsq = knn.score(X_train, y_train)
knn_training_rmse = np.sqrt(mean_squared_error(y_train, knn_training_pred))

print(f"R-Squared for the training set : {knn_training_rsq:.3f}")
print(f"RMSE for the training set : {knn_training_rmse:.3f}")

"""Evaluate the model on the testing set"""

knn_testing_pred = knn.predict(X_test)
knn_testing_rsq = knn.score(X_test, y_test)
knn_testing_rmse = np.sqrt(mean_squared_error(y_test, knn_testing_pred))

print(f"R-Squared for the testing set : {knn_testing_rsq:.3f}")
print(f"RMSE for the testing set : {knn_testing_rmse:.3f}")

"""Visualize the regression plot and the residual plot of the KNN method"""

residual_train = y_train - knn_training_pred
residual_test = y_test - knn_testing_pred

fig=plt.figure(figsize=(20,5))

ax1=plt.subplot(1,2,1)
ax1.scatter(y_train, knn_training_pred, s=60, alpha=0.8, edgecolor="white", label="training")
ax1.scatter(y_test, knn_testing_pred, marker="^", s=60, c="r", alpha=0.8, edgecolor="white", label="testing")
ax1.plot([y.min(), y.max()], [y.min(), y.max()], "k", lw=1)
ax1.set_title("Actual vs. Predicted Plot")
ax1.set_xlabel("Actual")
ax1.set_ylabel("Predicted")
ax1.legend()

ax2=plt.subplot(1,2,2)
ax2.scatter(y_train, residual_train, s=60, edgecolor="white", alpha=0.8, label="training")
ax2.scatter(y_test, residual_test, marker="^", s=60, c="r", edgecolor="white", alpha=0.8, label="testing")
ax2.axhline(y=0.3, linewidth= 1, linestyle="-", c="black")
ax2.legend()
ax2.set_title("Residual Plot")
ax2.set_xlabel("LC50")
ax2.set_ylabel("Residual")

plt.show()