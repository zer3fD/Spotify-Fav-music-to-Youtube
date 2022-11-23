# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import requests
import json
import pandas
from time import sleep
from bs4 import BeautifulSoup
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from requests_html import HTMLSession

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "clientSecretKey.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

videoId = []
ids=[]
newPlaylistId = "lol"

def getVideoId(query):
  request = youtube.search().list(
    part="snippet"
    ,maxResults = 1
    , q = query
  )
  response = request.execute()
  for item in response['items']:
    videoIds.append(item['id']['videoId'])
  return videoId[0]

def listOfVideoIds(list):
  for index,item in enumerate(list):
    temp = getVideoId(item)
    ids += [temp]
    return ids

def createPlaylist():
  request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": "Sample playlist created via API",
            "description": "This is a sample playlist description.",
            "tags": [
              "sample playlist",
              "API call"
            ],
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
  )
  response = request.execute()
  newPlaylistId = response['id']

def addToPlaylist(id,vID):
        request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": id,
            "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": vID
            }
          }
        }
        )
        response = request.execute()

def multiToPlaylist(vId,list):
  for index,item in enumerate(list):
    addToPlaylist(vId,item)

def main():
    data = pandas.read_csv('songs.csv')
    data = data['Songs'].tolist()

  #Create Playlist
    createPlaylist()
    
    listOfVideoIds(data)
    #Add videos to playlist
    multiToPlaylist(newPlaylistId,ids)

if __name__ == "__main__":
    main()