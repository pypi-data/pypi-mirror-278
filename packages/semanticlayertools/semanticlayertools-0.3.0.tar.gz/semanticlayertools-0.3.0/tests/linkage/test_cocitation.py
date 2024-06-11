import unittest
import os
import tempfile
import pandas as pd

from semanticlayertools.linkage.citation import Couplings

basePath = os.path.dirname(os.path.abspath(__file__ + "/../"))
filePath = f'{basePath}/testdata/cocite/'
filename = [x for x in os.listdir(filePath) if x.endswith('.json')]
testchunk = pd.read_json(filePath + filename[0], lines=True)


class TestCocitationCreation(unittest.TestCase):

    def setUp(self):
        self.outdir = tempfile.TemporaryDirectory()
        self.cociteinit = Couplings(
            filePath, self.outdir, 'reference',
            numberProc=2
        )

    def test_getCombinations(self):
        res = self.cociteinit._getCombinations(testchunk)
        assert (type(res[0]) == tuple)

