# Intertag
# Interactive metadata enditor for audio files

import os
import sys
import mutagen

ARTIST_KEY = 'TPE1'
ALBUM_KEY = 'TALB'
TITLE_KEY = 'TIT2'
TRACK_NUM_KEY = 'TRCK'
YEAR_KEY = 'TDRC'
METADATA_KEYS = [ARTIST_KEY, ALBUM_KEY, TITLE_KEY, TRACK_NUM_KEY, YEAR_KEY]

validExtensions = ['mp3']
artistList = []
albumList = []
yearList = []


def checkFiles(filelist):
    for f in filelist:
        ext = f.split('.')[-1]
        if not os.path.isfile(f) or ext not in validExtensions:
            print("Invalid file: %s" % (f))
            return False
    return True


def readFile(f):
    try:
        with open(f, 'rb') as fle:
            f = mutagen.File(fle)
    except mutagen.MutagenError as e:
        print("File unacceptable", e)

    for k in METADATA_KEYS:
        if k == ARTIST_KEY:
            artistList.append(f[ARTIST_KEY])
        elif k == ALBUM_KEY:
            albumList.append(f[ALBUM_KEY])
        elif k == YEAR_KEY:
            yearList.append(f[YEAR_KEY])


if __name__ == "__main__":
    files = sys.argv[1:]

    # Check command line argumetns
    if not checkFiles(files):
        print("Error checking files")
        sys.exit()
    
    for f in files:
        readFile(f)
            
