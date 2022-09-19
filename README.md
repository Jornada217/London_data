# London_data
Greater London Data Studies and Machine Learning.
This is part of my Mst dissertation, submitted to the University of Cambridge in partial fulfilment of the requirements for the Degree of Master of Studies of Interdisciplinary Design in the Built Environment.

These notebooks use the merged Land Registry Prices Paid with EPC Certificates and Census datatets. For privacy reasons, I am not uploading the datasets, bu tha algorithms are disclosed.

In the folder GLA-data there is a sequence of 18 algorithms used to parse and merge the EPC, Prices Paid, GLA, Census and Economic data. Use the sequence in file names, not the order set by github to read through the files.

The folder GLA-Time_series contains the notebooks developed to create the chart pre-analysis GLA_Graphs.ipynb), and the time-series random forest model (GLA_prediction 2011-21.ipynb). There is also a printed version of the error map, with improved resolution, as the printed version of the dissertation has limited visibility for this chart.

The files on the main folder will serve as curiosity. The files refer to attempts in using different machine learning algorithms for the same problem (Neural Networks, Support Vector Regression, K-Neares Neighbor. Because I am using a desktop computer, these attempts failed for lack of computing power. There is also a Random Forest attempt with PCA, with significant reduction in accuracy.
