# Intertag
# Interactive metadata enditor for audio files

import pprint
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

# Yeah, it's a global.  Sue me, it's a 100 line python script to help manage metadata for mp3 tiles
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
    ret = []
    for f in filelist:
        try:
            with open(f, 'rb') as fle:
                f = mutagen.File(fle)
                ret.append(f)
        except mutagen.MutagenError as e:
            print("File unacceptable", e)
            return ([], False)
    return (ret, True)


def valueForKey(key, mutagenFile):
    if key in mutagenFile:
        return mutagenFile[key].text[0]
    
    return ''


def addExistingMetadataToCache(f):
    for k in METADATA_KEYS:
        if k in f:
            cache[k].add(valueForKey(k, f))


def printFileInfo(filename, mutagenFile):
    # Print the file info to the terminal
    print("** FILE: " + filename + "\n")
    print("Artist Name   : " + valueForKey(ARTIST_KEY, mutagenFile))
    print("Album Artist  : " + valueForKey(ALBUM_ARTIST_KEY, mutagenFile))
    print("Album Name    : " + valueForKey(ALBUM_KEY, mutagenFile))
    print("Year Released : " + valueForKey(YEAR_KEY, mutagenFile))
    print("Track Title   : " + valueForKey(TITLE_KEY, mutagenFile))
    print("Track Number  : " + valueForKey(TRACK_NUM_KEY, mutagenFile))
    print("Total Tracks  : " + valueForKey(TRACK_CNT_KEY, mutagenFile))


def completeMetadata(filename, mutagenFile):
    printFileInfo(filename, mutagenFile)


if __name__ == "__main__":
    files = sys.argv[1:]

    # Check files on the way in
    mutagenFiles, ok = checkFiles(files)
    if not ok:
        print("Error checking files")
        sys.exit()

    print("Reading in files, building metadta cache")
    for f in mutagenFiles:
        addExistingMetadataToCache(f)
    print("Existing metadata added to cache")

    for fname, mutafile in zip(files, mutagenFiles):
        completeMetadata(fname, mutafile)
