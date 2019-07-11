from functions import *

def main():
    sqlData = readFromDB()
    numCount = createCounter()
    countNums(sqlData, numCount)
    writeCSV(numCount)

if __name__ == "__main__":
    main()