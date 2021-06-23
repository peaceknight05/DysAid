# in-built libraries
import random

# third-party libraries
import pronouncing

# local libraries
from substitute import Substitute

class Guide:
    """
    python class to convert words to word segments and graphemes
    ARPABET: https://www.wikiwand.com/en/ARPABET
    CMU Pronouncing Dictionary: http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=C+M+U+Dictionary
    """

    class InvalidWordException(Exception):
        """exception for invalid words passed to the convert function"""

        def __init__(self, invalid):
            """initialisation method to create an error message from the invalid word provided"""

            super().__init__(f"\"{invalid}\" is not a valid word")

    # hard-coded woel phonemes
    vowels = ["AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"]

    def phonemes(a):
        """
        python function to split a word into ARPAbet phonemes
        params:
            a (string)
            - the word to split
        output:
            array
            - an array of strings containing the ARPAbet phonemes of the word
        """

        # use third-party library to split word into phonemes
        try:
            p = pronouncing.phones_for_word(a)[0].split(" ")
        except IndexError: # input vailidation - handled by third-party library, throws custom error
            raise Guide.InvalidWordException(a)

        pa = [x[:-1] if x[-1] in ["0", "1", "2"] else x for x in p] # remove stress markings

        return pa

    def syl(a):
        """
        python function to split a word into space-separated syllables
        params:
            a (array of strings)
            - the phonemes of the word to generate syllables for
        output:
            array
            - an array of strings containing the syllables of the word
        """

        syllables = [] # array to store the syllables
        pointer = -1 # "pointer" to point at the end of the last syllable

        # algorithm for splitting word (as phoneme collection) into syllables
        # algorithm is self-designed; covers common patterns and is funcitonally
        # sufficient for intended purpose.
        for i, p in enumerate(a): # i is the index of the phoneme and p is the phoneme
            if p in Guide.vowels:
                # case 1: there are 3 or more phonemes in front of the current phoneme
                if len(a) >= (i+1)+3:
                    # case 1.1: syllable pattern is prev phonemes + vowel + con/vow + con/vow
                    if a[i+1] in Guide.vowels:
                        syllables.append(" ".join(a[pointer+1:i+1]))
                        pointer = i
                    # case 1.2: syllable pattern is prev phonemes + consonant + vowel + consonant
                    elif (not a[i+1] in Guide.vowels) and (a[i+2] in Guide.vowels) and (not a[i+3] in Guide.vowels):
                        syllables.append(" ".join(a[pointer+1:i+1]))
                        pointer = i
                    # case 1.3: syllable pattern is prev phonemes + consonant + vowel + vowel
                    elif (not a[i+1] in Guide.vowels) and (a[i+2] in Guide.vowels) and (a[i+3] in Guide.vowels):
                        syllables.append(" ".join(a[pointer+1:i+1]))
                        pointer = i
                    # case 1.4: syllable pattern is prev phonemes + consonant + consonant + vowel
                    elif (not a[i+1] in Guide.vowels) and (not a[i+2] in Guide.vowels) and (a[i+3] in Guide.vowels):
                        syllables.append(" ".join(a[pointer+1:i+2]))
                        pointer = i+1
                    # case 1.5: syllable pattern is prev phonemes + consonant + consonant + consonant
                    elif (not a[i+1] in Guide.vowels) and (not a[i+2] in Guide.vowels) and (not a[i+3] in Guide.vowels):
                        syllables.append(" ".join(a[pointer+1:i+3]))
                        pointer = i+2
                # case 2: there are 2 or more phonemes in front of the current phoneme
                elif len(a) == (i+1)+2:
                    # case 2.1: syllable pattern is prev phonemes + vowel + con/vow
                    if a[i+1] in Guide.vowels:
                        syllables.append(" ".join(a[pointer+1:i+1]))
                        pointer = i
                    # case 2.2: syllable pattern is prev phonemes + consonant + consonant
                    elif (not a[i+1] in Guide.vowels) and (not a[i+2] in Guide.vowels):
                        syllables.append(" ".join(a[pointer+1:]))
                    # case 2.3: syllable pattern is prev phonemes + consonant + vowel
                    elif (not a[i+1] in Guide.vowels) and (a[i+2] in Guide.vowels):
                        syllables.append(" ".join(a[pointer+1:i+1]))
                        pointer = i
                # case 3: there is 1 phoneme in front of the current phoneme
                elif len(a) == (i+1)+1:
                    if a[i+1] in Guide.vowels: # case 3.1: syllable pattern is prev phonemes + vowel
                        syllables.append(" ".join(a[pointer+1:i+1]))
                        pointer = i
                    else: # case 3.2: catch-all for anything else
                        syllables.append(" ".join(a[pointer+1:]))
                # case 4: the current phoneme is the last phoneme
                else:
                    # case 4.1: catch-all for rare exceptions to all above cases
                    syllables.append(" ".join(a[pointer+1:]))
        return syllables

    def convert(word):
        """
        python function to convert a word into sub-words and graphemes
        params:
            word (string)
            - the word to convert
        output:
            generator (string)
            - yields the subword or grapheme for each syllable of the corresponding word
        raises:
            Guide.InvalidWordException
            - the word is not a valid word
        """

        # input cleaning-up; in case multiple words are entered, take only the first word
        ans = word.split(" ")[0]

        pa = Guide.phonemes(ans) # split word into phonemes

        sl = Guide.syl(pa) # split word into syllables using syl()
        # create arrays where the vowels in each syllable are of a certain stress marking
        sl0 = [" ".join([f"{b}0" if b in Guide.vowels else b for b in a.split()]) for a in sl]
        sl1 = [" ".join([f"{b}1" if b in Guide.vowels else b for b in a.split()]) for a in sl]
        sl2 = [" ".join([f"{b}2" if b in Guide.vowels else b for b in a.split()]) for a in sl]

        guide = [] # array to store guide

        for s in range(len(sl)): # for syllable in the word; using s as the index
            # get guiding words for each stress value
            # (strict search) guiding word contains ONLY the syllable
            zero = pronouncing.search(f"^{sl0[s]}$")
            one = pronouncing.search(f"^{sl1[s]}$")
            two = pronouncing.search(f"^{sl2[s]}$")

            # only take the five most common words if there are at least seven words,
            # else don't take any, as all the words are probably uncommon.
            zero = zero[:5] if len(zero) >= 7 else []
            one = one[:5] if len(one) >= 7 else []
            two = two[:5] if len(two) >= 7 else []

            word = zero+one+two # collate all guiding words

            plain = sl[s].split() # just the plain syllable as an array of strings

            # graphemes are used instead of plain raw phoneme data
            # as it is comparably more user-readable
            grapheme = Substitute.gets(plain) # temp store for grapheme generator
            gstring = "-".join(grapheme) # temp store for grapheme string

            if len(word) == 0: # if no guiding words can be found with strict search
                # get guiding words for each stress value
                # (non-strict search) guiding word CONTAINS the syllable
                zero = pronouncing.search(f"{sl0[s]}")
                one = pronouncing.search(f"{sl1[s]}")
                two = pronouncing.search(f"{sl2[s]}")

                # only take the five most common words if there are at least seven words,
                # else don't take any, as all the words are probably uncommon.
                zero = zero[:5] if len(zero) >= 7 else []
                one = one[:5] if len(one) >= 7 else []
                two = two[:5] if len(two) >= 7 else []

                word = zero+one+two # collate all guiding words

                if len(word) == 0: # if no words can be found with strict and non-strict search
                    guide.append([gstring, 2]) # use the grapheme of the syllable; type 2 guide
                else: # if words can be found with non-strict search
                    guide.append([gstring, random.choice(word), 1]) # add plain and guiding word; type 1 guide
            else:
                guide.append([gstring, random.choice(word), 0]) # add plain and guiding word; type 0 guide

        for a in guide: # for guide word/grapheme
            g = a[-1] # guide type (0, 1 or 2)

            if g == 2: # guiding word was not found with S and NS search; provide grapheme
                yield a[0]
            elif g == 1: # guiding word was found with NS search; provide plain and guide with type 1 formatting
                yield f"{a[0]} as in {a[1]}"
            else: # guiding word was found with S search; provide plain and guide with type 0 formatting
                yield f"{a[1]} ({a[0]})"