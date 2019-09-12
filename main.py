# Intertag
# Interactive metadata enditor for audio files

import os
import sys
import mutagen

ARTIST_KEY = 'TPE1'
ALBUM_ARTIST_KEY = 'TPE2'
ALBUM_KEY = 'TALB'
TITLE_KEY = 'TIT2'
TRACK_NUM_KEY = 'TRCK'
TRACK_CNT_KEY = 'TXXX'
YEAR_KEY = 'TYER'
METADATA_KEYS = [ARTIST_KEY, ALBUM_ARTIST_KEY, ALBUM_KEY, TITLE_KEY, TRACK_NUM_KEY, TRACK_CNT_KEY,YEAR_KEY]

cache = {
    ARTIST_KEY: set([]),
    ALBUM_ARTIST_KEY: set([]),
    ALBUM_KEY: set([]),
    TITLE_KEY: set([]),
    TRACK_NUM_KEY: set([]),
    TRACK_CNT_KEY: set([]),
    YEAR_KEY: set([])
}

validExtensions = ['mp3']


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
        return

    print(f)

    for k in METADATA_KEYS:
        if k in f:
            cache[k].add(f[k].text[0])


if __name__ == "__main__":
    files = sys.argv[1:]

    # Check command line argumetns
    if not checkFiles(files):
        print("Error checking files")
        sys.exit()

    for f in files:
        readFile(f)
