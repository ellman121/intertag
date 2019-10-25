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
    ALBUM_KEY,
    TITLE_KEY,
    TRACK_NUM_KEY,
]

# Yeah, it's a bunch of globals.  Sue me.  It's a 100 line python script to
# help manage metadata for mp3 songs, I think I can bear to deal with a handful
# of global maps
cache = {
    ARTIST_KEY: [],  # Set of artist names (as strings)
    ALBUM_KEY: [],   # Set of (artist, album) tuples
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
        if k == ARTIST_KEY and k in f:
            s = set(cache[k])
            s.add(valueForKeyInMutagenFile(k, f))
            cache[k] = list(s)
        elif k == ALBUM_KEY and k in f:
            pair = (
                valueForKeyInMutagenFile(ARTIST_KEY, f),
                valueForKeyInMutagenFile(ALBUM_KEY, f)
            )

            s = set(cache[k])
            s.add(pair)
            cache[k] = list(s)

    cache[ARTIST_KEY].sort()
    cache[ALBUM_KEY].sort()


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


def cachedAlbumsForArtist(artistName):
    return list(filter(lambda t: t[0] == artistName, cache[ALBUM_KEY]))


def printCacheForKey(k, artistName):
    if k == ARTIST_KEY or k == ALBUM_ARTIST_KEY:
        for i, v in enumerate(cache[ARTIST_KEY]):
            print("(%d) - %s" % (i, v))
    elif k == ALBUM_KEY:
        if len(cache[ALBUM_KEY]) > 0:
            for i, v in enumerate(cachedAlbumsForArtist(artistName)):
                print("(%d) - %s" % (i, v[1]))

    print("")


def completeMetadata(filename, mutagenFile):
    # Fill metadata for each key
    for k in METADATA_KEYS:
        # Get the current artist because we need it to filter our cache prompt
        currentArtist = valueForKeyInMutagenFile(ARTIST_KEY, mutagenFile)

        # Reset the cursor and print info that we've filled
        resetCursor()
        printFileInfo(filename, mutagenFile)

        # Print our prompt
        print("(s) - Skip field")
        print("(n) - Next song")

        if k == ARTIST_KEY or k == ALBUM_KEY:
            print("(i) - Type new value")
            printCacheForKey(k, currentArtist)

        i = input("%13s : " % (field_names[k]))

        if i == "s":
            continue

        if i == "n":
            return

        if k == TRACK_NUM_KEY or k == TITLE_KEY:
            mutagenFile[k] = generateTagFrameForKey(k, i)
            mutagenFile.save(filename)
            continue

        # If the user wants to input a new value
        if i == "i":
            i = input("    New Value : ")
            v = i
            if k == ALBUM_KEY:
                v = (currentArtist, i)

            s = set(cache[k])
            s.add(v)
            cache[k] = list(s)
            cache[k].sort()

        # If the user selected an option
        else:
            if k == ARTIST_KEY:
                i = cache[k][int(i)]
            elif k == ALBUM_KEY:
                i = cachedAlbumsForArtist(currentArtist)[int(i)][1]

        if k == ARTIST_KEY:
            mutagenFile[ALBUM_ARTIST_KEY] = generateTagFrameForKey(
                                                ALBUM_ARTIST_KEY, i)

        mutagenFile[k] = generateTagFrameForKey(k, i)
        mutagenFile.save(filename)


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
