import os
import re
import time
import multiprocessing
from tqdm import tqdm
import pandas as pd
import numpy as np
import igraph as ig
from itertools import repeat

num_processes = multiprocessing.cpu_count() - 2


class CalculateCentralities():
    """Calculate centralities for networks."""

    def __init__(
        self,
        clusterFile: str,
        graphdataPath: str,
        metadataPath: str,
        outPath: str,
        timerange: tuple = (1945, 2004),
        numberProc: int = num_processes,
        debug: bool = False
    ):
        self.outPath = os.path.join(
            outPath, clusterFile.split("/")[-1].split(".csv")[0] + "/"
        )
        self.graphdataPath = graphdataPath
        os.makedirs(self.outPath, exist_ok=True)
        self.numberProc = numberProc
        self.timerange = timerange
        self.clusterFile = clusterFile
        self.metadataPath = metadataPath
        self.debug = debug

    def setupClusterData(
        self,
        minClusterSize: int = 1000,
        idcolumn: str = 'nodeID'
    ):
        """Initial gathering of metadata for previously found time clusters.

        Set minClusterSize to limit clusters considered for analysis.

        For all files in the metadata path, this calls `_mergeData` if the found
        year in the filename falls in the bounds.

        This step needs to be run once, all cluster metadata is generated
        and can be reused"""
        self.idcolumn = idcolumn
        clusterdf = pd.read_csv(self.clusterFile)
        clusterdf = clusterdf.query("@self.timerange[0] <= year <= @self.timerange[1]")
        basedata = clusterdf.groupby(
            ['year', 'cluster']
        ).size().to_frame('counts').reset_index()
        self.largeClusterList = list(
            basedata.groupby('cluster').sum().query(
                f'counts > {minClusterSize}'
            ).index
        )
        self.clusternodes = clusterdf.query(
            'cluster in @self.largeClusterList'
        )
        
        # filenames = [x for x in os.listdir(self.metadataPath) if x.endswith('.json')]
        # yearFiles = []
        # for x in filenames:
        #     try:
        #         year = int(re.findall(r'\d{4}', x)[0])
        #     except Exception:
        #         raise
        #     if self.timerange[0] <= year <= self.timerange[1]:
        #         yearFiles.append(x)
        # mergList = []
        # for file in tqdm(yearFiles):
        #     year = int(re.findall(r'\d{4}', file)[0])
        #     df = pd.read_json(self.metadataPath + file, lines=True)
        #     df.insert(0, "year", year)
        #     cl = clusterdf.query("year == @year and cluster in @largeCL")
        #     merged = df.merge(cl, left_on="nodeID", right_on="node", how="inner")
        #     mergList.append(merged)
        # self.clusterMetadata = pd.concat(mergList)
        return self
    
    def _loadYearGraph(self, year: int, useGC: bool, citationTyp: str = "cocite"):
        """Helper for loading graph data to igraph."""
        starttime = time.time()
        if useGC is False:
            graph = ig.Graph.Read_Ncol(
                f'{self.graphdataPath}{citationTyp}_{year}.ncol',
                names=True,
                weights=True,
                directed=False
            )
        elif useGC is True:
            graph = ig.Graph.Read_Pajek(
                f'{self.graphdataPath}{citationTyp}_{year}_GC.net'
            )
        if self.debug is True:
            print(f"Loaded graph for {year} in {time.time() - starttime:.2f} sec.")
        return graph

    def _calculateAuthority(self, year, graph, calculateClusters=False):
        """Calculate authority centrality of graph.
        
        Create histogram of found centralities with logarithmic
        binning. Write results to outfile for values larger zero.
        To make results for different graph sizes comparable, 
        the resulting bin values are divided by the number of nodes
        in the graph.
        """
        starttime = time.time()
        bins = 10 ** np.linspace(np.log10(0.00001), np.log10(1.0), 100)
        centrality = graph.authority_score(scale=True)
        histoCentrality = np.histogram(centrality, bins=bins)
        with open(f'{self.outPath}authority_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'a') as outfile:
            for val, bin_ in zip(histoCentrality[0], histoCentrality[1]):
                if val > 0.0:
                    outfile.write(
                        f"{year},{bin_},{val/len(graph.vs)}\n"
                    )
        if self.debug is True:
            print(f"\t\tCalculated authority in {time.time() - starttime:.2f} sec.")
        if calculateClusters is True:
            starttime2 = time.time()
            for clu in self.largeClusterList:
                self._calculateClusterHistogram("authority", year, graph, clu, centrality, bins)
            if self.debug is True:
                print(f"\t\tCalculated cluster data in {time.time() - starttime2:.2f} sec.")
        return

    def _calculateBetweenness(self, year, graph, calculateClusters=False):
        """Calculate normalized betweenness centrality of undirected graph.
        
        Create histogram of found centralities with logarithmic
        binning. Write results to outfile for values larger zero.
        To make results for different graph sizes comparable, 
        the resulting bin values are divided by the number of nodes
        in the graph.
        """
        starttime = time.time()
        bins = 10 ** np.linspace(np.log10(0.00001), np.log10(1.0), 100)
        centrality = graph.betweenness(directed=False)
        maxBet = max(centrality)
        centrality = [x / maxBet for x in centrality]
        histoCentrality = np.histogram(centrality, bins=bins)
        with open(f'{self.outPath}betweenness_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'a') as outfile:
            for val, bin_ in zip(histoCentrality[0], histoCentrality[1]):
                if val > 0.0:
                    outfile.write(
                        f"{year},{bin_},{val/len(graph.vs)}\n"
                    )
        if self.debug is True:
            print(f"\t\tCalculated betweenness in {time.time() - starttime:.2f} sec.")
        if calculateClusters is True:
            starttime2 = time.time()
            for clu in self.largeClusterList:
                self._calculateClusterHistogram("betweenness", year, graph, clu, centrality, bins)
            if self.debug is True:
                print(f"\t\tCalculated cluster data in {time.time() - starttime2:.2f} sec.")
        return

    def _calculateDegree(self, year, graph, calculateClusters=False):
        """Calculate normalized degree centrality of graph.
        
        Create histogram of found centralities with logarithmic
        binning. Write results to outfile for values larger zero.
        To make results for different graph sizes comparable, 
        the resulting bin values are divided by the number of nodes
        in the graph.
        """
        starttime = time.time()
        bins = 10 ** np.linspace(np.log10(0.00001), np.log10(1.0), 100)
        centrality = graph.degree(graph.vs, mode='all')
        maxDeg = max(centrality)
        centrality = [x / maxDeg for x in centrality]
        histoCentrality = np.histogram(centrality, bins=bins)
        with open(f'{self.outPath}degree_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'a') as outfile:
            for val, bin_ in zip(histoCentrality[0], histoCentrality[1]):
                if val > 0.0:
                    outfile.write(
                        f"{year},{bin_},{val/len(graph.vs)}\n"
                    )
        if self.debug is True:
            print(f"\t\tCalculated degree in {time.time() - starttime:.2f} sec.")
        if calculateClusters is True:
            starttime2 = time.time()
            for clu in self.largeClusterList:
                self._calculateClusterHistogram("degree", year, graph, clu, centrality, bins)
            if self.debug is True:
                print(f"\t\tCalculated cluster data in {time.time() - starttime2:.2f} sec.")
        return  
    
    def _calculateCloseness(self, year, graph, calculateClusters=False):
        """Calculate normalized closeness centrality of graph.
        
        Create histogram of found centralities with logarithmic
        binning. Write results to outfile for values larger zero.
        To make results for different graph sizes comparable, 
        the resulting bin values are divided by the number of nodes
        in the graph.
        """
        starttime = time.time()
        bins = 10 ** np.linspace(np.log10(0.00001), np.log10(1.0), 100)
        centrality = graph.closeness(mode='all', normalized=True)
        histoCentrality = np.histogram(centrality, bins=bins)
        with open(f'{self.outPath}closeness_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'a') as outfile:
            for val, bin_ in zip(histoCentrality[0], histoCentrality[1]):
                if val > 0.0:
                    outfile.write(
                        f"{year},{bin_},{val/len(graph.vs)}\n"
                    )
        if self.debug is True:
            print(f"\tCalculated closeness in {time.time() - starttime:.2f} sec.")
        if calculateClusters is True:
            starttime2 = time.time()
            for clu in self.largeClusterList:
                self._calculateClusterHistogram("closeness", year, graph, clu, centrality, bins)
            if self.debug is True:
                print(f"\tCalculated cluster data in {time.time() - starttime2:.2f} sec.")
        return  

    def _calculateClusterHistogram(self, centName, year, graph, cluster, centralities, bins):
        """Calculate centralities historgram for cluster nodes."""
        nodes = self.clusternodes.query("year == @year and cluster == @cluster").node.unique()
        clusternodes = graph.vs.select(name_in=nodes)
        clusterCentralities = []
        for cln in clusternodes:
            idx = cln.index
            clncent = centralities[idx]
            clusterCentralities.append(clncent)
        histoCluster = np.histogram(clusterCentralities, bins=bins)
        with open(f'{self.outPath}{centName}_cluster_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'a') as outfile:
            for val, bin_ in zip(histoCluster[0], histoCluster[1]):
                if val > 0.0:
                    outfile.write(
                        f"{cluster},{year},{bin_},{val/len(graph.vs)}\n"
                    )
        return 

    def _createOuputfiles(self, cent, calculateClusters=False):
        with open(f'{self.outPath}{cent}_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'x') as generalOutfile:
            generalOutfile.write(
                "year,bin,value\n"
            )
        if calculateClusters is True:
            with open(f'{self.outPath}{cent}_cluster_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'x') as clusterOutfile:
                clusterOutfile.write(
                    "cluster,year,bin,value\n"
                )
        return

    def run(
        self, centrality: str = "all", useGC: bool = True, calculateClusters: bool = True
    ):
        """Run calculation based on Pajek (useGC=True) or NCol (useGC=False)
        network data.

        For centralities choose "all" or one of the following:
        "authority", "betweenness", "closeness", "degree".
        Centralities are normalized by the maximal value per year, 
        where applicable.

        Note that for closeness centrality, binning is chosen as normal, while
        for all other centralities, binning is logarithmic.
        """
        if centrality == "all": 
            for cent in ["authority", "betweenness", "degree", "closeness"]:
                self._createOuputfiles(cent, calculateClusters=calculateClusters)
        else:
            self._createOuputfiles(centrality, calculateClusters=calculateClusters)
        if centrality == "all": 
            for year in list(range(self.timerange[0], self.timerange[1] + 1)):
                graph = self._loadYearGraph(year, useGC)
                self._calculateAuthority(year=year, graph=graph, calculateClusters=calculateClusters)              
                self._calculateDegree(year=year, graph=graph, calculateClusters=calculateClusters)
                self._calculateCloseness(year=year, graph=graph, calculateClusters=calculateClusters)
                self._calculateBetweenness(year=year, graph=graph, calculateClusters=calculateClusters)
        elif centrality == "authority":
            for year in list(range(self.timerange[0], self.timerange[1] + 1)):
                graph = self._loadYearGraph(year, useGC)
                self._calculateAuthority(year=year, graph=graph, calculateClusters=calculateClusters)
        elif centrality == "betweenness":
            for year in list(range(self.timerange[0], self.timerange[1] + 1)):
                graph = self._loadYearGraph(year, useGC)
                self._calculateBetweenness(year=year, graph=graph, calculateClusters=calculateClusters) 
        elif centrality == "closeness":
            for year in list(range(self.timerange[0], self.timerange[1] + 1)):
                graph = self._loadYearGraph(year, useGC)
                self._calculateCloseness(year=year, graph=graph, calculateClusters=calculateClusters)
        elif centrality == "degree":
            for year in list(range(self.timerange[0], self.timerange[1] + 1)):
                graph = self._loadYearGraph(year, useGC)
                self._calculateDegree(year=year, graph=graph, calculateClusters=calculateClusters)
        return

    def _calculateAuthorityParallel(self, inputtuple):
        """Calculate authority centrality of graph for parallelized run.
        
        Create histogram of found centralities with logarithmic
        binning. Write results to outfile for values larger zero.
        To make results for different graph sizes comparable, 
        the resulting bin values are divided by the number of nodes
        in the graph.
        """
        starttime = time.time()
        year = inputtuple[0]
        useGC = inputtuple[1]
        calculateClusters = inputtuple[2]
        graph = self._loadYearGraph(year=year, useGC=useGC)
        bins = 10 ** np.linspace(np.log10(0.00001), np.log10(1.0), 100)
        centrality = graph.authority_score(scale=True)
        histoCentrality = np.histogram(centrality, bins=bins)
        with open(f'{self.outPath}authority_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'a') as outfile:
            for val, bin_ in zip(histoCentrality[0], histoCentrality[1]):
                if val > 0.0:
                    outfile.write(
                        f"{year},{bin_},{val/len(graph.vs)}\n"
                    )
        if self.debug is True:
            print(f"\tCalculated authority in {time.time() - starttime:.2f} sec.")
        if calculateClusters is True:
            starttime2 = time.time()
            for clu in self.largeClusterList:
                self._calculateClusterHistogram("authority", year, graph, clu, centrality, bins)
            if self.debug is True:
                print(f"\tCalculated cluster data in {time.time() - starttime2:.2f} sec.")
        return

    def _calculateBetweennessParallel(self, inputtuple):
        """Calculate normalized betweenness centrality of undirected graph for parallelized run.
        
        Create histogram of found centralities with logarithmic
        binning. Write results to outfile for values larger zero.
        To make results for different graph sizes comparable, 
        the resulting bin values are divided by the number of nodes
        in the graph.
        """
        starttime = time.time()
        year = inputtuple[0]
        useGC = inputtuple[1]
        calculateClusters = inputtuple[2]
        graph = self._loadYearGraph(year=year, useGC=useGC)
        bins = 10 ** np.linspace(np.log10(0.00001), np.log10(1.0), 100)
        centrality = graph.betweenness(directed=False)
        maxBet = max(centrality)
        centrality = [x / maxBet for x in centrality]
        histoCentrality = np.histogram(centrality, bins=bins)
        with open(f'{self.outPath}betweenness_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'a') as outfile:
            for val, bin_ in zip(histoCentrality[0], histoCentrality[1]):
                if val > 0.0:
                    outfile.write(
                        f"{year},{bin_},{val/len(graph.vs)}\n"
                    )
        if self.debug is True:
            print(f"\tCalculated betweenness in {time.time() - starttime:.2f} sec.")
        if calculateClusters is True:
            starttime2 = time.time()
            for clu in self.largeClusterList:
                self._calculateClusterHistogram("betweenness", year, graph, clu, centrality, bins)
            if self.debug is True:
                print(f"\tCalculated cluster data in {time.time() - starttime2:.2f} sec.")
        return

    def _calculateDegreeParallel(self, inputtuple):
        """Calculate normalized degree centrality of graph for parallelized run.
        
        Create histogram of found centralities with logarithmic
        binning. Write results to outfile for values larger zero.
        To make results for different graph sizes comparable, 
        the resulting bin values are divided by the number of nodes
        in the graph.
        """
        starttime = time.time()
        year = inputtuple[0]
        useGC = inputtuple[1]
        calculateClusters = inputtuple[2]
        graph = self._loadYearGraph(year=year, useGC=useGC)
        bins = 10 ** np.linspace(np.log10(0.00001), np.log10(1.0), 100)
        centrality = graph.degree(graph.vs, mode='all')
        maxDeg = max(centrality)
        centrality = [x / maxDeg for x in centrality]
        histoCentrality = np.histogram(centrality, bins=bins)
        with open(f'{self.outPath}degree_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'a') as outfile:
            for val, bin_ in zip(histoCentrality[0], histoCentrality[1]):
                if val > 0.0:
                    outfile.write(
                        f"{year},{bin_},{val/len(graph.vs)}\n"
                    )
        if self.debug is True:
            print(f"\tCalculated degree in {time.time() - starttime:.2f} sec.")
        if calculateClusters is True:
            starttime2 = time.time()
            for clu in self.largeClusterList:
                self._calculateClusterHistogram("degree", year, graph, clu, centrality, bins)
            if self.debug is True:
                print(f"\tCalculated cluster data in {time.time() - starttime2:.2f} sec.")
        return  
    
    def _calculateClosenessParallel(self, inputtuple):
        """Calculate normalized closeness centrality of graph for parallelized run.
        
        Create histogram of found centralities with logarithmic
        binning. Write results to outfile for values larger zero.
        To make results for different graph sizes comparable, 
        the resulting bin values are divided by the number of nodes
        in the graph.
        """
        starttime = time.time()
        year = inputtuple[0]
        useGC = inputtuple[1]
        calculateClusters = inputtuple[2]
        graph = self._loadYearGraph(year=year, useGC=useGC)
        bins = 10 ** np.linspace(np.log10(0.00001), np.log10(1.0), 100)
        centrality = graph.closeness(mode='all', normalized=True)
        histoCentrality = np.histogram(centrality, bins=bins)
        with open(f'{self.outPath}closeness_centralities_logbin_{self.timerange[0]}-{self.timerange[1]}.csv', 'a') as outfile:
            for val, bin_ in zip(histoCentrality[0], histoCentrality[1]):
                if val > 0.0:
                    outfile.write(
                        f"{year},{bin_},{val/len(graph.vs)}\n"
                    )
        if self.debug is True:
            print(f"\tCalculated closeness in {time.time() - starttime:.2f} sec.")
        if calculateClusters is True:
            starttime2 = time.time()
            for clu in self.largeClusterList:
                self._calculateClusterHistogram("closeness", year, graph, clu, centrality, bins)
            if self.debug is True:
                print(f"\tCalculated cluster data in {time.time() - starttime2:.2f} sec.")
        return 

    def runparallel(
        self, centrality: str, useGC: bool = True, calculateClusters: bool = True
    ):
        """Run parallel centrality calculation based on Pajek (useGC=True) or NCol (useGC=False)
        network data.

        For centralities choose "all" or one of the following:
        "authority", "betweenness", "closeness", "degree".
        Centralities are normalized by the maximal value per year, 
        where applicable.

        Note that for closeness centrality, binning is chosen as normal, while
        for all other centralities, binning is logarithmic.
        """
        with multiprocessing.Pool(self.numberProc) as pool:
            years = np.array(range(self.timerange[0], self.timerange[1] + 1))
            data = list(zip(years, repeat(useGC), repeat(calculateClusters)))
            self._createOuputfiles(centrality, calculateClusters=calculateClusters)
            if centrality == "authority":
                _ = pool.map(self._calculateAuthorityParallel, data)
            elif centrality == "betweenness":
                _ = pool.map(self._calculateBetweennessParallel, data) 
            elif centrality == "closeness":
                _ = pool.map(self._calculateClosenessParallel, data)
            elif centrality == "degree":
                _ = pool.map(self._calculateDegreeParallel, data)
        return
