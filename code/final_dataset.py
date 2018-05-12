import pandas as pd
import matplotlib.pyplot as plt

def discretize(df, col):
	discretized = pd.qcut(df[col],10, labels = False, duplicates = 'drop')
	df[col] = discretized
	return df


cols = ["Studio" + str(i + 1) for i in range(822)]


df1 = pd.DataFrame.from_csv("movie_comment_data_new.csv", index_col = None)

df1 = df1.rename(columns = {'movie_name': 'Movie Title'})

df1 = df1.dropna()

df = pd.read_pickle("merged.pkl")

print(df1.columns, len(df1))
print(len(df))

df = pd.merge(df, df1, on = 'Movie Title', how = 'inner')

df.to_pickle("final_dataset.pkl")

#df = discretize(df, 'likes')


df = df.drop(cols, axis = 1)

print(df.columns)

print(df.loc[df['Movie Title'] == 'Iron Man'])



#plt.show()

