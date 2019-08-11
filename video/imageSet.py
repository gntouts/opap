import imgkit
import sqlite3
import os

DB = 'okeanos.db'

def ifNotExists(drawid):
    return not(os.path.isfile('./img/'+str(drawid-704207)+'.jpg'))


def createDBTable():
    '''Creates table 'kino' inside the Database.

    You have to declare a constant 'DB' at the top of the 'functions.py' file
    for the function to know which database to use.

    eg: DB = 'kino.db'
    '''
    conn = sqlite3.connect(DB)
    query = 'CREATE TABLE IF NOT EXISTS kino (drawid INTEGER, winning TEXT)'
    with conn:
        c = conn.cursor()
        c.execute(query)


def insertData(arg1, arg2):
    '''Takes arg1 and arg2 and inserts them as drawId
    and winning numbers into table kino.

    drawId=arg1, winning=arg2

    arg2 must be a STRING containing the winning numbers
    separated by single spaces.

    eg: arg2='4 54 21 4'

    '''
    con = sqlite3.connect(DB)
    with con:
        c = con.cursor()
        c.execute("""INSERT INTO kino (drawid,
                    winning)
                    VALUES (:drawid,
                    :winning)""",
                  {'drawid': arg1, 'winning': arg2})


def stringToInt(arr):
    '''Takes as argument a string of numbers divided by whitespaces
    and returns an array of these numbers.

    For example: "1 23 54" returns [1, 23, 54]'''
    arr = arr.split()
    for i in range(len(arr)):
        arr[i] = int(arr[i])
    return arr


def search(arr, val):
    for i in range(len(arr)):
        if arr[i] == val:
            return True
    return False


def createHTML(row):
    drawid = row[0]
    results = stringToInt(row[1])
    source = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
        <style>
        .top {
            text-align: center;
        }

        table {
            width: 1450px;
            height: 980px;
            margin: 0 auto;
        }
        body{
            width:1920px;
            height:1080px;
        }
    h1{
        font-size: xx-large;
    }
        td {
            text-align: center;
            border-radius: 49%;
            border: 5%;
            font-size: xx-large;
        }

        .win {
            background-color: crimson;
            color: white;
        }
        </style>
    </head>
    <body>
        <div class="top">'''
    source = source + createHead(drawid)
    source = source + '''</div><div>'''
    source = source + createTable(results)
    source = source + "</div></body></html>"
    return source


def createTable(results):
    source = "<table>"
    for i in range(8):
        source = source + "<tr>"
        for j in range(10):
            a = 10*i+j+1
            if search(results, a):
                source = source + '''<td class="win">''' + str(a)+"</td>"
            else:
                source = source + '''<td>''' + str(a)+"</td>"
        source = source + "</tr>"
    source = source + "</table>"
    return source


def createHead(drawid):
    return "<h1>"+str(drawid)+"</h1>"


def createImage(row):
    options = {
        'quiet': '',
        'disable-smart-width': '',
        'height': '1080',
        'width': '1920'
    }
    myHTML = createHTML(row)
    imgkit.from_string(
        myHTML, './img/'+str(row[0]-704207)+'.jpg', options=options)


def main():
    os.system("mkdir img")
    createDBTable()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    k = 0
    xd = 0
    results = c.execute('SELECT DISTINCT * FROM kino ORDER BY drawid')
    for row in results:
        if ifNotExists(row[0]):
            createImage(row)


if __name__ == "__main__":
    main()
