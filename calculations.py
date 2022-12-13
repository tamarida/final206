from databases import *

def get_pop(query,cur, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results   ## returns as a List of Tuples

def get_artist(query2, cur, conn):
    cursor = conn.cursor()
    cursor.execute(query2)
    results = cursor.fetchall()
    return results   ## returns as a List of Tuples

def get_lyrics(query3, cur, conn):
    cursor = conn.cursor()
    cursor.execute(query3)
    results = cursor.fetchall()
    return results

def get_avgpop(popularity, artist):
    pop_dic = {}

    for a in artist:
        for p in popularity: 
            if a[0] in pop_dic: 
                if p[1] == a[1]:
                    pop_dic[a[0]].append(p[0])
            else: 
                pop_dic[a[0]] = []
    avergelst = []
    totnum = 0

    for i in pop_dic.items(): 
        totnum = 0
        total = len(i[1])
        for num in i[1]:
            totnum += num
        psum = totnum/total
        tup = (i[0], psum)
        avergelst.append(tup)
    
    return avergelst

def get_badWords(profanity_lst, lyrics, artist):
    bad = []
    baddata = {}
    for i in lyrics: 
        lyric = i[1].split()
        totalbad = 0
        for x in lyric: 
            nplyric = re.sub(r'[^\w\s]', '', x)
            if nplyric.lower() in profanity_lst:
                totalbad += 1
        tup = (i[0], totalbad)
        bad.append(tup)

    for a in artist:
        for b in bad: 
            if a[0] in baddata: 
                if b[0] == a[1]:
                    baddata[a[0]].append(b[1])
            else: 
                baddata[a[0]] = []
    
    return baddata

def get_avgbad(bad):
    avgBadlst = []
    for i in bad.items(): 
        totalbad = 0
        blen = len(i[1])
        for num in i[1]:
            totalbad += num
        bsum = totalbad/blen
        tup = (i[0], bsum)
        avgBadlst.append(tup)
    return avgBadlst

query = "SELECT popularity, artistid FROM tracks"
query2 = "SELECT name, id FROM artist"
query3 = "SELECT artistid, lyrics FROM lyrics"
profanity_lst = ['ass', 'asshole', 'bitch', 'bullshit', 'cock', 'cunt', 'damn',
'dick', 'fuck', 'fuckin','fucking', 'goddamn', 'hell', 'hoe', 'hoes', 'motherfuckin','motherfucking','motherfucker',
'motherfuckers','nigga', 'niggas', 'penius', 'piss', 'porn' 'pussy', 'shit', 'slut', 'weed']
popularity = get_pop(query, cur,conn)
artist = get_artist(query2, cur, conn)
lyrics = get_lyrics(query3, cur, conn)
bad = get_badWords(profanity_lst,lyrics, artist)

data = get_avgpop(popularity, artist)
data2 = get_avgbad(bad)