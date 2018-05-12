import os
import pickle
import pandas
import json
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def get_sentiment_score(comment):
    snt = analyser.polarity_scores(comment)
    return snt['compound']


if __name__ == "__main__":
	with open('comments_data_new.txt', 'r') as infile:
		data_1 = json.load(infile)

	with open('comments_data_new_2000.txt', 'r') as infile:
		data_2 = json.load(infile)

	with open('comments_data_new_4000.txt', 'r') as infile:
		data_3 = json.load(infile)

	with open('comments_data_new_6000.txt', 'r') as infile:
		data_4 = json.load(infile)

	with open('comments_data_new_8000.txt', 'r') as infile:
		data_5 = json.load(infile)

	with open('comments_data_new_9000.txt', 'r') as infile:
		data_6 = json.load(infile)
    
	csvfile = open('movie_comment_data.csv', 'w')
	writer = csv.writer(csvfile)
	writer.writerow(['movie_name', 'trailer_video_id', 'likes', 'dislikes', 'views', 'sentiment_score'])

	for j in range(6):

		if (j == 0): data = data_1
		if (j == 1): data = data_2
		if (j == 2): data =  data_3
		if (j == 3): data = data_4
		if (j == 4): data = data_5
		if (j == 5): data = data_6

		for movie_name, movie_info in data.items():
			if (movie_info == {}): continue
			else:
				for video_id, video_info in movie_info.items():
					video_info_1 = video_info
					video_id_1 = video_id

				comments = video_info_1['comments']
				stats = video_info_1['stats']
				if (stats == {}):
					likes = None
					dislikes = None
					views = None
				else:
					likes = stats['likes']
					dislikes = stats['dislikes']
					views = stats['views']
				print(movie_name)

				combined_text = ""
				total_score = 0
				for comment in comments:
					combined_text = combined_text + " " + comment['text'] 
					score = get_sentiment_score(comment['text'])
					total_score += score

				if (len(comments) == 0): ave_score = 0
				else: ave_score = total_score/len(comments)				
				writer.writerow([movie_name, video_id_1, likes, dislikes, views, ave_score])

	csvfile.close()

