import unittest
import os
import pytest
import tempfile
import pandas as pd

from semanticlayertools.clustering.reports import ClusterReports
from semanticlayertools.linkage.citation import Couplings
from semanticlayertools.clustering.leiden import TimeCluster

basePath = os.path.dirname(os.path.abspath(__file__ + "/../"))
filePath = f'{basePath}/testdata/cocite/'
filename = [x for x in os.listdir(filePath) if x.endswith('.json')]
testchunk = pd.read_json(filePath + filename[0], lines=True)


class TestReportsCreation(unittest.TestCase):

    def setUp(self):
        self.outpath = tempfile.TemporaryDirectory()

        self.citeinit = Couplings(
            inpath=filePath,
            outpath=self.outpath.name,
            referenceColumn="reference",
            numberProc=2,
            timerange=(1950, 1959)
        )
        res0 = self.citeinit.getCocitationCoupling()

        self.cluinit = TimeCluster(
            inpath=self.outpath.name,
            outpath=self.outpath.name,
            timerange=(1950, 1959)
        )
        self.res1 = self.cluinit.optimize(clusterSizeCompare=10)

        self.reportsinit = ClusterReports(
            infile=self.res1.outfile,
            metadatapath=filePath,
            outpath=self.outpath.name,
            textcolumn="title",
            languageModel="en_core_web_sm",
            numberProc=2,
            minClusterSize=1,
            timerange=(1950, 1959)
        )

    def test_getCombinations(self):
        res = self.reportsinit.gatherClusterMetadata()
        # TODO:  assert (type(res[0]) == tuple)

