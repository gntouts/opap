import sqlite3
import csv
import requests
import json
import itertools
DB = 'correct.db'
DB2 = 'allcombos.db'

'''---------------------------------------------------------------------------------'''

'''---------------------------DATA MANIPULATION FUNCTIONS---------------------------'''

'''---------------------------------------------------------------------------------'''


def iterateSubsets(draws, subCnt):

    def hasAll(bigArr, subArr):
        '''Checks if bigArr has all elements of subArr.
        Parameters
        ----------
        bigArr: Array

        subArr: Array
        '''
        if subArr[0] < bigArr[0]:
            return False
        elif subArr[-1] > bigArr[-1]:
            return False
        else:
            f = 0
            for val in subArr:
                if interpolationSearch(bigArr, val):
                    f += 1
                else:
                    break
            if f == len(subArr):
                return True
            else:
                return False

    for sub in subCnt:
        for draw in draws:
            if hasAll(draw, sub[1]):
                sub[0] += 1


def stringToInt(arr):
    '''Takes as argument a string of numbers divided by whitespaces
    and returns an array of these numbers.

    For example: "1 23 54" returns [1, 23, 54]
    '''
    arr = arr.split()
    for i in range(len(arr)):
        arr[i] = int(arr[i])
    return arr


def arrayToString(arr):
    '''Takes an array of integers and returns a string of these integers divided by whitespaces.

    For example: [1, 23, 54] returns "1 23 54"
    '''

    temp = ""
    for i in range(len(arr)):
        temp += str(arr[i])+" "
    return temp[:-1]


def sortArray(arr):
    '''Sorts a 2-D array (arr) based on the values of the first "element" (arr[i][0]).
    '''
    def sortFirst(val):
        return val[0]

    arr.sort(key=sortFirst, reverse=True)
    return arr


def findSubsets(arr, n):
    '''Finds all unique subsets of n elements that can be found in Array 'arr' and
    returns them in a 2D Array.
    '''
    return list(itertools.combinations(arr, n))


def createSubCount(arr):
    '''Takes an Array of subsets and returns a 2D array with counters
    '''
    temp = []
    for sub in arr:
        temp1 = []
        temp1.append(0)
        temp1.append(sub)
        temp.append(temp1)
    return temp


def interpolationSearch(arr, val):
    '''Interpolation Search
    Parameters
    ----------
    arr : Array
        The array we will check
    val : Int
        The element we will search for

    Returns True if element exists in array and False if not.'''
    low = 0
    high = (len(arr) - 1)
    while low <= high and val >= arr[low] and val <= arr[high]:
        index = low + \
            int(((float(high - low) /
                  (arr[high] - arr[low])) * (val - arr[low])))
        if arr[index] == val:
            return True
        if arr[index] < val:
            low = index + 1
        else:
            high = index - 1
    return False


'''---------------------------------------------------------------------------------'''

'''----------------------------FUNCTIONS FOR APItoDB.py-----------------------------'''

'''---------------------------------------------------------------------------------'''


def createTable():
    '''Creates table 'kino' inside the Database.

    You have to declare a constant 'DB' at the top of the 'functions.py' file for the
    function to know which
    database to use.

    eg: DB = 'kino.db'
    '''
    conn = sqlite3.connect(DB)
    query = 'CREATE TABLE IF NOT EXISTS kino (drawid INTEGER, winning TEXT)'
    with conn:
        c = conn.cursor()
        c.execute(query)


def insertData(arg1, arg2):
    '''Takes arg1 and arg2 and inserts them as drawId and winning numbers into table kino.

    drawId=arg1, winning=arg2

    arg2 must be a STRING containing the winning numbers separated by single spaces.

    eg: arg2='4 54 21 4'

    '''
    conn = sqlite3.connect(DB)
    with conn:
        c = conn.cursor()
        c.execute("""INSERT INTO kino (drawid,
                    winning)
                    VALUES (:drawid,
                    :winning)""",
                  {'drawid': arg1, 'winning': arg2})


def insertData2(arg1, arg2):
    '''Takes arg1 and arg2 and inserts them as drawId and winning numbers into table kino.

    drawId=arg1, winning=arg2

    arg2 must be a STRING containing the winning numbers separated by single spaces.

    eg: arg2='4 54 21 4'

    '''
    conn = sqlite3.connect(DB2)
    with conn:
        c = conn.cursor()
        c.execute("""INSERT INTO kino (drawid,
                    winning)
                    VALUES (:drawid,
                    :winning)""",
                  {'drawid': arg1, 'winning': arg2})


def makeURL(startId, stopId):
    '''Returns the URL for the API request. It takes the start drawId and stop drawId as arguments'''
    return "https://api.opap.gr/draws/v3.0/1100/draw-id/"+str(startId)+"/"+str(stopId)+"?property=drawId&property=winningNumbers"


def sendReq(reqUrl):
    '''Takes an URL as argument, send a JSON API request and returns a 2D array with the draw ID and the winning numbers
    provided by the response. The format of the returnt array is:

    Array[i][0]: drawId

    Array[i][1]: list of winning numbers
    '''
    response = requests.get(reqUrl).json()['content']
    temp = []
    for i in response:
        temp1 = []
        temp1.append(i['drawId'])
        temp1.append(i['winningNumbers']['list'])
        temp.append(temp1)
    return temp


def getAllData(target):
    '''Sends requests for all data available and appends them to the 'target' Array'''

    def appendEach(source, target):
        for item in source:
            target.append(item)

    def getEm(arg1, arg2, target):
        source = sendReq(makeURL(arg1, arg2))
        appendEach(source, target)

    end = getActiveDraw()
    start = 704207
    for i in range(start, end, 10):
        if not (i-start) % 1000:
            print(str(i-start)+" / "+str(end-start))
        getEm(i-10, i-1, target)
        if i+10 > end:
            getEm(i, end-1, target)


def parseToDB(arr):
    '''Takes the result array created by getAllData() and inserts it into our Database, using the insertData() function.'''
    for item in arr:
        insertData(item[0], arrayToString(item[1]))


def parseToDB2(arr):
    '''Takes the result array created by getAllData() and inserts it into our Database, using the insertData() function.'''
    for item in arr:
        insertData2(item[0], arrayToString(item[1]))


def getActiveDraw():
    '''Returns the drawId of the currently active draw'''
    return int(requests.get('https://api.opap.gr/draws/v3.0/1100/active').json()['drawId'])


'''---------------------------------------------------------------------------------'''

'''--------------------------FUNCTIONS FOR collectNums.py---------------------------'''

'''---------------------------------------------------------------------------------'''


def readFromDB():
    '''Selects all rows in DB and returns them in an array, where Array[i][0] is the drawID and
    Array[i][1] is a list of the winning numbers.

    You have to declare a constant 'DB' at the top of the 'functions.py' file for the function to know which
    database to use.

    eg: DB = 'kino.db'

    Also, make sure the *****.db file is in the same folder with the script!
    '''
    temp = []
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    for row in c.execute('SELECT DISTINCT * FROM kino ORDER BY drawid'):
        temp1 = []
        temp1.append(row[0])
        temp1.append(stringToInt(row[1]))
        temp.append(temp1)
    return temp


def createCounter():
    '''Returns an array used for counting frequencies. Array[i][0] is the counter and Array[i][1]
    is the number, whose frequency we count. In this case, the numbers are 1-80.
    '''
    temp = []
    for i in range(80):
        temp1 = []
        temp1.append(0)
        temp1.append(i+1)
        temp.append(temp1)
    return temp


def countNums(data, cnt):
    '''Takes as argument 2 2-D arrays:

    1. the array where our data is saved

    2. the counter array we created

    and returns the cnt (counter array),
    sorted by frequency of appearance.
    '''
    for i in range(len(data)):
        for j in range(len(data[i][1])):
            cnt[data[i][1][j]-1][0] += 1
    cnt = sortArray(cnt)


def writeCSV(arr):
    '''Writes each row of the arr to a .csv file, using a comma as a delimiter.
    '''
    print("Enter the .csv file name (for example: 'mydata'): ")
    fileName = input()
    fileName = fileName+'.csv'
    with open(fileName, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in arr:
            filewriter.writerow(row)


def writeCSV2(arr):
    '''Writes each row of the arr to a .csv file, using a comma as a delimiter.
    '''
    print("Enter the .csv file name (for example: 'mydata'): ")
    fileName = 'AllCombos.csv'
    with open(fileName, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in arr:
            filewriter.writerow(row)
