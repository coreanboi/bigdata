# Yujoon Jang Homework9
# Topic: Final Project - AMC Movie Guide

from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import re
import os

def rtSearch(rtTitle):
    rtTitle = re.sub(r'[^\w\d]', '_', rtTitle)
    rtTitle = re.sub('_+', '_', rtTitle)
    try:
        rtPage = urlopen('https://www.rottentomatoes.com/m/' + rtTitle)
        rtSoup = BeautifulSoup(rtPage, 'html.parser')
        score = rtSoup.find('score-board')
        tomatoScore = score.attrs['tomatometerscore']
        audienceScore = score.attrs['audiencescore']
        if tomatoScore == '':
            tomatoScore = '---'
        if audienceScore == '':
            audienceScore = '---'  
    except:
        tomatoScore = '---'
        audienceScore = '---'
        pass
    return [rtTitle, tomatoScore, audienceScore]

def timeToMinutes(time):
    hours = 0
    minutes = 0
    if 'hr' in time:
        hours = int(time[0:2].strip()) * 60
    if 'min' in time:
        minutes = int(time[-6:-4].strip())
    time = hours + minutes
    return time

def extractDate(date):
    monthList = {
        'jan' : '01',
        'feb' : '02',
        'mar' : '03',
        'apr' : '04',
         'may' : '05',
         'jun' : '06',
         'jul' : '07',
         'aug' : '08',
         'sep' : '09',
         'oct' : '10',
         'nov' : '11',
         'dec' : '12'
    }
    date = date.replace('Released ', '')
    date = date.replace('Opening ', '')
    year = date[-4:]
    month = monthList[date[0:3].lower()]
    day = date[-8:-6].replace(' ', '')
    if len(day) == 1:
        day = '0' + day
    date = [year, month, day]
    date = year + '' + month + '' + day
    return date

def featureOption():
    print('\n\033[1m\033[96m[ Feature List ]\033[0m')
    print('1) Sort by Alphabet (A -> Z)')
    print('2) Sort by Running Time (Shortest -> Longest)')
    print('3) Sort by Released Date (Newest -> Oldest)')
    print('4) Sort by Tomatometer (Highest -> Lowest)')
    print('5) Sort by Audience Score (Highest -> Lowest)')
    print('6) Show only recommended movies (85 >= Tomatometer or Audience Score)')
    print('7) Save the final listing result in .csv file')
    print('8) Exit Program')
    f = input('\033[1mSelect feature options >> \033[0m')
    print('')
    return f

amcPage = urlopen('https://www.amctheatres.com/movies')
amcSoup = BeautifulSoup(amcPage, 'html.parser')
movieTitle = amcSoup.find_all('h3')
runningTime = amcSoup.find_all('span', {'class' : 'js-runtimeConvert'})
releasedDate = amcSoup.find_all('span', {'class' : 'MoviePosters__released-month'})
listOrder = 0
i = 0
movieData = []
print('\033[93m\033[1m# # # # # # # # # # # # # # # # # # # # # # #\033[0m')
print('\033[93m\033[1m# # # # # \033[91m    AMC MOVIE GUIDE    \033[93m # # # # #\033[0m')
print('\033[93m\033[1m# # # # # \033[96m           (by Yujoon)         \033[93m # # # # #\033[0m')
print('\033[93m\033[1m# # # # # # # # # # # # # # # # # # # # # # #\033[0m\n')
print('Please wait. Currently loading the movie data from AMC website.')

# The following code came from https://github.com/tqdm/tqdm
from tqdm import tqdm
loop = tqdm(total = len(movieTitle)-5, position = 0, colour = 'BLACK', leave = False)
for k in range(len(movieTitle)-5):
    loop.set_description('Loading...'.format(k))
# End of code from https://github.com/tqdm/tqdm
    
    while i <= len(movieTitle)-5:
        if movieTitle[i].text == 'Private Theatre Rental':
            movieTitle.remove(movieTitle[i])
        rtInfo = rtSearch(movieTitle[i].text)
        if rtInfo[1] == '---' and rtInfo[2] == '---':
            rtInfo = rtSearch(rtInfo[0] + '_' + releasedDate[i].text[-4:])  
        #print(i+1, '\b) ', movieTitle[i].text)
        #print(runningTime[i].text, ' │ ', releasedDate[i].text)
        #print('Tomatometer:', rtInfo[1], ' │ ', 'Audience Score:', rtInfo[2], '\n')
        timeInt = timeToMinutes(runningTime[i].text)
        dateInt = extractDate(releasedDate[i].text)
        tScore = rtInfo[1]
        aScore = rtInfo[2]
        if rtInfo[1] == '---':
            tScore = 0
        if rtInfo[2] == '---':
            aScore = 0
        movieData.append([movieTitle[i].text, int(timeInt), int(dateInt), int(tScore), int(aScore), runningTime[i].text, releasedDate[i].text, rtInfo[1], rtInfo[2]])
# The following code came from https://github.com/tqdm/tqdm
        loop.update(1)
# End of code from https://github.com/tqdm/tqdm
        i += 1
loop.close()
print('Loading completed.')
feature = featureOption()

while feature != '8':
    if feature == '1' or feature == '2' or feature == '3' or feature == '4' or feature == '5':
        if feature == '1':
            movieData.sort()
        elif feature == '2':
            movieData.sort(key=lambda elem: elem[1])
        elif feature == '3':
            movieData.sort(key=lambda elem: elem[2], reverse=True)
        elif feature == '4':
            movieData.sort(key=lambda elem: elem[3], reverse=True)
        else:
            movieData.sort(key=lambda elem: elem[4], reverse=True)
        listOrder = 1
        i = 0
        while i < len(movieData):
            print(i+1, '\b) ', movieData[i][0])
            print(movieData[i][5], ' │ ', movieData[i][6])
            print('Tomatometer:', movieData[i][7], ' │ ', 'Audience Score:', movieData[i][8], '\n')
            i += 1
        print('Total', i, 'movies are currently available at AMC Theatres.')
    elif feature == '6':
        recommendedList = []
        listOrder = 2
        i = 0
        while i < len(movieData):
            if  movieData[i][3] >= 85:
                recommendedList.append(movieData[i])
            elif movieData[i][4] >= 85:
                recommendedList.append(movieData[i])
            i += 1
        i = 0
        while i < len(recommendedList):
            print(i+1, '\b) ', recommendedList[i][0])
            print(recommendedList[i][5], ' │ ', recommendedList[i][6])
            print('Tomatometer:', recommendedList[i][7], ' │ ', 'Audience Score:', recommendedList[i][8], '\n')
            i += 1
        print('Total', i, 'movies are recommended.')
    elif feature == '7':
        fileName = input('Name the file as (Don\'t add file extensions) >> ')
# The following code came from https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
        filePath = os.path.dirname(os.path.realpath(__file__)) + '/' + fileName + '.csv'
#End of Code https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
        listData = []
        if listOrder == 2:
            listData = recommendedList
        else:
            listData = movieData
        with open(filePath, 'w', encoding='utf-8') as writeFile:
            writeFile.write('Movie Title, Running TIme (Min), Released Date, Tomatometer, Audience Score, Data as of ' + str(datetime.now().date()) + '\n')
            i = 0
            while i < len(listData):
                formattedDate = str(listData[i][2])
                formattedDate =  formattedDate[:4] + '-' + formattedDate[4:6] + '-' + formattedDate[-2:]
                formattedMovieTitle = listData[i][0].replace(',', '')
                writeFile.write(formattedMovieTitle + ',' + str(listData[i][1]) + ',' + formattedDate + ',' + str(listData[i][7]) + ',' + str(listData[i][8]) + '\n')
                i += 1
            print('Saved Path: ' + filePath)
            print('Total', i, 'movies in the list were saved to ' + fileName + '.csv file.')
    else:
        print('No such option available. Please try again.')
    feature = featureOption()
print('Thank you for using \'AMC Movie Guide\'. Good Bye.')