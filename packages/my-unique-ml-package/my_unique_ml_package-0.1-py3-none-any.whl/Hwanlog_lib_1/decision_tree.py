import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

def load_and_prepare_data():
    bank_df = pd.read_csv('UniversalBank.csv')
    bank_df = bank_df.drop(columns=['ID', 'ZIP Code'])
    
    X = bank_df.drop(columns=['Personal Loan'])
    y = bank_df['Personal Loan']
    
    train_X, valid_X, train_y, valid_y = train_test_split(X, y, test_size=0.4, random_state=1)
    
    return train_X, valid_X, train_y, valid_y

def train_decision_tree(train_X, train_y):
    fullClassTree = DecisionTreeClassifier()
    fullClassTree.fit(train_X, train_y)
    return fullClassTree

def plot_decision_tree(model, feature_names):
    plt.figure(figsize=(20,10))
    plot_tree(model, feature_names=feature_names, filled=True, rounded=True, class_names=['No', 'Yes'])
    plt.show()

def main():
    train_X, valid_X, train_y, valid_y = load_and_prepare_data()
    model = train_decision_tree(train_X, train_y)
    plot_decision_tree(model, feature_names=train_X.columns)