import argparse
import sqlite3

selectQuery = "select id_local, pathFromRoot from aglibraryfolder where pathFromRoot"
updateQuery = "update aglibraryfolder set pathFromRoot = ? where id_local = ?"

vowelMap = {"b5cc81":   "ad",   # έ
            "5cc81":    "d",    # ύ
            "ebfcc81":  "f8c",  # ό
            "b1cc81":   "ac",   # ά
            "b9cc81":   "af",   # ί
            "9cc81":    "e",    # ώ
            "b7cc81":   "ae"    # ή
            }

def main():
    args = getArgs()
    print("loading lightroom catalog: ", args.dbPath)

    con, cur = loadDb(args.dbPath)
    res = cur.execute(selectQuery)

    updatedFolders = []
    for folder in res.fetchall():
        updatedFolder = processFolder(folder)
        if updatedFolder is not None:
            updatedFolders.append(updatedFolder)

            if len(updatedFolders) % 10 == 0:
                print("identified {len:d} folder names".format(len = len(updatedFolders)))

    for updatedFolder in updatedFolders:
        try:
            con.execute(updateQuery, (updatedFolder[1], updatedFolder[0]))
        except sqlite3.Error:
            print("error updating: {local_id:d} to {path:s}".format(local_id = updatedFolder[0], path = updatedFolder[1]))


    if args.dryRun:
        con.rollback()
    else:
        con.commit()
    con.close()

    if args.verbose is True:
        print(updatedFolders)

    print(f"updated {len(updatedFolders)} folder names")

def getArgs():
    parser = argparse.ArgumentParser(
        prog = 'LightroomPathFixer',
        description = 'fix greek vowels in lightroom folder paths')
    parser.add_argument('-d', '--db', dest = 'dbPath', action='store')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument('-r', '--dry-run', dest='dryRun', action='store_true')
    return parser.parse_args()

def processFolder(folder):
    pathInHex = folder[1].encode('utf-8').hex()
    pathChanged = False
    for badVowel in vowelMap.keys():
        if badVowel in pathInHex:
            pathInHex = pathInHex.replace(badVowel, vowelMap.get(badVowel))
            pathChanged = True

    if pathChanged:
        return [folder[0], bytes.fromhex(pathInHex).decode("UTF-8")]

def loadDb(fileName):
    con = sqlite3.connect(fileName)
    cur = con.cursor()
    return con, cur

if __name__ == "__main__":
    main()