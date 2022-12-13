import unittest
import requests
import base64
import json
import requests
import csv
import os
from bs4 import BeautifulSoup
import sqlite3
import re

from secrets import *

# Step 1 - Authorization 
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Encode as Base64
message = f"{clientId}:{clientSecret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')


headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

#Code above give us access to the Spotify API now we have to make requests!

headers = {
    "Authorization": "Bearer " + token
}

def get_artistID(list_of_artist):
    """This function get_artistID takes in a list of artist names,
    searches the Spotify API for that artist, and
    returns a list if tuples of the (Artist Name, Artist ID)"""

    searchUrl = "https://api.spotify.com/v1/search"
    artistId_lst = []


    for artist in list_of_artist: 
        para = {
        "q" : artist,
        "type": "artist",
        "limit": "5"
        } #these are the parameters for searching in the Spotify API
        r = requests.get(searchUrl, headers=headers, params = para)
        json_data = json.loads(r.text) #takes results from request and turns it into a python dictionary object

        if artist == json_data['artists']['items'][0]['name']:
        # ^if the artists name is the same as the artist name in the results
            tup = (json_data['artists']['items'][0]['name'], json_data['artists']['items'][0]['id'])
            #^creat a tuple of the artist name and artist id
            artistId_lst.append(tup)
            #^add tuple to list

    return artistId_lst


def get_topTracks(artistId_lst):
    """The function get_topTracks takes in a list of tuples that contain (Artist Name, Artist ID),
    uses the top tracks Spotify API and the Artist ID 
    to return a list of tuples that have the artist name, artist ID, song title, song popularity
    with 10 songs (their top songs) per artist
    Ex. (Artist ID, Artist Name, Song Title (1), Song Popularity)
        (Artist ID, Artist Name, Song Title (2), Song Popularity) 
        etc... """

    para = {
    "market": 'US',
    "limit": "10"
    } #these are parameters for top tracks results in the Spotify API
    toptracks_lst = []


    for id in artistId_lst: #id is tuple of artist name(id[0]) and artist ID(id[1])
        toptracksUrl = f"https://api.spotify.com/v1/artists/{id[1]}/top-tracks"

        r = requests.get(toptracksUrl, headers=headers, params = para)
        json_data = json.loads(r.text)
        #^requests and load results into a python object

        for i in range(0,10): 
        #^give us the top ten tracks
            tup = (id[1], id[0], json_data['tracks'][i]['name'],json_data['tracks'][i]['popularity'] )
            #^create a tup and add (Artist ID, Artist Name, Song Title) 
            toptracks_lst.append(tup)
            #^add tuple to list
    return(toptracks_lst)



def get_songURLpath(data):
    """The function get_songURLpath takes in a list of tuples (from get_topTracks)
    and searches the artist name and the song title using the Genius API 
    finds the pathurl for each song (the pathurl is a string ex. '/songs/234513/'
    that is used at the end of the genius.com url to find the song lyrics) 
    and returns a list of tuples that contains the Artist ID from Spotify, 
    Song Title from Genius, Artist Name from Genius, and the Song URL Path """

    song_data = []

    for i in data: 
        songTitle = i[2]
        artistName = i[1]
        artistIDfromSpotify = i[0]

        
        genius_search_url = f"http://api.genius.com/search?q={artistName + songTitle}&access_token={client_access_token}"
        #^searches the Genius API with the artist name and song title
        r = requests.get(genius_search_url)
        json_data = json.loads(r.text)
        #^requests and load results into a python object


        for i in range(len(json_data['response']['hits'])):
        #^for the length of the search results
            if songTitle.lower() in json_data['response']['hits'][i]['result']['title'].lower() or json_data['response']['hits'][i]['result']['title'].lower() in songTitle.lower():
            #^if the song title from Spotify and Genius are the same
                songTitle_genius = json_data['response']['hits'][i]['result']['title']
                artistName_genius = json_data['response']['hits'][i]['result']['artist_names']
                songURLpath = json_data['response']['hits'][i]['result']['api_path']
                tup = (artistIDfromSpotify, songTitle, artistName, songURLpath)
                song_data.append(tup)
                break
                #^give us the information once it matches then break out of the conditional
    return song_data

def get_profanity(genius_data):
    """ The function get_profanity takes in a list of tuples (from get_songURLpath)
    uses BeautifulSoup and the url path form the genius data to find the lyrics then
    counts the number of words in the song and the number of "bad" words in the song"""

    profanity_data = []

    for i in genius_data:
    #^for each song
        songTitle = i[1]
        artistName = i[2]
        lyrics = ""

        url = "https://genius.com" + i[3] 
        #^adds the url path of the song to the url
        data = requests.get(url)
        soup = BeautifulSoup(data.text,'html.parser')
        #^Request using BeautifulSoup

        lyrics_container = soup.find('div', class_ = "Lyrics__Container-sc-1ynbvzw-6 YYrds") 
        try:
            lyrics += lyrics_container.text + ' '
            brlyrics = lyrics_container.find_all('br')
            for brlyric in brlyrics:
                lyrics += brlyric.text + ' '
            alyrics = lyrics_container.find_all('a')
            for alyric in alyrics:
                spanlyrics = alyric.find_all('span')
                for spanlyric in spanlyrics:
                    lyrics += spanlyric.text + " "    
        except:
            pass
        #^sometimes lyrics were deeply embeed into the html so we asked the code to try
        
        profanity_data.append((songTitle, artistName, lyrics))
    return profanity_data






# MAIN # 
list_of_artist = ["H.E.R.", "Summer Walker", "Jhené Aiko", "Ari Lennox", 
"Bryson Tiller", "SZA", "Brent Faiyaz",
"Kehlani", "Drake", "Chris Brown", "Lucky Daye", "Queen Naija", 
"Jazmine Sullivan", "Mariah the Scientist", "Tems"]
artistIdtup = get_artistID(list_of_artist)
data = get_topTracks(artistIdtup)
genius_data = get_songURLpath(data)
profanity_data = get_profanity(genius_data)












# WASTELAND #

    # search_term = "Formation"
    # genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"

    # r = requests.get(genius_search_url)
    # json_data = json.loads(r.text)

    

    # api_key = json_data['response']['hits'][1]['result']['api_path']
    # title = json_data['response']['hits'][1]['result']['title']
    # artist = json_data['response']['hits'][0]['result']['artist_names']

# for loop attempt had trouble making it continue to search after it didn't find the right result
        # for search in json_data['response']['hits']:
        #     search_result = 0
        #     if json_data['response']['hits'][search_result]['result']['title'] == songTitle:
        #         print("yay!")

    

        # while found == False:
        #     if json_data['response']['hits'][search_result]['result']['artist_names'] != "Genius":
        #         # don't give us a playlist created by Genius
        #         if json_data['response']['hits'][search_result]['result']['artist_names'] != "Spotify":
        #             # don't give us a playlist created by Spotify
        #             if json_data['response']['hits'][search_result]['result']['language'] != 'en':
        #                 # don't give us a song that isn't in english
        #                 found = True
        #                 song_data.append(json_data['response']['hits'][search_result]['result']['api_path'])
        #                 break
        #             else:
        #                 search_result += 1
        #                 found = False

        # for i in json_data['response']['hits']:
        #     #print(i)
        #     for j in range(0,5):
        #         if json_data['response']['hits'][j]['result']['artist_names'] != "Genius":
        #             if json_data['response']['hits'][j]['result']['artist_names'] != "Spotify":
        #                 if json_data['response']['hits'][j]['result']['language'] != 'en':
        #                     #print(json_data['response']['hits'][j]['result']['title'])

          # for word in lyrics.split():
        #     if word in profanity_lst:
        #         if word in profanity_dic:
        #             profanity_dic[word] += 1
        #         else:
        #             profanity_dic[word] = 1
        #     if i[0] not in profanity:
        #         profanity[i[0]] = profanity_dic
    
    #print(profanity)

        # lyrics_container = soup.find('div', class_ = "Lyrics__Container-sc-1ynbvzw-6 YYrds") 
        # try:
        #     alyrics = lyrics_container.find_all('a')
        #     for alyric in alyrics:
        #         spanlyrics = alyric.find_all('span')
        #         for spanlyric in spanlyrics:
        #             brlyrics = spanlyric.find_all('br')
        #             lyrics += spanlyric.text + " "
        #             for brlyric in brlyrics:
        #                 lyrics += brlyric.text + " "

    #     def get_avg_popularity(data):
    # """The function get_avg_popularity takes in a list of tuples(from get_topTracks) 
    # and calculates the average song popularity using the Artist's top ten tracks, 
    # then stores in a list of tuples avg_popularity with the 
    # Artist Name: Average Song Popularity in a key value pair"""
    # popularity_tot_dic = {}
    # for i in data: 
    #     if i[1] in popularity_tot_dic:
    #         popularity_tot_dic[i[1]] += int(i[3])
    #     else:
    #         popularity_tot_dic[i[1]] = int(i[3])
    # #^creats a song popularity total dictionary per artist dictionary

    # avg_popularity = [] 
    # for i in popularity_tot_dic.items():
    #     avg = int(i[1])/10
    #     artist = i[0]
    #     tup = (artist, avg)
    #     avg_popularity.append(tup)
    # #^uses the total popularity dictionary and calculates average per artist and add tuple into list

    # def get_table2(avg_popularity, filename):
    # with open(filename, 'w') as out:
    #     csv_out = csv.writer(out)
    #     csv_out.writerow([ 'Artist Name', 'Average Popularity'])
    #     for row in avg_popularity:
    #         csv_out.writerow(row)