import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %% read csv
df = pd.read_csv('data.csv')
# print(df.info())

df.drop(["Unnamed: 32", "id"], axis=1, inplace=True)
df.diagnosis = [1 if each == "M" else 0 for each in df.diagnosis]

y = df.diagnosis.values
x_data = df.drop(["diagnosis"], axis=1)

# %% normalization
x = (x_data - x_data.min()) / (x_data.max() - x_data.min())
x = x.values

# %% train test split
from sklearn.model_selection import train_test_split
(x_train, x_test, y_train, y_test) = train_test_split(x,y,test_size=0.2,random_state=42)

x_train = x_train.T
x_test = x_test.T
y_train = y_train.T
y_test = y_test.T

# %% parameter initialize and sigmoid function
def initialize_weight_and_bias(dimension):
    w = np.full((dimension, 1), 0.01)
    b = 0.0
    
    return w, b

# note: sigmoid = f(x) = 1 / 1 + e^-(x)
def sigmoid(z):
    y_head = 1/(1+np.exp(-z))
    return y_head

def forward_backward_propagation(w,b,x_train,y_train):
    # forward propagation
    # z = (w.T)x + b
    # in another say z = b + px1w1 + px2w2 + ... + pxn*wn
    z = np.dot(w.T, x_train) + b
    y_head = sigmoid(z)
    loss = -y_train*np.log(y_head)-(1-y_train)*np.log(1-y_head)
    cost = (np.sum(loss))/x_train.shape[-1]
    
    derivative_weight = (np.dot(x_train, ((y_head-y_train).T))) / x_train.shape[1]
    derivative_bias = np.sum(y_head-y_train)/x_train.shape[1]
    gradients = {"derivative_weight": derivative_weight, "derivative_bias": derivative_bias}
    
    return cost, gradients

def update(w, b, x_train, y_train, learning_rate, number_of_iterarion):
    cost_list = []
    cost_list2 = []
    index = []
    
    for i in range(number_of_iterarion):
        cost, gradients = forward_backward_propagation(w, b, x_train, y_train)
        cost_list.append(cost)
        
        w = w - learning_rate * gradients["derivative_weight"]
        b = b - learning_rate * gradients["derivative_bias"]
        if i % 10 == 0:
            cost_list2.append(cost_list)
            index.append(i)
            print("Cost after iteration: %i: %f" %(i, cost))
        
    parameters = {"weight": w, "bias": b}
    plt.plot(index, cost_list2)
    plt.xticks(index, rotation="vertical")
    plt.xlabel("number of iteration")
    plt.ylabel("Cost")
    plt.show()
        
    return parameters, gradients, cost_list

def predict(w, b, x_test):
    z = sigmoid(np.dot(w.T, x_test) + b)
    y_prediction = np.zeros((1, x_test.shape[1]))
    
    for i in range(z.shape[1]):
        if z[0,i] <= 0.5:
            y_prediction[0, i] = 0
        else:
            y_prediction[0, i] = 1
            
    return y_prediction


# %% logistic regression
def logistic_regression(x_train, y_train, x_text, y_test, learning_rate, num_iterations):
    dimension = x_train.shape[0]
    w, b = initialize_weight_and_bias(dimension)
    
    parameters, gradients, cost_list = update(w, b, x_train, y_train, learning_rate, num_iterations)
    
    y_prediction_test = predict(parameters["weight"], parameters["bias"], x_test)
    # y_prediction_train = predict(parameters["weight"], parameters["bias"], x_train)
    
    # print("train accuracy {} %".format(100 - np.mean(np.abs(y_prediction_train - y_train)) * 100))
    print("test accuracy {} %".format(100 - np.mean(np.abs(y_prediction_test - y_test)) * 100))
    
logistic_regression(x_train, y_train, x_test, y_test, learning_rate = 1, num_iterations = 300)

# %% logistic regresssion with sklearn
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()

lr.fit(x_train.T, y_train.T)
print("Test accuracy: {}%".format(lr.score(x_test.T, y_test.T)))
