import pandas as pd

df = pd.read_pickle("final_dataset_rating.pkl")
df = df.drop('Movie Title', axis = 1)


df1 = pd.read_pickle("movie_df.pkl")

df2 = pd.read_pickle("movie_with_id.pkl")
df1 = df1.drop_duplicates(subset=['Movie Title'])


df2 = df2.drop_duplicates(subset=['imdb_id'])
df2 = df2.drop_duplicates(subset=['Movie Title'])

df3 = df2[['Movie Title', 'imdb_id']]


cols = ["Studio" + str(i + 1) for i in range(822)]
cols1 = ["Gross Earnings" + str(i + 1) for i in range(10)]
cols2 = ["Opening Theatres" + str(i + 1) for i in range(8)]
cols3 = ["Opening Earnings" + str(i + 1) for i in range(10)]
cols4 = ["Total Theatres" + str(i+1) for i in range(10)]

cols.extend(cols1)
cols.extend(cols2)
cols.extend(cols3)
cols.extend(cols4)


df = df.drop(cols, axis = 1)

df4 = pd.merge(df1, df3, on = 'Movie Title', how = 'inner')



df5 = pd.merge(df4, df, on = 'imdb_id', how = 'inner')


for index, row in df5.iterrows():
	if (len(row.cast) < 5 and len(row.cast) != 0):
		df5.set_value(index, 'cast_rating', float(row['cast_rating'] * 5)/len(row.cast))
	if (len(row.similar) < 5 and len(row.similar) != 0):
		df5.set_value(index, 'similar_movie_rating', float(row['similar_movie_rating'] * 5)/len(row.similar))



drop_cols = ['Close Data', 'Release Date', 'cast', 'directing', 'id',
				'popularity', 'sentiment_score', 'likes', 'dislikes', 'views', 'trailer_video_id']

df5 = df5.drop(drop_cols, axis = 1)


print(df5.columns)

df5.to_pickle("new_dataset.pkl")





