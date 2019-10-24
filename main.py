# Intertag
# Interactive metadata enditor for audio files

import sys
import mutagen

ARTIST_KEY = 'TPE1'
ALBUM_ARTIST_KEY = 'TPE2'
ALBUM_KEY = 'TALB'
TITLE_KEY = 'TIT2'
TRACK_NUM_KEY = 'TRCK'
METADATA_KEYS = [
    ARTIST_KEY,
    ALBUM_ARTIST_KEY,
    ALBUM_KEY,
    TITLE_KEY,
    TRACK_NUM_KEY,
]

# Yeah, it's a bunch of globals.  Sue me.  It's a 100 line python script to
# help manage metadata for mp3 songs, I think I can bear to deal with a handful
# of global maps
cache = {
    ARTIST_KEY: [],
    ALBUM_KEY: {},  # Indexed by artist name
}

field_names = {
    ARTIST_KEY:       "Artist Name",
    ALBUM_ARTIST_KEY: "Album Artist",
    ALBUM_KEY:        "Album Title",
    TITLE_KEY:        "Song Title",
    TRACK_NUM_KEY:    "Track Number",
}

validExtensions = ['mp3']


def resetCursor():
    """Clear the page and set the cursor to the top left"""
    print(u"\u001b[2J")
    print(u"\u001b[0;0H")


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


def valueForKeyInMutagenFile(key, mutagenFile):
    if key in mutagenFile:
        return mutagenFile[key].text[0]
    return ''


def addExistingMetadataToCache(f):
    for k in METADATA_KEYS:
        if k in f and valueForKeyInMutagenFile(k, f) not in cache[k]:
            cache[k].append(valueForKeyInMutagenFile(k, f))


def printFileInfo(fname, f):
    # Print the file info to the terminal
    print("** FILE: " + fname)
    print("")  # Skip a line
    print("Artist Name   : " + valueForKeyInMutagenFile(ARTIST_KEY, f))
    print("Album Artist  : " + valueForKeyInMutagenFile(ALBUM_ARTIST_KEY, f))
    print("Album Name    : " + valueForKeyInMutagenFile(ALBUM_KEY, f))
    print("Track Title   : " + valueForKeyInMutagenFile(TITLE_KEY, f))
    print("Track Number  : " + valueForKeyInMutagenFile(TRACK_NUM_KEY, f))
    print("")  # Skkp a line


def generateTagFrameForKey(k, v):
    if k == ARTIST_KEY:
        return mutagen.id3.TPE1(encoding=3, text=v)
    elif k == ALBUM_ARTIST_KEY:
        return mutagen.id3.TPE2(encoding=3, text=v)
    elif k == ALBUM_KEY:
        return mutagen.id3.TALB(encoding=3, text=v)
    elif k == TITLE_KEY:
        return mutagen.id3.TIT2(encoding=3, text=v)
    elif k == TRACK_NUM_KEY:
        return mutagen.id3.TRCK(encoding=3, text=v)
    else:
        raise KeyError(k)


def completeArtist(filename, mutagenFile):
    """
    Fill and save the artist information, return true if the user wants to
    skip to the next song
    """

    # Print our cache for this key
    print("(i) - Type new value")
    print("(s) - Skip field")
    print("(n) - Next song")
    for i, v in enumerate(cache[ARTIST_KEY]):
        print("(%d) - %s" % (i, v))

    print("")
    i = input("%13s : " % (field_names[ARTIST_KEY]))

    if i == "s" or i == "n":
        return i == "n"

    if i == "i":
        i = input("    New Value : ")
        if i not in cache[ARTIST_KEY]:
            cache[ARTIST_KEY].append(i)
        else:
            i = cache[ARTIST_KEY][cache[ARTIST_KEY].index(i)]
    else:
        i = cache[ARTIST_KEY][int(i)]

    mutagenFile[ARTIST_KEY] = generateTagFrameForKey(ARTIST_KEY, i)
    mutagenFile[ALBUM_ARTIST_KEY] = generateTagFrameForKey(ALBUM_ARTIST_KEY, i)
    mutagenFile.save(filename)
    return False


def completeMetadata(filename, mutagenFile):
    # Fill metadata for each key
    for k in METADATA_KEYS:
        # Reset the cursor and print info that we've filled
        resetCursor()
        printFileInfo(filename, mutagenFile)

        v = False
        if k == ARTIST_KEY:
            v = completeArtist(filename, mutagenFile)
        elif k == ALBUM_ARTIST_KEY:
            continue  # Skip because we do both artist + album artist above
        elif k == ALBUM_KEY:
            # Complete Album
            continue
        elif k == TITLE_KEY:
            # Complete title
            continue
        elif k == TRACK_NUM_KEY:
            # Complete title
            continue

    return


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
