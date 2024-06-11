# LouvainSplit

LouvainSplit is a Python package for efficient graph partitioning using the LouvainSplit algorithm, based on the paper by Mehrdad Javadi, Hossein Aghighi and Mohsen Azadbakht.

## Abstract

Graph partitioning is essential for uncovering cohesive communities within complex networks. This paper introduces LouvainSplit, an innovative algorithm designed to enhance graph partitioning efficiency and accuracy. LouvainSplit leverages advanced techniques in feature representation, community detection, and evaluation, providing a robust framework for addressing challenges inherent in graph partitioning tasks across diverse domains. At its core, LouvainSplit utilizes a feature pyramid representation approach to extract both basic and summary features from input graphs at multiple granularity levels. This methodology ensures a subtle evaluation of graph data by capturing fundamental graph information alongside intricate structural patterns, thus offering a comprehensive representation of underlying community structures. A key innovation of our approach is the integration of the Louvain algorithm, renowned for its efficacy in community detection. By leveraging pairwise cosine similarities computed from node feature vectors, the Louvain algorithm optimizes modularity iteratively, effectively partitioning graphs into cohesive communities. This iterative process facilitates the identification of significant network structures within complex networks, providing valuable insights into their organizational dynamics. To comprehensively evaluate LouvainSplit's performance, we integrated diverse graph partitioning algorithms, including PyMetis, Genetic Algorithm (GA), DBSCAN, KMeans, OPTICS, and spectral clustering to evaluate the effectiveness of LouvainSplit and using popular evaluation metrics across diverse benchmarks spanning various domains and graphs. The results demonstrate LouvainSplit's superiority in terms of recall score, modularity, and scalability compared to existing methods. Moreover, LouvainSplit maintains competitive average runtime values, ensuring efficient processing even with large-scale datasets.

DOI: [10.21203/rs.3.rs-4301602/v1](https://doi.org/10.21203/rs.3.rs-4301602/v1)

## Installation

You can install the package via pip:

```sh
pip install louvainsplit


## Usage
Here is an example of how to use the LouvainSplit package:
import networkx as nx
from louvainsplit import construct_feature_pyramid, louvain_algorithm

# Create a sample graph
G = nx.karate_club_graph()

# Construct the feature pyramid
feature_pyramid = construct_feature_pyramid(G, num_levels=3)


# Apply the Louvain algorithm
partitions = louvain_algorithm(feature_pyramid, num_clusters=3)

print("Partitions:", partitions)

output >>> Partitions: [[0, 3, 6, 9, 12, 15, 18, 21, 24], [1, 4, 7, 10, 13, 16, 19, 22, 25], [2, 5, 8, 11, 14, 17, 20, 23]]

## Features
Feature Pyramid Representation: Extracts both basic and summary features from input graphs at multiple granularity levels.
Louvain Algorithm Integration: Utilizes the Louvain algorithm for efficient community detection based on cosine similarities of node feature vectors.

## Functions and Methods
construct_feature_pyramid(graph, num_levels)
Constructs a feature pyramid representation of the input graph.

Parameters:

graph: A NetworkX graph object.
num_levels: The number of levels in the feature pyramid.
Returns: A list of tensors representing the feature pyramid.
extract_basic_features(graph)
Extracts basic features from the input graph.

graph: A NetworkX graph object.
Returns: A list of basic features [num_nodes, num_edges, avg_degree clustering_coefficient].
extract_abstract_features(graph, level)
Extracts abstract features from the input graph at the specified level.

graph: A NetworkX graph object.
level: The granularity level for feature extraction.
Returns: A tensor of abstract features.
louvain_algorithm(feature_pyramid, num_clusters, similarity_measure='cosine')
Applies the Louvain algorithm to partition the graph based on the feature pyramid.

feature_pyramid: A list of tensors representing the feature pyramid.
num_clusters: The number of clusters to partition the graph into.
similarity_measure: The similarity measure to use (cosine is currently supported).
Returns: A list of partitions, where each partition is a list of node indices.



