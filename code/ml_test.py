import pandas as pd
import numpy as np
check_df = pd.read_pickle('usable_dataset1.pkl')
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
mask = np.random.rand((len(check_df))) < 0.8

train = check_df[mask]

test = check_df[~mask]

print(train.columns)
y_train = train['Opening Earnings']
x_train = train.drop(['Movie Title', 'Opening Earnings', 'Gross Earnings'], axis=1)
x_train = x_train.astype('float64')

x_train.reset_index(drop = True, inplace = True)
y_train.reset_index(drop = True, inplace = True)



y_test = test['Opening Earnings']
x_test = test.drop(['Movie Title', 'Opening Earnings', 'Gross Earnings'], axis = 1)
x_test = x_test.astype('float64')
#print(len(x_test))
y_test = y_test.astype('float64')

x_test.reset_index(drop = True, inplace = True)
y_test.reset_index(drop = True, inplace = True)

num_clusters = 50

X = x_train.as_matrix()
Y = y_train.as_matrix()
X_t = x_test.as_matrix()
Y_t = y_test.as_matrix()
#print(y_test[0:10])
#print(Y_t[0:10])
#print(X.shape, Y.shape)
svc = LogisticRegression(solver = 'lbfgs')
svc.fit(X,Y)
ch = svc.predict(X_t)
#print(svc.score(ch,Y_t))
print(ch[0:10])
print(Y_t[0:10])
cor = [(int(Y_t[x]-1)) <= (int(ch[x])) <= (int(Y_t[x])+1)  for x in range(len(Y_t))]
print(sum(cor)/len(Y_t))
# kmeans = KMeans(n_clusters=num_clusters, random_state=0,init = 'k-means++').fit(X)
# x_train['Labels'] = kmeans.labels_


# a = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}
# res = [0]*num_clusters
# for key in a:
# 	res[key] = np.sum(Y[a[key]])/float(len(a[key]))

# print(res)

# pred = kmeans.predict(X_t)
# f = [res[x] for x in pred]
# print(f[0:10])
# print(Y_t[0:10])
# print(y_test[0:10])


