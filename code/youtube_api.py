import os
import pickle
import pandas
import google.oauth2.credentials
import json

from googleapiclient.discovery import build
from googleapiclient.discovery import build_from_document
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


CLIENT_SECRETS_FILE = "client_secrets_ar.json"
SCOPES = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials = credentials)

max_iters = 5 
maxResults = 100

# Call the API's commentThreads.list method to list the existing comments.
def get_comments(youtube, video_id):
    pageToken = None
    comments = []
    pageToken = None
    for i in range(max_iters):
        if pageToken != False:
            try:
                results = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    order="relevance",
                    pageToken=pageToken,
                    maxResults=maxResults
                ).execute()
            except:
                print("ERROR: comments could not be scapped")
                return comments
        else:
            break

        if ("nextPageToken" in results): pageToken = results["nextPageToken"] 
        else: pageToken = False

        for item in results["items"]:
            cur_comment = {}
            comment = item["snippet"]["topLevelComment"]
            cur_comment['text'] = comment["snippet"]["textDisplay"]
            cur_comment['time'] = comment["snippet"]['publishedAt']
            cur_comment['rating'] = comment["snippet"]['viewerRating']
            comments.append(cur_comment)

    return comments

#publishedBefore='publishedBefore'

def search_list_by_keyword(youtube, movie_name):
    query = movie_name + ' offitial trailer'
    try:
        results = youtube.search().list(
            part='snippet',
            maxResults=1,
            q=query,
            type='video',
            order='relevance'
        ).execute()  
    except:
        print("ERROR:: search query failed")
        return []

    video_ids = []
    for item in results["items"]:
        video_id = item["id"]['videoId']
        video_ids.append(video_id)

    return video_ids


def get_videos_stats(youtube, video_id):
    try:
        results = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()
    except:
        print("ERROR:: stats query failed")
        return {}

    stats = {}

    statistics = results["items"][0]['statistics']

    if ('viewCount' in statistics): stats['views'] = statistics['viewCount']
    else:
        print("ERROR: viewCount key error") 
        stats['views'] = None
    if ('likeCount' in statistics): stats['likes'] = statistics['likeCount']
    else: 
        print("ERROR: likeCount key error") 
        stats['likes'] = None
    if ('dislikeCount' in statistics): stats['dislikes'] = statistics['dislikeCount']
    else: 
        print("ERROR: dislikes key error") 
        stats['dislikes'] = None

    return stats


def get_movie_data(youtube, movie_name):
    movie_data = {}
    videos = search_list_by_keyword(youtube, movie_name)
    for videoid in videos:
        movie_data[videoid] = {}
        movie_data[videoid]['stats']  = get_videos_stats(youtube, videoid)
        movie_data[videoid]['comments'] = get_comments(youtube, videoid)
    return movie_data


if __name__ == "__main__":
    youtube = get_authenticated_service()
    pickle_in = open("movie_df.pkl","rb")
    movie_list = pickle.load(pickle_in)

    data = {}

    for movie_name in movie_list['Movie Title']:
        print(str(i) + " : " + movie_name)
        if ((movie_name in data) and (data[movie_name] != {})):
            print("Already scrapped movie data")
        else:
            movie_data = get_movie_data(youtube, movie_name)
            data[movie_name] = movie_data
            with open('comments_data_new.txt', 'w') as outfile:
                json.dump(data, outfile)
    
