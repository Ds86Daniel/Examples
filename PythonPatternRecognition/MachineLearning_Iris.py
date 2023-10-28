# -*- coding: utf-8.


"""
Created on Tue Oct 17 23:18:02 2023

@author: Sanchez-Cisneros
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

def iris_classifier_visualizer():
    # Load dataset
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    class_names = iris.target_names

    # Split dataset into training and testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train a KNN classifier
    classifier = KNeighborsClassifier(n_neighbors=3)
    classifier.fit(X_train, y_train)

    # Predictions
    y_pred = classifier.predict(X_test)

    # Print classification report
    print(classification_report(y_test, y_pred, target_names=class_names))

    # Confusion matrix
    matrix = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10,7))
    sns.heatmap(matrix, annot=True, cmap="Blues", xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.show()

# Run the function
iris_classifier_visualizer()
