import pickle
import pandas as pd
from sklearn.neural_network import MLPClassifier
import string
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

window = 0
def check(x, y):
	if (y - window <= x <= y + window):
		return 1
	else:
		return 0

df = pd.read_pickle('usable_dataset1.pkl')
print(df.columns)
df['sentiment_score'] = [x > 0 for x in df['sentiment_score']]

msk = np.random.rand(len(df)) < 0.8

X_train = df[msk]

X_test = df[~msk]

y_train =  X_train['Opening Earnings']
y_test =  X_test['Opening Earnings']

X_train.drop(['Opening Earnings', 'Gross Earnings', 'Movie Title'], axis=1, inplace=True)
X_test.drop(['Opening Earnings', 'Gross Earnings', 'Movie Title'], axis=1, inplace=True)

print(len(X_train.columns))

X_train.reset_index(drop = True, inplace = True)
y_train.reset_index(drop = True, inplace = True)
X_test.reset_index(drop = True, inplace = True)
y_test.reset_index(drop = True, inplace = True)

X_train = X_train.as_matrix()
y_train = y_train.as_matrix()
X_test = X_test.as_matrix()
y_test = y_test.as_matrix()

clf = MLPClassifier(hidden_layer_sizes=(200, 100, 50), activation='logistic', solver='adam', 
	alpha=0.0001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001, 
	power_t=0.5, max_iter=5000, shuffle=True, random_state=None, tol=0.0001, verbose=False, 
	warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, 
	validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

clf.fit(X_train, y_train)  
y = clf.predict(X_test)

print(y[0:20])
print(y_test[0:20])

cor = [check(y[i], y_test[i]) for i in range(len(y))]

#print accuracy
print(sum(cor)/len(y))

## The following code was taken from https://chrisalbon.com/machine_learning/model_evaluation/plot_the_learning_curve/
train_sizes, train_scores, test_scores = learning_curve(estimator = clf, X = X_train, y = y_train, cv = None)\

# Create means and standard deviations of training set scores
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)

# Create means and standard deviations of test set scores
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

# Draw lines
plt.plot(train_sizes, train_mean, '--', color="#'r'",  label="Training score")
plt.plot(train_sizes, test_mean, color='g', label="Cross-validation score")

# Draw bands
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="#DDDDDD")
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#DDDDDD")

# Create plot
plt.title("Learning Curve")
plt.xlabel("Training Set Size"), plt.ylabel("Accuracy Score"), plt.legend(loc="best")
plt.tight_layout()
plt.show()
