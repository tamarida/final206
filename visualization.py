from calculations import *
import matplotlib.pyplot as plt
import numpy as np


def plot_avg(data):

    artist = []
    averages = []
    for i in data: 
        artist.append(i[0])
        averages.append(i[1])
   

    colors = ['green', 'blue', 'purple', 'brown', 'teal']
    plt.bar(artist, averages, color=colors)
    plt.title('Average Song Popularity per Artist', fontsize=10)
    plt.xlabel('Artist', fontsize=10)
    plt.ylabel('Average Song Popularity', fontsize=10)
    plt.grid(True)
    plt.show()


def plot_avgbad(data2):

    artist = []
    averages_bad = []
    for i in data2: 
        artist.append(i[0])
        averages_bad.append(i[1])
   

    colors = ['green', 'blue', 'purple', 'brown', 'teal']
    plt.bar(artist, averages_bad, color=colors)
    plt.title('Average Bad Word Usage per Artist', fontsize=14)
    plt.xlabel('Artist', fontsize=14)
    plt.ylabel('Average Bad Word Usage', fontsize=14)
    plt.grid(True)
    plt.show()

def plot_correlation(data, data2):
    list1 = []
    list2 = []
    for i in data:
        list1.append(i[1])
    for i in data2:
        list2.append(i[1])
    
    x = np.array(list1)
    y = np.array(list2)

    plt.scatter(x, y)
    plt.title('Average Bad Word Usage vs. Avergae Popularity Level in R&B Music', fontsize=14)
    plt.xlabel('Average Popularity Level', fontsize=14)
    plt.ylabel('Average Bad Word Usage', fontsize=14)
    plt.grid(True)
    plt.show()
         


# MAIN #
plot_avg(data)
plot_avgbad(data2)
plot_correlation(data, data2)


