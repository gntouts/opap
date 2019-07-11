from functions import *


def main():
    print("Reading from DB")
    sqlData = readFromDB()
    allDraws = []
    allSets = []
    for item in sqlData:
        allDraws.append(item[1])
    print("Calculating subsets")
    allSets = findSubsets([i for i in range(1, 81)], 5)
    print('Creating subset counter')
    cntSets = createSubCount(allSets)
    print('Initializing a shit ton of calculations')
    iterateSubsets(allDraws, cntSets)
    print("If you see this, then everything went well. I hope...")
    print("Sorting the chaos")
    sortArray(cntSets)
    print("Saving to .csv")
    writeCSV2(cntSets)
    print("Saving to SQLite")
    parseToDB2(cntSets)
    print('Finally, OVER!')


if __name__ == "__main__":
    main()
