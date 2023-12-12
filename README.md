# **LTM**: language time machine

#### _AIR - WS2023 - Group 11_

|                       |                    |                              |
| :-------------------: | :----------------: | :--------------------------: |
|     **Felix Holz**    | **David Wildauer** |     **Leopold Magurano**     |
| Data (pre-)processing |      ML model      | Visualization and evaluation |

_Language evolves over time. We assume that it is possible for a machine learning model to pick up on these small changes, given a large enough dataset._

In this project, we aim to employ various document representation techniques, such as analyzing the word frequencies or using doc2vec (an extension of word2vec), to create embeddings of the documents. These embeddings are used to train a machine learning model, which is able to predict the time period (year) in which a text snippet was published. 

![](https://lh7-us.googleusercontent.com/CdBs5-xt8GBJnFtSnhr7Ie469-LSH-NIils5X2PfqirbRef_Tz7esIMNHwBUXI9v6m37iwtYJlNJKaCjUEUH3WRfQO2bUl0ccupRXdqlXqZ8wVn3hgvmfuTXQWORNm_3B4eYNAeI36qV9bneTP1I8UU)

For our training, testing, and evaluation dataset we will be using text snippets from a subset of the publicly available _Project Gutenberg_ eBooks. The text snippets with the corresponding publishing dates are parsed from the eBooks extracted from the .zim file<sup>\[1]</sup> and written to a simple database to give everyone in our team easy access to it. We aim to implement and test different embeddings of our text snippets, which we then use for our machine learning model to predict the time period, or more accurately the year, in which this text snippet was published.
