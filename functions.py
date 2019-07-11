import sqlite3
import csv
DB = 'kinodata.db'


def stringToInt(arr):
    '''Takes as argument a string of numbers divided by whitespaces
    and returns an array of these numbers.

    For example: "1 23 54" returns [1, 23, 54]
    '''
    arr = arr.split()
    for i in range(len(arr)):
        arr[i] = int(arr[i])
    return arr



def sortArray(arr):
    '''Sorts a 2-D array (arr) based on the values of the first "element" (arr[i][0]).
    '''
    def sortFirst(val): 
        return val[0]
    
    arr.sort(key = sortFirst, reverse = True)
    return arr



'''---------------------------------------------------------------------------------'''

'''--------------------------FUNCTIONS FOR collectNums.py---------------------------'''

'''---------------------------------------------------------------------------------'''



def readFromDB():
    '''Selects all rows in DB and returns them in an array, where Array[i][0] is the drawID and
    Array[i][1] is a list of the winning numbers.
    
    You have to declare a constant "DB" at the top of your file for the function to know which
    database to use. 
    
    eg: DB = 'kino.db'

    Also, make sure the *****.db file is in the same folder with the script!
    '''
    temp=[]
    conn = sqlite3.connect(DB)
    c =conn.cursor()
    for row in c.execute('SELECT DISTINCT * FROM kino ORDER BY drawid'):
        temp1=[]
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
        temp1=[]
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
            cnt[data[i][1][j]-1][0]+=1
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