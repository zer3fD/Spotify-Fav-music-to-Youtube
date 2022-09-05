# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from time import sleep
from urllib import request, response
from bs4 import BeautifulSoup
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from requests_html import HTMLSession

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def getVideoId(query):
    searchQueryUrl="http://www.youtube.com/results?search_query="
    url = searchQueryUrl + query
    url.replace(" ","+")
    page = request.get(url)
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html,"html.parser")
    results = soup.find('a',id="video-title")
    return results['href'].split('/watch?v=')[1]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_633095474208-2j3rgsvjpfti0495aehbnsa53m2jnvsn.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": "Spotify API",
            "description": "Playlist of spotify liked videos",
            "tags": [
              "spotify playlist"
            ],
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    response = request.execute()

    print("PlayList Created")

if __name__ == "__main__":
    main()