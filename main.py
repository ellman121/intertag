# Intertag
# Interactive metadata enditor for audio files

import os
import sys
import mutagen

validExtensions = ['mp3']
artistList = []
albumList = []


def checkFiles(filelist):
    for f in filelist:
        ext = f.split('.')[-1]
        if not os.path.isfile(f) or ext not in validExtensions:
            print("Invalid file: %s" % (f))
            return False
    return True


def readFile(f):
    try:
        f = mutagen.File(f)
    except mutagen.MutagenError as e:
        print("Error parsing file")
        print(e)
    
    print(f)


if __name__ == "__main__":
    files = sys.argv[1:]

    # Check command line argumetns
    if not checkFiles(files):
        print("Error checking files")
        sys.exit()
    
    for f in files:
        readFile(f)
            
