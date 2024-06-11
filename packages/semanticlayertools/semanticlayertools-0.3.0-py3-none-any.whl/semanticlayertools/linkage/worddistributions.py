import time
import math
from operator import itemgetter
from collections import Counter
from itertools import islice, groupby
from tqdm import tqdm
import pandas as pd
from scipy.stats import ttest_ind


class CalculateKDL():
    """Calculates KDL scores for time slices.

    .. seealso::

        Stefania Degaetano-Ortlieb and Elke Teich. 2017. 
        Modeling intra-textual variation with entropy and surprisal: topical vs. stylistic patterns.
        In Proceedings of the Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature, pages 68–77,
        Vancouver, Canada. Association for Computational Linguistics.

    """

    def __init__(
        self,
        targetData,
        compareData,
        yearColumnTarget: str = 'year',
        yearColumnCompare: str = 'year',
        tokenColumnTarget: str = 'tokens',
        tokenColumnCompare: str = 'tokens',
        debug: bool = False
    ):

        self.baseDF = compareData
        self.targetDF = targetData
        self.yearColTarget = yearColumnTarget
        self.yearColCompare = yearColumnCompare
        self.tokenColumnTarget = tokenColumnTarget
        self.tokenColumnCompare = tokenColumnCompare
        self.ngramData = []
        self.minNgramNr = 1
        self.debug = debug

    def _window(self, seq, n):
        """Return a sliding window (of width n) over data from the iterable.

        s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
        """
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def _createSlices(self, windowSize):
        """Create slices of dataframe."""
        slices = []
        years = sorted(self.targetDF[self.yearColTarget].unique())
        for x in self._window(years, windowSize):
            slices.append(x)
        return slices

    def _calculateDistributions(self, source, dataframe, timesliceNr, timeslice, specialChar):
        unigram = []
        fourgram = []
        if source == "target":
            yearCol = self.yearColTarget
            tokenCol = self.tokenColumnTarget
        elif source == "compare":
            yearCol = self.yearColCompare
            tokenCol = self.tokenColumnCompare
        df = dataframe[dataframe[yearCol].isin(timeslice)]
        for _, row in df.iterrows():
            for elem in row[tokenCol]:
                elemLen = len(elem.split(specialChar))
                if elemLen == 1:
                    unigram.append(elem)
                elif elemLen == 4:
                    fourgram.append(elem.split(specialChar))
        unigramCounts = dict(Counter(unigram).most_common())
        fourgram.sort(key=lambda x: x[3])
        sorted4grams = [
            [specialChar.join(x) for x in list(group)] for key, group in groupby(fourgram, itemgetter(3))
        ]
        return (timesliceNr, source, timeslice[-1], unigramCounts, sorted4grams)
   
    def getNgramPatterns(self, windowSize=3, specialChar="#"):
        """Create dictionaries of occuring ngrams.
       
        :param specialChar: Special character used to delimit tokens in ngrams (default=#)
        :type specialChar: str
        """
        starttime = time.time()
        self.ngramData = []
        print(f"Got data for {self.baseDF[self.yearColCompare].min()} to {self.baseDF[self.yearColCompare].max()}, starting calculations.")
        for idx, timeslice in tqdm(enumerate(self._createSlices(windowSize)), leave=False):
            sliceName = timeslice[-1]
            if self.debug is True:
                print(f"\tStart slice {sliceName}.")
            self.ngramData.append(
                self._calculateDistributions('target', self.targetDF, idx, timeslice, specialChar)
            )
            self.ngramData.append(
                self._calculateDistributions('compare', self.baseDF, idx, timeslice, specialChar)
            )
        if self.debug is True:
            print(f"Done in  {time.time() - starttime} seconds.")
        return
       
    def getKDLRelations(self, windowSize: int = 3, minNgramNr: int = 5, specialChar: str = "#"):
        """Calculate KDL relations.

        :param specialChar: Special character used to delimit tokens in ngrams (default=#)
        :type specialChar: str
        """
        self.kdlRelations = []
        distributions = pd.DataFrame(
            self.ngramData,
            columns=['sliceNr', 'dataType', 'sliceName', 'unigrams', 'fourgrams']
        )
        for idx in distributions['sliceNr'].unique():
            targetData = distributions.query('dataType == "target" and sliceNr == @idx')
            sorted4gram = targetData['fourgrams'].iloc[0]
            sorted4gramDict = {elem[0].split(specialChar)[3]: elem for elem in sorted4gram}
            unigramCounts = targetData['unigrams'].iloc[0]
            year1 = targetData['sliceName'].iloc[0]
            compareDataPost = distributions.query(
                f'dataType == "compare" and (sliceNr >= {idx + windowSize} or sliceNr <={idx - windowSize})'
            )
            for _, row in compareDataPost.iterrows():
                kdlVals = []
                idx2 = row['sliceNr']
                year2 = row['sliceName']
                sorted4gram2 = row['fourgrams']
                sorted4gramDict2 = {elem[0].split(specialChar)[3]: elem for elem in sorted4gram2}
                # unigramCounts2 = row['unigrams']
                for key, elem1 in sorted4gramDict.items():  
                    if unigramCounts[key] < minNgramNr:
                        continue
                    if key not in sorted4gramDict2.keys():
                        continue
                       
                    elem2 = sorted4gramDict2[key]
                    basisLen1 = len(set(elem1))
                    basisLen2 = len(set(elem2))
                       
                    counts1 = dict(Counter(elem1).most_common())
                    counts2 = dict(Counter(elem2).most_common())
                       
                    probList = []
                    for key, val in counts1.items():
                        if key in counts2.keys():
                            probList.append(
                                val / basisLen1 * math.log((val * basisLen2) / (basisLen1 * counts2[key]), 2)
                            )
                    kdl = sum(probList)
                    kdlVals.append(kdl)
               
                self.kdlRelations.append(
                    (idx, idx2, year1, year2, sum(kdlVals))
                )
        return self.kdlRelations


class UnigramKDL():

    def __init__(
        self,
        data,
        targetName: str,
        lambdaParam: float = 0.95,
        yearCol: str = 'Year',
        authorCol: str = "Author",
        tokenCol: str = "tokens",
        docIDCol: str = "bibcode",
        windowSize: int = 3
    ):
        self.fullcorpus = data
        self.targetcorpus = data.query(
            f"{authorCol}.fillna('').str.contains('{targetName}')"
        )

        self.lambdaParam = lambdaParam
        self.yearCol = yearCol
        self.tokenCol = tokenCol
        self.docIDCol = docIDCol
        self.winSize = windowSize

        self.fullModel = {}
        self.fullDocModel = {}
        self.targetModel = {}
        self.targetDocModel = {}

    def _createUnigramModel(self, sl, data):
        unigrams = []
        unigramsPerDoc = []
        for idx, row in data.iterrows():
            text = row[self.tokenCol]
            docid = row[self.docIDCol]
            unigramtext = [x for x in text if '#' not in x]
            docLen = len(unigramtext)
            docCounts = Counter(unigramtext)
            for key, val in docCounts.items():
                unigramsPerDoc.append(
                    (sl, docid, key, val / docLen)
                )
            unigrams.extend(unigramtext)
        termlength = len(unigrams)
        counts = Counter(unigrams)
        unigramModel = {x: y / termlength for x, y in counts.items()}
        return unigramModel, unigramsPerDoc

    def _window(self, seq, n):
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def _createSlices(self, windowSize):
        """Create slices of dataframe."""
        slices = []
        years = sorted(self.fullcorpus[self.yearCol].unique())
        for x in self._window(years, windowSize):
            slices.append(x)
        return slices

    def _createCorpora(self, languageModelType='unigram'):
        yearslices = self._createSlices(self.winSize)
        if languageModelType == "unigram":
            for sl in yearslices:
                slStart = sl[0]
                slEnd = sl[-1]
                slicefull = self.fullcorpus.query(f"{slStart} < {self.yearCol} < {slEnd}")
                slicetarget = self.targetcorpus.query(f"{slStart} < {self.yearCol} < {slEnd}")
                self.fullModel[slEnd], self.fullDocModel[slEnd] = self._createUnigramModel(slEnd, slicefull)
                self.targetModel[slEnd], self.targetDocModel[slEnd] = self._createUnigramModel(slEnd, slicetarget)
            self.fullModel["complete"], self.fullDocModel["complete"] = self._createUnigramModel("complete", self.fullcorpus)
        elif languageModelType == "trigram":
            raise NotImplementedError(
                "This language model is not implemented yet."
            )
        return

    def calculateJMS(self, term, targetUM, fullUM):
        """Jelinek-Mercer smoothening"""
        probF = fullUM.get(term, 0)
        probT = targetUM.get(term, 0)
        return self.lambdaParam * probT + (1 - self.lambdaParam) * probF

    def calculateKDL(self, languageModelType="unigram", timeOrder="synchron"):
        """Synchronous or asynchronous comparision."""
        yearslices = self._createSlices(self.winSize)
        self._createCorpora(languageModelType=languageModelType)
        resPoint = []
        resSummed = []
        for sl in tqdm(yearslices, leave=None):
            targetYear = sl[-1]
            yearTerms = set(self.targetModel[targetYear].keys())
            if timeOrder == "synchron":
                years = [targetYear]
            elif timeOrder == "asynchron":
                years = [key for key in self.fullModel.keys() if key != "complete"]
            else:
                raise ValueError("Time order not in synchron / asynchron. ")
            for compareYear in years:
                sliceResults = []
                for term in list(yearTerms):
                    jelinekTarget = self.calculateJMS(
                        term, self.targetModel[targetYear], self.fullModel["complete"]
                    )
                    jelinekFull = self.calculateJMS(
                        term, self.fullModel[compareYear], self.fullModel["complete"]
                    )
                    termProb = jelinekTarget * math.log(
                        (jelinekTarget) / (jelinekFull), 2
                    )
                    resPoint.append(
                        (targetYear, compareYear - targetYear, term, termProb)
                    )
                    sliceResults.append(termProb)
                resSummed.append(
                    (targetYear, compareYear - targetYear, sum(sliceResults))
                )
        return resPoint, resSummed
    
    def welch_tTest(self, languageModelType="unigram", timeOrder="synchron"):
        """Calculate significants"""
        resultPointwise, _ = self.calculateKDL(
            languageModelType=languageModelType,
            timeOrder=timeOrder
        )
        resultdf = pd.DataFrame(
            resultPointwise,
            columns=['targetYear', 'timedifference', 'term', 'kdl']
        )
        tempvalues = []
        errors = []
        for targetYear in tqdm(self.targetDocModel.keys(), leave=None):
            dataT = pd.DataFrame(
                self.targetDocModel[targetYear],
                columns=['sl', "docid", 'term', 'prob']
            )
            if timeOrder == "asynchron":
                years = [key for key in self.fullDocModel.keys() if key != "complete"]
            elif timeOrder == "synchron":
                years = [targetYear]
            for compareYear in years:
                dataF = pd.DataFrame(
                    self.fullDocModel[compareYear],
                    columns=['sl', "docid", 'term', 'prob']
                )
                for term in dataT.term.unique():
                    dataseriesT = dataT.query(f'term == "{term}"').prob.values
                    dataseriesF = dataF.query(f'term == "{term}"').prob.values
                    if any(
                        (len(dataseriesT) < 2, len(dataseriesF) < 2)
                    ):
                        errors.append(
                            (
                                targetYear,
                                compareYear - targetYear,
                                term,
                                len(dataseriesT),
                                len(dataseriesF)
                            )
                        )
                    else:
                        test = ttest_ind(
                            dataseriesT, dataseriesF, equal_var=False
                        )
                        tempvalues.append(
                            (
                                targetYear,
                                compareYear - targetYear,
                                term,
                                test.pvalue,
                                test.statistic
                            )
                        )
        tempdf = pd.DataFrame(
            tempvalues,
            columns=['targetYear', 'timedifference', 'term', 'pvalue', 'prob']
        )
        result = resultdf.merge(
            tempdf,
            left_on=['targetYear', 'timedifference', 'term'],
            right_on=['targetYear', 'timedifference', 'term'],
            how='outer'
        )
        return result, errors
