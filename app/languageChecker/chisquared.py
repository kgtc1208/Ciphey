"""
 ██████╗██╗██████╗ ██╗  ██╗███████╗██╗   ██╗
██╔════╝██║██╔══██╗██║  ██║██╔════╝╚██╗ ██╔╝
██║     ██║██████╔╝███████║█████╗   ╚████╔╝ 
██║     ██║██╔═══╝ ██╔══██║██╔══╝    ╚██╔╝  
╚██████╗██║██║     ██║  ██║███████╗   ██║ 
© Brandon Skerritt
Github: brandonskerritt

Class calculates the Chi squared score
"""

import mathsHelper
from string import punctuation
# I had a bug where empty string was being added to letter freq dictionary
# this solves it :)
punctuation += " "
class chiSquared:
    """Class that calculates the Chi squared score and tries to work out what language it might be
    to add a new language, go into this class (/app/languageChecker/chisquared.py)
    Find "self.languages" and add it to the dictionary like "German":[0.789, 0.651...]
    The list is the letter frequency ordered in alphabetical order """
    def __init__(self):
        self.languages = {
            "English":
            [0.0855, 0.0160, 0.0316, 0.0387, 0.1210,0.0218, 0.0209, 0.0496, 0.0733, 0.0022,0.0081, 0.0421, 0.0253, 0.0717, 0.0747,0.0207, 0.0010, 0.0633, 0.0673, 0.0894,0.0268, 0.0106, 0.0183, 0.0019, 0.0172,0.0011]
            #{'A': 8.12, 'B': 1.49, 'C': 2.71, 'D': 4.32, 'E': 12.02, 'F': 2.3, 'G': 2.03, 'H': 5.92, 'I': 7.31, 'J': 0.1, 'K': 0.69, 'L': 3.98, 'M': 2.61, 'N': 6.95, 'O': 7.68, 'P': 1.82, 'Q': 0.11, 'R': 6.02, 'S': 6.28, 'T': 9.1, 'U': 2.88, 'V': 1.11, 'W': 2.09, 'X': 0.17, 'Y': 2.11, 'Z': 0.07}
        }
        self.average = 0.0
        self.totalDone = 0.0
        self.oldAverage = 0.0
        self.mh = mathsHelper.mathsHelper()
        self.highestLanguage = ""
        self.totalChi = 0.0

        # these are settings that may impact how the program works overall
        self.chiSquaredSignificaneThreshold = 20
        self.totalDoneThreshold = 10
    def checkChi(self, text):
        """Checks to see if the Chi score is good
        if it is, it returns True
        Call this when you want to determine whether something is likely to be Chi or not
        
        Arguments:
            * text - the text you want to run a Chi Squared score on
        
        Outputs:
            * True - if it has a significantly lower chi squared score
            * False - if it doesn't have a significantly lower chi squared score
        """
        # TODO 20% isn't optimal
        # runs after every chi squared to see if it's 1 significantly lower than averae
        # the or statement is bc if the program has just started I don't want it to ignore the 
        # ones at the start
        self.chiSquared(text)
        if self.mh.percentage(self.oldAverage, self.average) >= self.chiSquaredSignificaneThreshold or self.totalDone < self.totalDoneThreshold:
            print("It's significant!")
            return(True)
        else:
            return(False)
    def chiSquared(self, text):
        """Creates letter frequency of text and compares that to the letter frequency of the language"""

        # This part creates a letter frequency of the text
        letterFreq = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
        for letter in text:
            if letter in letterFreq:
                letterFreq[letter] +=1
            else:
                # if letter is not puncuation, but it is still ascii
                # it's probably a different language so add it to the dict
                if letter not in punctuation and self.mh.isAscii(letter) :
                    letterFreq[letter] = 1
                
        # so we dont have to calculate len more than once
        # turns them into probabilities (frequency distribution)
        lenOfString = len(text)
        for key, value in letterFreq.items():
            try:
                letterFreq[key] = value / lenOfString
            except ZeroDivisionError as e:
                print("Error, you have entered an empty string :( The error is \"" + str(e) +"\" on line 34 of LanguageChecker.py (function chiSquared)")
                exit(1)

        # calculates chi squared of each language
        maxChiSquare = 0.00
        languagesChi = {}

        for language in self.languages:
            #, list(languages[language].values())
            temp = self.myChi(letterFreq, self.languages[language])
            languagesChi[language] = temp
            if temp > maxChiSquare:
                self.highestLanguage = language
        # calculates running average
        self.oldAverage = self.average
        self.totalDone += 1
        # calculates a running average, maxChiSquare is the new chi score we get
        self.average = (self.totalChi + maxChiSquare) / self.totalDone
        return(languagesChi)
    def myChi(self, text, distribution):
        """My own implementation of Chi squared using the two resources mention in the comments on this definition as guidance"""
        # chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://cgi.csc.liv.ac.uk/~john/comp105resources/lecture10.pdf
        # http://practicalcryptography.com/cryptanalysis/text-characterisation/chi-squared-statistic/
        # given a text frequency and a distribution, calculate it's Chi score
        chiScore = 0.0
        print(len(text))
        print(len(distribution))
        for counter, letter in enumerate(text.values()):
            chiScore = chiScore + ((letter - distribution[counter])**2) / distribution[counter]
        return chiScore
    def getMostLikelyLanguage(self):
        """Returns what the most likely language is
        Only used when the threshold of checkChi is reached"""
        return self.highestLanguage