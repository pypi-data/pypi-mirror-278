import re
import os
import time
import multiprocessing
from collections import Counter
from tqdm import tqdm

import spacy
import textacy
import textacy.tm
import pandas as pd
import warnings

from ..cleaning.text import htmlTags

num_processes = multiprocessing.cpu_count() - 2


class ClusterReports():
    """Generate reporting on time-clusters.

    Generate reports to describe the content for all found clusters above a
    minimal size by collecting metadata for all publications in each cluster,
    finding the top 20 authors and affiliations of authors involved in the
    cluster publications, and running basic NMF topic modelling with N=20 and
    N=50 topics (english language models are used!).
    For each cluster a report file is written to the output path.

    Input CSV filename is used to create the output folder in output path. For
    each cluster above the limit, a subfolder is created to contain all metadata
    for the cluster. The metadata files are assumed to be in JSONL format and
    contain the year in the filename.

    :param infile: Path to input CSV file containing information on nodeid, clusterid, and year
    :type infile: str
    :param metadatapath: Path to JSONL (JSON line) formated metadata files.
    :type metadatapath: str
    :param outpath: Path to create output folder in, foldername reflects input filename
    :type outpath: str

    :param textcolumn: The dataframe column of metadata containing textutal for topic modelling (default=title)
    :type textcolumn: str
    :param numberProc: Number of CPU the routine will use (default = all!)
    :type numberProc: int
    :param minClusterSize: The minimal cluster size, above which clusters are considered (default=1000)
    :type minClusterSize: int
    :param timerange: Time range to evalute clusters for (usefull for limiting computation time, default = (1945, 2005))
    :type timerange: tuple
    """

    def __init__(
        self, infile: str, metadatapath: str, outpath: str,
        textcolumn: str = 'title',
        authorColumnName: str = 'author',
        affiliationColumnName: str = 'aff',
        publicationIDcolumn: str = 'nodeID',
        numberProc: int = num_processes,
        languageModel: str = "en_core_web_lg",
        minClusterSize: int = 1000,
        timerange: tuple = (1945, 2005),
        rerun: bool = False,
        debug: bool = False
    ):
        """Constructor method"""
        self.numberProc = numberProc
        self.minClusterSize = minClusterSize
        self.metadatapath = metadatapath
        self.textcolumn = textcolumn

        self.langModel = languageModel
        self.nlp = spacy.load(self.langModel)

        self.authorColumnName = authorColumnName
        self.affiliationColumnName = affiliationColumnName
        self.publicationIDcolumn = publicationIDcolumn

        self.debug = debug

        clusterdf = pd.read_csv(infile)
        basedata = clusterdf.groupby(['year', 'cluster']).size().to_frame('counts').reset_index()
        self.largeClusterList = list(
            basedata.groupby('cluster').sum().query(f'counts > {self.minClusterSize}').index
        )
        self.clusternodes = clusterdf.query(
            'cluster in @self.largeClusterList'
        )
        outfolder = infile.split(os.path.sep)[-1][:-4] + "_minCluSize_" + str(self.minClusterSize)
        self.timerange = timerange
        self.outpath = os.path.join(outpath, outfolder)
        if os.path.isdir(self.outpath) and rerun is False:
            raise OSError(f'Output folder {self.outpath} exists. Aborting.')
        else:
            os.makedirs(self.outpath, exist_ok=True)
            for clu in self.largeClusterList:
                os.makedirs(os.path.join(self.outpath, f'Cluster_{clu}'), exist_ok=True)
        if self.debug is True:
            print(f"Found {len(self.largeClusterList)} cluster larger then {self.minClusterSize} nodes.")

    def create_corpus(self, dataframe, cluster):
        """Create corpus out of dataframe.

        Using the text contained in the cluster metadata to generate a corpus.
        After some basic preprocessing each text is used to generate a Spacy doc,
        of which only the lemmatized words without stop words are considered.

        :params dataframe: Input dataframe
        :type dataframe: `pd.Dataframe`
        :returns: A textacy corpus file with english as the base language
        :rtype: `textacy.Corpus`
        """
        starttime = time.time()
        docs = []
        dataframe = dataframe.drop_duplicates(subset=self.publicationIDcolumn).dropna(subset=self.textcolumn)
        if len(dataframe) > 10000:
            sample = dataframe.sample(int(len(dataframe) / 100))
        else:
            sample = dataframe.sample(int(len(dataframe) / 10))
        titles = [htmlTags(x) for x in sample[self.textcolumn].values]
        if self.debug is True:
            print(f"\tBuilding corpus for random sample of {len(titles)} documents.")
        generateDocuments = self.nlp.pipe(
            titles,
            n_process=self.numberProc
        )
        corpus_titles = textacy.Corpus(self.nlp)
        corpus_titles.add(generateDocuments, n_process=self.numberProc)
        if self.debug is True:
            print(f"\tBuild corpus in {(time.time() - starttime)/60:.2f} min.")
        corpus_titles.save(f"{self.outpath}/Cluster_{cluster}_corpus.bin.gz")
        return corpus_titles

    def find_topics(
        self, corpus_titles: list, n_topics: int, top_words: int,
    ):
        """Calculate topics in corpus.

        Use NMF algorithm to calculate topics in corpus file for `n_topics`
        topics, returning `top_words` most common words for each topic.
        Each word has to occure at least twice in the corpus and at most in 95%
        of all documents.

        :param corpus_titles: The corpus containing the preprocessed texts.
        :type corpus_titles: `textacy.Corpus`
        :param n_topics: Number of considered topics
        :type n_topics: int
        :param top_words: Number of returned words for each found topic
        :type top_words: int
        :returns: List of found topics with top occuring words
        :rtype: str
        """
        vectorizer = textacy.representations.vectorizers.Vectorizer(
            tf_type="linear",
            idf_type="smooth",
            norm="l2",
            min_df=2,
            max_df=0.95
        )
        tokenized_docs = (
            (
                term.lemma_ for term in textacy.extract.terms(doc, ngs=1, ents=True)
            ) for doc in corpus_titles
        )
        doc_term_matrix = vectorizer.fit_transform(tokenized_docs)

        model = textacy.tm.TopicModel("nmf", n_topics)
        model.fit(doc_term_matrix)

        topics = []
        for topic_idx, top_terms in model.top_topic_terms(
            vectorizer.id_to_term, top_n=top_words
        ):
            topics.append(
                "topic " + str(topic_idx) + ": " + "   ".join(top_terms)
            )
        outtext = f'\n\n\tTopics in cluster for {n_topics} topics:\n'
        for topic in topics:
            outtext += f'\t\t{topic}\n'
        return outtext

    def fullReport(self, cluster):
        """Generate full cluster report for one cluster.

        :param cluster: The cluster number to process
        :type cluster: int or str
        :raises ValueError: If input cluster data can not be read.
        :returns: Report text with all gathered informations
        :rtype: str
        """
        starttime = time.time()
        clusterpath = os.path.join(self.outpath, f'Cluster_{cluster}')
        clusterfiles = os.listdir(clusterpath)
        clusterdf = []
        for x in clusterfiles:
            try:
                clusterdf.append(
                    pd.read_json(os.path.join(clusterpath, x), lines=True)
                )
            except ValueError:
                raise
        dfCluster = pd.concat(clusterdf, ignore_index=True)
        if self.debug is True:
            print(f"Cluster {cluster} has {dfCluster.shape[0]} documents.")
        if dfCluster.shape[0] == 0:
            raise ValueError(f"No data for Cluster {cluster}.")
        basedf = self.clusternodes.query('cluster == @cluster')
        inputnodes = set(basedf.node.values)
        notFound = inputnodes.difference(set(dfCluster[self.publicationIDcolumn].values))
        topAuthors = Counter(
            [x for y in dfCluster[self.authorColumnName].fillna('').values for x in y]
        ).most_common(21)
        authortext = ''
        for x in topAuthors:
            if x[0] != '':
                authortext += f'\t{x[0]}: {x[1]}\n'
        topAffils = Counter(
            [x for y in dfCluster[self.affiliationColumnName].fillna('').values for x in y]
        ).most_common(21)
        affiltext = ''
        for x in topAffils:
            if x[0] != '' and x[0] != '-':
                affiltext += f'\t{x[0]}: {x[1]}\n'
        if self.debug is True:
            print(f'\tFinished base report for cluster {cluster}.')
        titlesOnly = dfCluster.drop_duplicates(subset=self.publicationIDcolumn).dropna(subset=self.textcolumn)
        if titlesOnly.shape[0] > 1000:
            corpus = self.create_corpus(dfCluster, cluster)
            
            warnings.simplefilter(action='ignore', category=FutureWarning)
            topics_15 = self.find_topics(corpus, n_topics=15, top_words=20)
            topics_50 = self.find_topics(corpus, n_topics=50, top_words=20)
        else:
            topics_15 = f"Number of documents to low ({len(titlesOnly)})." 
            topics_50 = f"Number of documents to low ({len(titlesOnly)})." 
            if self.debug is True:
                print(f"\tSkiping reports, only {len(titlesOnly)} docs with title.")
        outtext = f"""Report for Cluster {cluster}

Got {len(inputnodes)} unique publications in time range: {basedf.year.min()} to {basedf.year.max()}.
    Found metadata for {dfCluster.shape[0]} publications.
    There are {len(notFound)} publications without metadata.

    The top 20 authors of this cluster are:
    {authortext}

    The top 20 affiliations of this cluster are:
    {affiltext}

    {topics_15}

    {topics_50}

Finished analysis of cluster {cluster} in {time.time()- starttime} seconds."""
        print('\tFinished topics.')
        return outtext

    def writeReports(self):
        """Generate reports and write to output path."""
        for cluster in self.largeClusterList:
            outtext = self.fullReport(cluster)
            with open(f'{self.outpath}/Cluster_{cluster}.txt', 'w') as file:
                file.write(outtext)

    def _mergeData(self, filename):
        """Merge metadata for cluster nodes.

        Writes all metadata for nodes in cluster to folders.

        :param filename: Metadata input filename
        :type filename: str
        """
        if self.debug is True:
            print(f"Extracting cluster metadata for file {filename}.")
        filepath = os.path.join(self.metadatapath, filename)
        data = pd.read_json(filepath, lines=True)
        selectMerge = data.merge(
            self.clusternodes,
            left_on=self.publicationIDcolumn,
            right_on='node',
            how='inner'
        )
        selectMerge = selectMerge.drop_duplicates(subset=self.publicationIDcolumn)
        if selectMerge.shape[0] > 0:
            for clu, g0 in selectMerge.groupby('cluster'):
                g0.to_json(
                    os.path.join(
                        self.outpath,
                        f'Cluster_{clu}',
                        'merged_' + filename
                    ), orient='records', lines=True
                )
        return ''

    def gatherClusterMetadata(self):
        """Initial gathering of metadata for clusters.

        For all files in the metadata path, call `_mergeData` if the found
        year in the filename falls in the bounds.

        This step needs to be run once, then all cluster metadata is generated
        and can be reused.
        """
        filenames = sorted([x for x in os.listdir(self.metadatapath) if x.endswith("json")])
        yearFiles = []
        for x in filenames:
            try:
                year = int(re.findall(r'\d{4}', x)[0])
            except Exception:
                raise
            if self.timerange[0] <= year <= self.timerange[1]:
                yearFiles.append(x)
        with multiprocessing.Pool(self.numberProc) as pool:
            _ = pool.map(self._mergeData, tqdm(yearFiles, leave=False))
        return