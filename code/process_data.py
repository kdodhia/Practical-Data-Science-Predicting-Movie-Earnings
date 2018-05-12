import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing

Seasons = {1: 0, 2:0, 3:1, 4:1, 5:1, 6:2, 7:2, 8:2, 9:3, 10:3, 11:3, 12:0}

def convert_to_int(df):
	df['Total Theatres'] = df['Total Theatres'].apply(lambda x: int(x.replace(',', '')))
	df['Opening Theatres'] = df['Opening Theatres'].apply(lambda x: int(x.replace(',', '')))
	df['Gross Earnings'] = df['Gross Earnings'].apply(lambda x: int(x.replace(',', '').replace('$', '')))
	df['Opening Earnings'] = df['Opening Earnings'].apply(lambda x: int(x.replace(',', '').replace('$', '')))
	df['budget'] = df['budget'].apply(lambda x: int(x))
	#df['likes'] = df['likes'].apply(lambda x: int(x))
	#df['dislikes'] = df['dislikes'].apply(lambda x: int(x))


	return df

def one_hot_encode(df, col):
	drop_col = df[col].unique()
	if (col == "Studio"):
		drop_col = sorted(drop_col, key = str.lower)
	else:
		drop_col = sorted(drop_col)

	if (col == 'Release Date'):
		cols = ['Winter', 'Spring', 'Summer', 'Fall']
	else:
		cols = [col + str(i + 1) for i in range(len(drop_col))]
	df[col] = df[col].apply(lambda x: drop_col.index(x))
	dummies = pd.get_dummies(df[col]).astype('int64')
	dummies.columns = cols
	df = df.reset_index(drop = True)
	dummies = dummies.reset_index(drop = True)
	df = pd.concat([df, dummies], axis = 1)
	df[cols] = df[cols].astype('int64')
	df = df.drop(col, axis = 1)
	return df
	

def convert_to_float(df):
	df['cast_rating'] = df['cast_rating'].apply(lambda x: float(x))
	df['directing_rating'] = df['directing_rating'].apply(lambda x: float(x))
	df['similar_movie_rating'] = df['similar_movie_rating'].apply(lambda x: float(x))
	return df

def discretize(df, col):
	if (col == 'Opening Earnings'):
		discretized = pd.cut(df[col],10)
		print(discretized)


	else:
		discretized = pd.qcut(df[col],20, labels = False, duplicates = 'drop')



	df[col] = discretized
	return df

def drop_nan(df):
	df = df[df['Total Theatres'] != 'N/A']
	df = df[df['Opening Theatres'] != 'N/A']
	df = df[df['Gross Earnings'] != 'N/A']
	df = df[df['Opening Earnings'] != 'N/A']
	df['cast_rating'] = df['cast_rating'].replace(np.nan, 0)
	df['similar_movie_rating'] = df['similar_movie_rating'].replace(np.nan, 0)
	df['directing_rating'] = df['directing_rating'].replace(np.nan, 0)

	return df


def get_log(df):
	df['Total Theatres'] = np.log(df['Total Theatres'])
	df['Total Theatres'] = df['Total Theatres'].apply(lambda x: 0 if (np.isneginf(x)) else x)

	df['Opening Theatres'] = np.log(df['Opening Theatres'])
	df['Opening Theatres'] = df['Opening Theatres'].apply(lambda x: 0 if (np.isneginf(x)) else x)

	df['dislikes'] = np.log(df['dislikes'])
	df['dislikes'] = df['dislikes'].apply(lambda x: 0 if (np.isneginf(x)) else x)

	df['likes'] = np.log(df['likes'])
	df['likes'] = df['likes'].apply(lambda x: 0 if (np.isneginf(x)) else x)

	df['views'] = np.log(df['views'])
	df['views'] = df['views'].apply(lambda x: 0 if (np.isneginf(x)) else x)

	return df

def date_to_season(df):
	df['Release Date'] = df['Release Date'].apply(lambda x: Seasons[int(x.split('/')[0])])
	return df


df = pd.read_pickle("new_dataset.pkl")

#df1 = pd.read_pickle("final_db2.pkl")
#df1 = df1.rename(index=str, columns={"name": "Movie Title"})
df = drop_nan(df)
df = convert_to_int(df)

df = convert_to_float(df)
#print(df.likes)
df = df.drop(['similar', 'popularity_rating', 'production_companies'], axis = 1)
#print(len(df))
df1 = pd.DataFrame.from_csv("movie_comment_data_new.csv", index_col = None)

df1 = df1.rename(columns = {'movie_name': 'Movie Title'})
df1 = df1.dropna()



#print(len(df), len(df1))
df = pd.merge(df, df1, on = "Movie Title", how = 'inner')
#print(df.columns)



df = df.drop("Studio", axis = 1)

plt.hist(df['likes'], bins = len(df['likes'].unique()))
plt.axis([0,100000,0,100])

plt.xlabel("likes")
plt.ylabel("Count")
plt.title('Frequency Histogram of likes')

plt.show()



#df = df[df['views'] < 10000000]
# df = df[df.views > 50000]


#df = one_hot_encode(df, 'Studio')
df = discretize(df, 'Opening Earnings')
df = discretize(df, 'Gross Earnings')
df = discretize(df, 'Total Theatres')
df = discretize(df, 'Opening Theatres')
df = discretize(df, 'dislikes')
df = discretize(df, 'views')
df = discretize(df, 'likes')


plt.hist(df['likes'], bins = len(df['likes'].unique()))
plt.axis([0,20,0,5000])
plt.xlabel("likes")
plt.ylabel("Count")
plt.title('Frequency Histogram Bins')

plt.show()


# df = df.drop_duplicates('trailer_video_id')

df = df.drop(['budget', 'trailer_video_id', 'imdb_id'], axis = 1)

df = df.drop('genres', axis = 1)

print(df.dtypes)


df = df.drop('adult', axis = 1)



print(df.likes)

#plt.hist(df['Total Theatres'], bins = df['Total Theatres'].unique())
#plt.show()
#df = one_hot_encode(df, 'Opening Earnings')
#df = one_hot_encode(df, 'Gross Earnings')
df = one_hot_encode(df, 'Total Theatres')
df = one_hot_encode(df, 'Opening Theatres')
df = one_hot_encode(df, 'dislikes')
df = one_hot_encode(df, 'views')
df = one_hot_encode(df, 'likes')

print(df.dtypes)


df.to_pickle("usable_dataset1.pkl")


#df.to_pickle("movie_processed1.pkl")

#print(df1['imdb_id'])

print(len(df))

#df2 = pd.merge(df, df1, on='Movie Title', how = 'inner')
#print(len(df2))










