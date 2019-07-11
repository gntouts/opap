from functions import *


def main():
    print("Initializing:")
    print("Creating Table...")
    conn = sqlite3.connect(DB)
    createTable()
    print("Table 'kino' created!")
    print("........................................................")
    print("Proceeding with requests...")
    print("This will take some time.")
    A = []
    getAllData(A)
    print("Done!")
    parseToDB(A)
    print("Writing data to the Database...")
    print("This will take some time.")


if __name__ == "__main__":
    main()
