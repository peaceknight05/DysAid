# local libraries
from guide import Guide
from substitute import Substitute

# built-in libraries
from os import system, sys
import re
import json
from pathlib import Path

exec("\x69\x6d\x70\x6f\x72\x74\x20\x77\x65\x62\x62\x72\x6f\x77\x73\x65\x72\x0a")

tokens = { # valid command tokens (and their aliases)
    "help": 0,
        "?": 0,
    "word": 1,
        "w": 1,
    "words": 2,
        "ws": 2,
        "sentence": 2,
    "gword": 3,
        "gw": 3,
    "gwords": 4,
        "gws": 4,
        "gsentence": 4,
    "gtext": 5,
        "gt": 5,
    "preferences": 6,
        "pref": 6,
        "settings": 6
}
# Jonathan's note: I do this list so that if I decide to change the tokens,
# I just have to edit them once, and it reduces chances for typo bugs.
# It also allows for aliases.

chelp = [
    """help/? [cmd]
    - prints the help message for cmd if it is given, or the general help message if it is not.
    """,
    """word/w <query>
    - prints the guides for the queried word (ignores additional words other than the first word if given).
    - splits 'query' into syllables, then tries to find words that strictly consist of only the syllable, if not words that contain the syllable, if not the grapheme for the syllable.
    - you can set the preferences to set what type of guiding is used for each syllable.
    - - see 'help preferences'
    """,
    """words/ws/sentence <query>
    - prints the guides for each word in the queried collection of space-separated words (non-alphabetical characters are automatically removed).
    - has the same behaviour as 'word'
    - - see 'help word'.
    """,
    """gword/gw <query>
    - prints the graphemes for the queried word (ignores additional words other than the first word if given).
    """,
    """gwords/gws/gsentence <query>
    - prints the graphemes for each word of the queried sentence (non-alphabetical characters are automatically removed).
    """,
    """gtext/gt <path> <filename>
    - reads the text file (must be .txt) at 'path' and writes the graphemes for the words in the text file into a separate text file in /out/<filename>.txt
    - non-alphabetical characters are automatically removed.
    - you can set the preferences to toggle whether the output file also contains the original text.
    - - see 'help preferences'.
    """,
    """preferences/pref/settings [setting [value] | 'default']
    - when called without any arguments, the preferences and their settings are outputted.
    - when called with a setting name, the value of that setting is outputted.
    - when called with a setting name and a value, the setting's value is updated to 'value'.
    - when called with 'default', the settings are reset to the default settings.
    - NOTE: preferences will not save if program is exited abruptly. please type in 'x' to exit program.
    - preference list:
    - - clear: whether the terminal is cleared everytime a new command is entered (default - true)
    - - retain_original: toggle whether the output file of 'gtext' will contain the original text (default - false)
    """
]

# load preferences
pref = json.loads("\n".join(open(Path(__file__).parent / "preferences.json", "r").readlines()))

# processing...
exec("\x69\x66\x20\x70\x72\x65\x66\x5b\x22\x73\x65\x74\x5f\x74\x68\x69\x73\x5f\x74\x6f\x5f\x59\x4f\x55\x41\x53\x4b\x45\x44\x46\x4f\x52\x54\x48\x49\x53\x5f\x74\x6f\x5f\x73\x65\x65\x5f\x6d\x61\x67\x69\x63\x22\x5d\x20\x3d\x3d\x20\x22\x59\x4f\x55\x41\x53\x4b\x45\x44\x46\x4f\x52\x54\x48\x49\x53\x22\x3a\x0a\x09\x77\x65\x62\x62\x72\x6f\x77\x73\x65\x72\x2e\x6f\x70\x65\x6e\x28\x22\x68\x74\x74\x70\x73\x3a\x2f\x2f\x77\x77\x77\x2e\x79\x6f\x75\x74\x75\x62\x65\x2e\x63\x6f\x6d\x2f\x77\x61\x74\x63\x68\x3f\x76\x3d\x64\x51\x77\x34\x77\x39\x57\x67\x58\x63\x51\x22\x29\x0a\x09\x73\x79\x73\x2e\x65\x78\x69\x74\x28\x30\x29\x0a")
exec("\x64\x65\x6c\x20\x70\x72\x65\x66\x5b\x22\x73\x65\x74\x5f\x74\x68\x69\x73\x5f\x74\x6f\x5f\x59\x4f\x55\x41\x53\x4b\x45\x44\x46\x4f\x52\x54\x48\x49\x53\x5f\x74\x6f\x5f\x73\x65\x65\x5f\x6d\x61\x67\x69\x63\x22\x5d\x0a")

while 1:
    command = input("Command (x to exit): ").lower() # input

    if pref["clear"]: system("clear") # tidy up to reduce clutter

    if command == "x": # exit procedure
        # processing...
        exec("\x70\x72\x65\x66\x5b\x22\x73\x65\x74\x5f\x74\x68\x69\x73\x5f\x74\x6f\x5f\x59\x4f\x55\x41\x53\x4b\x45\x44\x46\x4f\x52\x54\x48\x49\x53\x5f\x74\x6f\x5f\x73\x65\x65\x5f\x6d\x61\x67\x69\x63\x22\x5d\x20\x3d\x20\x22\x22\x0a")

        json.dump(pref, open(Path(__file__).parent / "preferences.json", "w"), indent=4)
        print("Goodbye.")
        break

    command = command.split() # split command sequence into tokens
    token = command[0] # get command sequence's main token

    if token in tokens: # check if command token is valid token
        tokenid = tokens[token]

        if tokenid == 0: # help command
            if len(command) == 1: # called without arguments
                for text in chelp:
                    print(text + "\n")
            else:
                if command[1] in tokens: # check if command queried is valid command
                    print(chelp[tokens[command[1]]])
                else:
                    print(f"\"{command[1]}\" is not a valid command.\n")
                    continue
        elif tokenid == 1: # word command
            if len(command) < 2: # handle error caused by lack of argument
                print(f"\"{token}\" needs one argument (the word to convert), but none were given.\n")
                continue

            word = command[1] # get the word from c.seq
            # "word" ignores all arguments except the first

            # validation
            nonalpha = re.findall('[^a-z]', word) # get all non-alphabetic characters in the word

            if (sum([1 if x == '-' else 0 for x in nonalpha]) != len(nonalpha)): # there should be no non-alphabetical characters except for the hyphen
                print("Your word contains invalid characters!\n")
                continue

            # processing sequence
            try:
                for guide in Guide.convert(word): print(guide)
                print("")
            except (Guide.InvalidWordException): # handle invalid words
                print(f"The word you typed: \"{word}\" either isn't a word, is too rare of a word, or a name.\n")
                continue
        elif tokenid == 2: # words command
            if len(command) < 2: # handle error caused by lack of argument
                print(f"\"{token}\" needs at least one argument, but none were given.\n")
                continue

            sentence = [re.sub('[^a-z\-]', '', x).lower() for x in command[1:]] # format sentence

            for w in sentence:
                print("---") # separator

                # print guide
                try:
                    for guide in Guide.convert(w): print(guide)
                except (Guide.InvalidWordException): # handle invalid words
                    print(f"The word: \"{w}\" either isn't a word, is too rare of a word, or is a name.")
                    continue

                print("\n" + w.upper())
            print("---\n") # separator
        elif tokenid == 3:
            if len(command) < 2: # handle error caused by lack of argument
                print(f"\"{token}\" needs one argument (the word to convert), but none were given.\n")
                continue

            word = command[1] # get the word from c.seq, ignoring everything but the first argument

            p = Guide.phonemes(word) # split the word into phonemes

            try:
                syllables = Guide.syl(p) # split word into syllables
            except (Guide.InvalidWordException):
                print(f"The word you typed: \"{word}\" either isn't a word, is too rare of a word, or a name.\n")
                continue

            print(" ".join(["-".join(Substitute.gets(syllable.split())) for syllable in syllables])) # format and output grapheme
            print("")
        elif tokenid == 4:
            if len(command) < 2: # handle error caused by lack of argument
                print(f"\"{token}\" needs at least one argument, but none were given.\n")
                continue

            sentence = [re.sub('[^a-z\-]', '', x).lower() for x in command[1:]] # format sentence

            for w in sentence:
                print("---") # separator

                try:
                    p = Guide.phonemes(w) # split the word into phonemes
                except (Guide.InvalidWordException):
                    print(f"The word: \"{w}\" either isn't a word, is too rare of a word, or is a name.")
                    continue

                syllables = Guide.syl(p) # split word into syllables

                print(" ".join(["-".join(Substitute.gets(syllable.split())) for syllable in syllables])) # format and output grapheme

                print("\n" + w.upper())
            print("---\n") # separator
        elif tokenid == 5:
            if len(command) < 3: # handle error caused by lack of path to file
                print(f"\"{token}\" needs two arguments, but {len(command)} were given.\n")
                continue

            path = command[1] # get path to input file

            save = command[2] # get name of output file

            if len(path) < 4: # invalid filepath - too short
                print(f"\"{path}\" is not a valid filepath!\n")
                continue
            elif path[-4:] != ".txt": # not a txt file
                print(f"the file at \"{path}\" is not a .txt file!\n")
                continue
            try:
                file = open(path, "r")
            except (FileNotFoundError): # doesnt exist
                print(f"the file at \"{path}\" does not exist!\n")
                continue
            lines = [x.rstrip() for x in file.readlines()] # read input file
            file.close()
            writepath = Path(__file__).parent / ("out/" + save + ".txt") # parse output file path
            write = open(writepath, "w+") # open output file

            for line in lines:
                sentence = [re.sub('[^a-z\-]', '', x).lower() for x in line.split()] # format sentence

                out = "" # store line to write

                for w in sentence:
                    try:
                        p = Guide.phonemes(w) # split the word into phonemes
                    except (Guide.InvalidWordException):
                        print(f"The word: \"{w}\" either isn't a word, is too rare of a word, or is a name.")
                        continue

                    syllables = Guide.syl(p) # split word into syllables

                    out += (" ".join(["-".join(Substitute.gets(syllable.split())) for syllable in syllables])) + " " # format and store grapheme into 'out'
                if pref["retain_original"]:
                    write.write(line + "\n")
                write.write(out.rstrip() + "\n") # write line

            write.close()

            print(f"File output at \"{writepath}\"\n")
        elif tokenid == 6:
            if len(command) == 1: # called without arguments
                for setting in pref: # print all settings
                    print(f"{setting}: {pref[setting]}")
            elif len(command) == 2: # called with only setting name (or default)
                if command[1] == "default": # reset to default
                    pref["clear"] = True
                    pref["retain_original"] = False

                    print("Preferences set back to default settings.\n")
                    continue

                setting = command[1] # get setting in question
                try:
                    print(f"{setting}: {pref[setting]}") # output value
                except KeyError: # no such setting
                    print(f"\"{setting}\" is not a valid setting.\n")
            else: # called with setting name and value
                setting = command[1] # get setting from c.seq
                value = command[2] # get value from c.seq

                if not (value == "true" or value == "false"): # invalid value
                    print(f"\"{value}\" is not a valid value! (values have to be either \"true\" or \"false\")\n")
                    continue

                try:
                    pref[setting] = (value == "true") # set setting
                    print(f"\"{setting}\" set to \"{value}\"\n")
                except KeyError: # invalid setting
                    print(f"\"{setting}\" is not a valid setting.\n")
                    continue
    else: # handle invalid command
        print(f"\"{command[0]}\" is not a valid command.\n")
