class Substitute:
    """this class converts phoneme(s) to grapheme(s)"""

    # hard-coded conversion, sourced from offical conversion chart with edits
    # (ARPAbet to grapheme)
    # source: https://www.dyslexia-reading-well.com/44-phonemes-in-english.html (IPA to grapheme)
    # Jonathan note:
    # not very elegant, but it gets it done
    # one drawback is that because it is hard-coded,
    # the graphemes are independant and isolated from inter-word context
    # whereas real graphemes change depending on surrounding phonemes and what would make the most sense.
    # however, given that each phoneme sounds almost (albeit not entirely) exactly the same,
    # this wouldn't affect it terribly, and it should be functionally sufficient
    sub = { # order follows linked source
        # vowels
        "AE": "ae",
        "EY": "eigh",
        "EH": "eh",
        "IY": "ee",
        "IH": "ih",
        "AY": "igh",
        "AA": "au", # ARPAbet limitation: open back rounded and unrounded is the same
        "OW": "ough", # note that this is incredibly similar to UW, AW, and AO
        "UH": "oo",
        "AH": "ah",
        "UW": "oogh", # note that this is incredibly similar to OW, AW and AO
        "OY": "oy",
        "AW": "augh", # note that this is incredibly similar to OW, UW and AO
        "AX": "er",
        "AXR": "ayer",
        "ER": "ur",
        "AO": "aw",# note that this is incredibly similar to OW, UW and AW
        # ARPAbet limitation: no ɪɚ or ʊɚ


        # consonants
        "B": "b",
        "D": "d",
        "F": "f",
        "G":"g",
        # "H": "h",
        "HH": "h",
        "JH": "dge",
        "K": "k",
        "L": "l",
        "M": "m",
        "N": "n",
        "P": "p",
        "R": "r",
        "S": "s",
        "T": "t",
        "V": "v",
        "W": "w",
        "Z": "z",
        "ZH": "zh", # this is increadibly similar to SH, except that it's voiced
        "CH": "ch",
        "SH": "sh", # this is icredibly similar to ZH, except that it's not voiced
        "TH": "th", # this is incredibly similar to DH, except that it's not voiced.
        "DH": "th", # this is incredibly similar to TH, except that it's voiced.
        "NG": "ng",
        "Y": "y"
    }

    def get(phoneme):
        """
        params:
            phoneme (string)
            - one phoneme to convert into a grapheme
        output:
            string
            - the corresponding grapheme for the phoneme
        """

        return Substitute.sub[phoneme]

    def gets(phonemes):
        """
        params:
            phonemes (array of strings)
            - list of phonemes to convert into graphemes
        output:
            generator (string)
            - yields the grapheme for each phoneme at each step
        """

        for phoneme in phonemes:
            yield Substitute.get(phoneme)