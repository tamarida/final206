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

from functions import *


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def createArtistTable(list_of_artist, cur, conn):
    cur.execute("CREATE table IF NOT EXISTS artist (id INTEGER PRIMARY KEY, name TEXT)")
    id = 1
    for artist in list_of_artist:
        cur.execute("INSERT OR IGNORE INTO artist (id, name) values (?,?)",(id,artist))
        id += 1
    conn.commit()

def createTrackTable(data, cur, conn):
    cur.execute("CREATE table IF NOT EXISTS tracks (id INTEGER PRIMARY KEY, songTitle TEXT, artistid INTEGER, popularity INTEGER)")
    cur.execute("SELECT MAX(id) FROM tracks")
    track_count = cur.fetchone()[0]
    if track_count is None:
       track_count = 1
    id = track_count
    for i in range(track_count, track_count + 25):
        artistid = cur.execute("SELECT id FROM artist WHERE name = ?", (data[i][1],)).fetchone()[0]
        st = data[i][2]
        pop = int(data[i][3])
        cur.execute("INSERT OR IGNORE INTO tracks (id, songTitle, artistid, popularity) VALUES (?,?,?,?)",(id,st,artistid,pop))
        id += 1
    conn.commit()



def createLyricsTable(profanity_data, cur, conn):
   cur.execute("CREATE table IF NOT EXISTS lyrics (id INTEGER PRIMARY KEY, tracksid INTEGER, artistid INTEGER, lyrics LONGTEXT)")
   cur.execute("SELECT MAX(id) FROM lyrics")
   lyric_count = cur.fetchone()[0]
   if lyric_count is None:
       lyric_count = 1
   id = lyric_count
   for lyrics in range(lyric_count, lyric_count + 25):
        tracksid = cur.execute("SELECT id FROM tracks WHERE songTitle = ?", (profanity_data[lyrics][0],)).fetchone()[0]
        artistid = cur.execute("SELECT id FROM artist WHERE name = ?", (profanity_data[lyrics][1],)).fetchone()[0]
        lyric = profanity_data[lyrics][2]
        cur.execute("INSERT OR IGNORE INTO lyrics (id, tracksid, artistid, lyrics) VALUES (?,?,?,?)",(id, tracksid, artistid, lyric))       
        id += 1
   conn.commit()



cur, conn = open_database('FinalProject.db')
createArtistTable(list_of_artist, cur, conn)
createTrackTable(data, cur, conn)
createLyricsTable(profanity_data, cur, conn)

