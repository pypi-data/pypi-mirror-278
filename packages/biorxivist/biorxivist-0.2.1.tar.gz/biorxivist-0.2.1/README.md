# BioRxivist

BioRxivist is a platform to explore the possibilities in combinding Large Laguage Models (LLM) with full text pre-publication scientific articles from [BioRxiv](https://biorxiv.org).  Use this tool to obtain datasets from BioRxiv publications build knowledge graphs using [Neo4J](https://neo4j.com/).  And facilitate the use of docker run databases and other tools.



<a id="tocz"></a>
## Table of Contents
1. ### [Using BioRxivist to find and load text from papers](#loading-text)
2. ### [BioRxivistPaper Objects](#paper-object)
3. ### [Building Vector embeddings](#embeddings)
4. ### [Connecting to and existing vector database](#vectordatabase)


```python
import os
import sys
sys.version
```




    '3.10.13 (main, Nov 17 2023, 08:59:57) [GCC 9.4.0]'




```python
from dotenv import find_dotenv, load_dotenv
from os import environ
import openai
from warnings import warn
# import classes from BioRxivist
from biorxivist.webtools import BioRxivPaper
from biorxivist.webtools import BioRxivDriver
from biorxivist.webtools import SearchResult
from langchain.vectorstores import Neo4jVector
```


```python
# load_environment variables like our API key and Neo4J credentials
load_dotenv(find_dotenv())
```




    True



Setting Up Your Environment

Your environment should include the following:

```
OPENAI_API_KEY=<YOUR_SECRET_KEY>
NEO4J_URL=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=MyPa$$word!
```
Get an [openai key](https://openai.com/)

If you are installing this package in a development enviornment you might choose to set them in a `.env` environment variable here.

<a id='loading-text'></a>
# Using BioRxivist to find and load text from papers

The first thing we'll want to do is find a paper of interest.  Well use the object from this package. `BioRxivDriver` will give us access to BioRxiv's search utility. `SearchResuls` will help us manage the results of our search. `BioRxivPaper` will manage how we access text from the papers.


[Table Of Contents](#tocz)


```python
driver = BioRxivDriver()
```


```python
r = driver.search_biorxiv('TGF-Beta 1 Signaling in monocyte maturation')
```


```python
r.response.request.url
```




    'https://www.biorxiv.org/search/TGF-Beta+1+Signaling+in+monocyte+maturation%20numresults:75'




```python
type(r)
```




    biorxivist.webtools.SearchResult




```python
len(r.results)
```




    75




```python
# load more results
r.more()
```


```python
len(r.results)
```




    150




```python
# Results are a list of BioRxivPaper objects
r.results[0:5]
```




    [[Shear Stress Induces a Time-Dependent Inflammatory Response in Human Monocyte-Derived Macrophages](https://biorxiv.org/content/10.1101/2022.12.08.519590v3),
     [Cross-species analysis identifies conserved transcriptional mechanisms of neutrophil maturation](https://biorxiv.org/content/10.1101/2022.11.28.518146v1),
     [Melanogenic Activity Facilitates Dendritic Cell Maturation via FMOD](https://biorxiv.org/content/10.1101/2022.05.14.491976v2),
     [Microglia integration into human midbrain organoids leads to increased neuronal maturation and functionality](https://biorxiv.org/content/10.1101/2022.01.21.477192v1),
     [Long-term culture of fetal monocyte precursors in vitro allowing the generation of bona fide alveolar macrophages in vivo](https://biorxiv.org/content/10.1101/2021.06.04.447115v2)]



<a id='paper-object'></a>
# BioRxivPaper Objects:
BioRxiv Paper objects link us to BioRxiv resources related to individual papers. Once instantiated these papers load a minimal amount of information into memory the URI of the papers homepage and the title.  Other features like the paper's abstract and full text are lazy-loaded properties. They are only accessed once we call them for the first time. After that they are available from memory so we don't have to hit the URL another time.

They are also feed directly into our LangChain pipeline.  In the next section we will make sure of their BioRxivPaper.langchain_html_doc attribute.

[Table of Contents](#tocz)

# Interact with individual papers:
The results are a collection of BioRxivPaper objects.  We can interact with them by indexing into the list or we can pull them out and interact with them here:


```python
paper3 = r.results[3]
```


```python
paper3.title
```




    'Microglia integration into human midbrain organoids leads to increased neuronal maturation and functionality'




```python
paper3.abstract
```




    'The human brain is a complex, three-dimensional structure. To better recapitulate brain complexity, recent efforts have focused on the development of human specific midbrain organoids. Human iPSC-derived midbrain organoids consist of differentiated and functional neurons, which contain active synapses, as well as astrocytes and oligodendrocytes. However, the absence of microglia, with their ability to remodel neuronal networks and phagocytose apoptotic cells and debris, represents a major disadvantage for the current midbrain organoid systems. Additionally, neuro-inflammation related disease modeling is not possible in the absence of microglia. So far, no studies about the effects of human iPSC-derived microglia on midbrain organoid neural cells have been published. Here we describe an approach to derive microglia from human iPSCs and integrate them into iPSC-derived midbrain organoids. Using single nuclear RNA Sequencing, we provide a detailed characterization of microglia in midbrain organoids as well as the influence of their presence on the other cells of the organoids. Furthermore, we describe the effects that microglia have on cell death and oxidative stress- related gene expression. Finally, we show that microglia in midbrain organoids affect synaptic remodeling and increase neuronal excitability. Altogether, we show a more suitable system to further investigate brain development, as well as neurodegenerative diseases and neuro- inflammation.\n\nMain Points\n\n– Macrophage precursors can be efficiently co-cultured with midbrain organoids, they integrate into the tissue and differentiate into microglia in 3D.\n\n– Organoids containing microglia have a smaller size and show a down-regulation of oxidative stress-related genes.\n\n– Organoids co-cultured with microglia show differences in genes related to synaptic remodeling and action potential, as well as a more spontaneous action potential firing.'



# Accessing the paper's text

There are now a few ways to access the papers text:


```python
# through the paper.text property:
# print(paper3.text)
# by accessing the BioRxivPaper.__str__ attribute:
print(f'...{paper3[392:1000]}...')
```

    ...r ability to remodel neuronal networks and phagocytose apoptotic cells and debris, represents a major disadvantage for the current midbrain organoid systems. Additionally, neuro-inflammation related disease modeling is not possible in the absence of microglia. So far, no studies about the effects of human iPSC-derived microglia on midbrain organoid neural cells have been published. Here we describe an approach to derive microglia from human iPSCs and integrate them into iPSC-derived midbrain organoids. Using single nuclear RNA Sequencing, we provide a detailed characterization of microglia in midbrain...


<a id='embeddings'></a>
# Build vector Embeddings

You can use OpenAI to build vecotor embeddings from the paper(s) you extract from BioRxiv.  This will form the bases of all tools to follow. =


[Table of Contents](#tocz)


```python
openai.api_key = environ['OPENAI_API_KEY']
```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
```


```python
len(paper3.langchain_doc)
```

    Created a chunk of size 1473, which is longer than the specified 1000
    Created a chunk of size 1440, which is longer than the specified 1000
    Created a chunk of size 1038, which is longer than the specified 1000
    Created a chunk of size 1232, which is longer than the specified 1000
    Created a chunk of size 1149, which is longer than the specified 1000
    Created a chunk of size 1177, which is longer than the specified 1000
    Created a chunk of size 1144, which is longer than the specified 1000
    Created a chunk of size 1029, which is longer than the specified 1000
    Created a chunk of size 1039, which is longer than the specified 1000
    Created a chunk of size 1408, which is longer than the specified 1000
    Created a chunk of size 1071, which is longer than the specified 1000
    Created a chunk of size 1400, which is longer than the specified 1000
    Created a chunk of size 1863, which is longer than the specified 1000
    Created a chunk of size 1268, which is longer than the specified 1000
    Created a chunk of size 1113, which is longer than the specified 1000
    Created a chunk of size 3284, which is longer than the specified 1000
    Created a chunk of size 1067, which is longer than the specified 1000
    Created a chunk of size 1805, which is longer than the specified 1000
    Created a chunk of size 1341, which is longer than the specified 1000
    Created a chunk of size 2355, which is longer than the specified 1000
    Created a chunk of size 1540, which is longer than the specified 1000
    Created a chunk of size 1061, which is longer than the specified 1000
    Created a chunk of size 1025, which is longer than the specified 1000
    Created a chunk of size 1201, which is longer than the specified 1000
    Created a chunk of size 1355, which is longer than the specified 1000
    Created a chunk of size 1183, which is longer than the specified 1000
    Created a chunk of size 1463, which is longer than the specified 1000
    Created a chunk of size 1648, which is longer than the specified 1000
    Created a chunk of size 2672, which is longer than the specified 1000
    Created a chunk of size 1016, which is longer than the specified 1000
    Created a chunk of size 2228, which is longer than the specified 1000
    Created a chunk of size 1566, which is longer than the specified 1000
    Created a chunk of size 2109, which is longer than the specified 1000





    78




```python
# TODO lets make an object in BioRxivist that does this
vec = Neo4jVector.from_documents(
    paper3.langchain_doc,
    OpenAIEmbeddings()
)
# If you have your NEO4J environment variables set no need to set them here.
```


```python
type(vec)
```




    langchain.vectorstores.neo4j_vector.Neo4jVector




```python
docs_with_score = vec.similarity_search_with_score('Providing the reasonging complete the following the function of CSF2 is <BLANK>?', k=5)
```


```python
docs_with_score[0]
```




    (Document(page_content='In addition to the homeostatic function, AM play an essential role in protecting influenza virus-infected mice from morbidity by maintaining lung integrity through the removal of dead cells and excess surfactant (Schneider et al, 2014). To assess the functional capacity of CSF2-cFLiMo-derived AM during pulmonary virus infection, we reconstituted Csf2ra-/- neonates with CSF2-cFLiMo and infected adults 10 weeks later with influenza virus PR8 (Fig. 5A). Without transfer, Csf2ra-/- mice succumbed to infection due to lung failure (Fig. 5B-E), as reported previously (Schneider et al, 2017). Notably, the presence of CSF2-cFLiMo-derived-AM protected Csf2ra-/- mice from severe morbidity (Fig. 5B, C) and completely restored viability (Fig. 5D) and O2 saturation (Fig. 5E) compared to infected WT mice.', metadata={'title': 'Long-term culture of fetal monocyte precursors in vitro allowing the generation of bona fide alveolar macrophages in vivo', 'source': 'https://biorxiv.org/content/10.1101/2021.06.04.447115v2.full-text'}),
     0.9044170379638672)




```python
for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

    --------------------------------------------------------------------------------
    Score:  0.9044170379638672
    In addition to the homeostatic function, AM play an essential role in protecting influenza virus-infected mice from morbidity by maintaining lung integrity through the removal of dead cells and excess surfactant (Schneider et al, 2014). To assess the functional capacity of CSF2-cFLiMo-derived AM during pulmonary virus infection, we reconstituted Csf2ra-/- neonates with CSF2-cFLiMo and infected adults 10 weeks later with influenza virus PR8 (Fig. 5A). Without transfer, Csf2ra-/- mice succumbed to infection due to lung failure (Fig. 5B-E), as reported previously (Schneider et al, 2017). Notably, the presence of CSF2-cFLiMo-derived-AM protected Csf2ra-/- mice from severe morbidity (Fig. 5B, C) and completely restored viability (Fig. 5D) and O2 saturation (Fig. 5E) compared to infected WT mice.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.9043794870376587
    In addition to the homeostatic function, AM play an essential role in protecting influenza virus-infected mice from morbidity by maintaining lung integrity through the removal of dead cells and excess surfactant (Schneider et al, 2014). To assess the functional capacity of CSF2-cFLiMo-derived AM during pulmonary virus infection, we reconstituted Csf2ra-/- neonates with CSF2-cFLiMo and infected adults 10 weeks later with influenza virus PR8 (Fig. 5A). Without transfer, Csf2ra-/- mice succumbed to infection due to lung failure (Fig. 5B-E), as reported previously (Schneider et al, 2017). Notably, the presence of CSF2-cFLiMo-derived-AM protected Csf2ra-/- mice from severe morbidity (Fig. 5B, C) and completely restored viability (Fig. 5D) and O2 saturation (Fig. 5E) compared to infected WT mice.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.9014166593551636
    CSF2-cFLiMo generated from wild-type or gene-deficient mice could be used as a high-throughput screening system to study AM development in vitro and in vivo. Our model is suitable to study the relationship between AM and lung tissue, as well as the roles of specific genes or factors in AM development and function. Furthermore, CSF2-cFLiMo can overcome the limitation in macrophage precursor numbers and be used as a therapeutic approach for PAP disease or in other macrophage-based cell therapies including lung emphysema, lung fibrosis, lung infectious disease and lung cancer (Byrne et al, 2016; Lee et al, 2016; Wilson et al, 2010). Finally, genetically modified and transferred CSF2-cFLiMo might facilitate the controlled expression of specific therapeutic proteins in the lung for disease treatment, and therefore, could represent an attractive alternative to non-specific gene delivery by viral vectors.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.901383638381958
    CSF2-cFLiMo generated from wild-type or gene-deficient mice could be used as a high-throughput screening system to study AM development in vitro and in vivo. Our model is suitable to study the relationship between AM and lung tissue, as well as the roles of specific genes or factors in AM development and function. Furthermore, CSF2-cFLiMo can overcome the limitation in macrophage precursor numbers and be used as a therapeutic approach for PAP disease or in other macrophage-based cell therapies including lung emphysema, lung fibrosis, lung infectious disease and lung cancer (Byrne et al, 2016; Lee et al, 2016; Wilson et al, 2010). Finally, genetically modified and transferred CSF2-cFLiMo might facilitate the controlled expression of specific therapeutic proteins in the lung for disease treatment, and therefore, could represent an attractive alternative to non-specific gene delivery by viral vectors.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.901383638381958
    Overall, our studies demonstrate that CSF2-cFLiMo-AM were functionally equivalent to naturally differentiated AM. To determine the number of donor cells required to fully reconstitute the AM compartment of Csf2ra-/- mice, we titrated the number of transferred CSF2-cFLiMo (Fig. 4A). Transfer of a minimum of 5×104 CSF2-cFLiMo to neonatal Csf2ra-/- mice resulted in AM numbers in adult recipients that were comparable to unmanipulated WT mice (around 5×105) (Fig. 4B) and protected mice from PAP (Fig. 4C). We have previously established that around 10% of primary fetal liver monocytes supplied intranasally reach the lung (Li et al, 2020). Thus, CSF2-cFLiMo have expanded around 100-fold 6 weeks after transfer to Csf2ra-/- neonates. Notably, extended time of CSF2-cFLiMo in vitro culture (i.e. 4 months) prior transfer into recipient mice did not negatively affect their differentiation and functional capacity (Fig. 4B, C). Another critical function of tissue-resident macrophages including AM is the removal of apoptotic cells (efferocytosis) (Morioka et al, 2019). We compared efferocytosis between CSF2-cFLiMo-AM in Csf2ra-/- mice and AM in WT mice by intratracheal (i.t.) installation of labelled apoptotic thymocytes. CSF2-cFLiMo-AM and AM were equally potent at phagocytosing apoptotic cells from the bronchoalveolar space (Fig. 4D).
    --------------------------------------------------------------------------------


<a id='vectordatabase'></a>
# Connect to an existing vector store

Once you have a vector store in your enviroment BioRxivist can simplify how you access and interact with that data using its `Neo4JDatabase` object.


[Table of Contents](#tocz)

## From Existing Index:


```python
index_name = "vector"  # default index name

store = Neo4jVector.from_existing_index(
    OpenAIEmbeddings(),
    index_name=index_name,
)
# consuming the NEOJ environment variables
```


```python
type(store)
```




    langchain.vectorstores.neo4j_vector.Neo4jVector




```python
result = store.similarity_search_with_score('CSF2', k=5)
```


```python
result
```




    [(Document(page_content='CSF2-cFLiMo generated from wild-type or gene-deficient mice could be used as a high-throughput screening system to study AM development in vitro and in vivo. Our model is suitable to study the relationship between AM and lung tissue, as well as the roles of specific genes or factors in AM development and function. Furthermore, CSF2-cFLiMo can overcome the limitation in macrophage precursor numbers and be used as a therapeutic approach for PAP disease or in other macrophage-based cell therapies including lung emphysema, lung fibrosis, lung infectious disease and lung cancer (Byrne et al, 2016; Lee et al, 2016; Wilson et al, 2010). Finally, genetically modified and transferred CSF2-cFLiMo might facilitate the controlled expression of specific therapeutic proteins in the lung for disease treatment, and therefore, could represent an attractive alternative to non-specific gene delivery by viral vectors.', metadata={'title': 'Long-term culture of fetal monocyte precursors in vitro allowing the generation of bona fide alveolar macrophages in vivo', 'source': 'https://biorxiv.org/content/10.1101/2021.06.04.447115v2.full-text'}),
      0.9244592189788818),
     (Document(page_content='CSF2-cFLiMo generated from wild-type or gene-deficient mice could be used as a high-throughput screening system to study AM development in vitro and in vivo. Our model is suitable to study the relationship between AM and lung tissue, as well as the roles of specific genes or factors in AM development and function. Furthermore, CSF2-cFLiMo can overcome the limitation in macrophage precursor numbers and be used as a therapeutic approach for PAP disease or in other macrophage-based cell therapies including lung emphysema, lung fibrosis, lung infectious disease and lung cancer (Byrne et al, 2016; Lee et al, 2016; Wilson et al, 2010). Finally, genetically modified and transferred CSF2-cFLiMo might facilitate the controlled expression of specific therapeutic proteins in the lung for disease treatment, and therefore, could represent an attractive alternative to non-specific gene delivery by viral vectors.', metadata={'title': 'Long-term culture of fetal monocyte precursors in vitro allowing the generation of bona fide alveolar macrophages in vivo', 'source': 'https://biorxiv.org/content/10.1101/2021.06.04.447115v2.full-text'}),
      0.9244399070739746),
     (Document(page_content='Next, we assessed whether CSF2-cFLiMo show therapeutic activity upon transfer into adult Csf2ra-/- mice, which had already developed PAP. Adult Csf2ra-/- mice were transferred i.t. with 0.5, 1 or 2 million CSF2-cFLiMo (Fig. 4E-G). Ten weeks after transfer, donor-derived AM were detectable in the BAL and lung of Csf2ra-/- only in recipients transferred with 2 million cells (Fig. 4F). The protein levels in the BAL from mice transferred with 2×106 cells were significantly lower when compared to naïve Csf2ra-/- mice, suggesting that transferred cells were able to reduce proteinosis, although not to the level of WT mice (Fig. 4G). However, CSF2-cFLiMo-derived AM exhibited higher expression of F4/80 and CD11b, and lower expression of Siglec-F and CD64 when compared to WT AM (Fig. E5A, B), indicating that the AM phenotype was not fully recapitulated but intermediate between AM-derived from CSF2-cFLiMo transferred to neonates and AM-derived from CSF2-cFLiMo transplanted to adult mice. These results show that CSF2-cFLiMo can reproduce AM phenotype and function most adequately only when transferred to neonatal Csf2ra-/- mice.', metadata={'title': 'Long-term culture of fetal monocyte precursors in vitro allowing the generation of bona fide alveolar macrophages in vivo', 'source': 'https://biorxiv.org/content/10.1101/2021.06.04.447115v2.full-text'}),
      0.9204541444778442),
     (Document(page_content='Next, we assessed whether CSF2-cFLiMo show therapeutic activity upon transfer into adult Csf2ra-/- mice, which had already developed PAP. Adult Csf2ra-/- mice were transferred i.t. with 0.5, 1 or 2 million CSF2-cFLiMo (Fig. 4E-G). Ten weeks after transfer, donor-derived AM were detectable in the BAL and lung of Csf2ra-/- only in recipients transferred with 2 million cells (Fig. 4F). The protein levels in the BAL from mice transferred with 2×106 cells were significantly lower when compared to naïve Csf2ra-/- mice, suggesting that transferred cells were able to reduce proteinosis, although not to the level of WT mice (Fig. 4G). However, CSF2-cFLiMo-derived AM exhibited higher expression of F4/80 and CD11b, and lower expression of Siglec-F and CD64 when compared to WT AM (Fig. E5A, B), indicating that the AM phenotype was not fully recapitulated but intermediate between AM-derived from CSF2-cFLiMo transferred to neonates and AM-derived from CSF2-cFLiMo transplanted to adult mice. These results show that CSF2-cFLiMo can reproduce AM phenotype and function most adequately only when transferred to neonatal Csf2ra-/- mice.', metadata={'title': 'Long-term culture of fetal monocyte precursors in vitro allowing the generation of bona fide alveolar macrophages in vivo', 'source': 'https://biorxiv.org/content/10.1101/2021.06.04.447115v2.full-text'}),
      0.9204541444778442),
     (Document(page_content='Overall, our studies demonstrate that CSF2-cFLiMo-AM were functionally equivalent to naturally differentiated AM. To determine the number of donor cells required to fully reconstitute the AM compartment of Csf2ra-/- mice, we titrated the number of transferred CSF2-cFLiMo (Fig. 4A). Transfer of a minimum of 5×104 CSF2-cFLiMo to neonatal Csf2ra-/- mice resulted in AM numbers in adult recipients that were comparable to unmanipulated WT mice (around 5×105) (Fig. 4B) and protected mice from PAP (Fig. 4C). We have previously established that around 10% of primary fetal liver monocytes supplied intranasally reach the lung (Li et al, 2020). Thus, CSF2-cFLiMo have expanded around 100-fold 6 weeks after transfer to Csf2ra-/- neonates. Notably, extended time of CSF2-cFLiMo in vitro culture (i.e. 4 months) prior transfer into recipient mice did not negatively affect their differentiation and functional capacity (Fig. 4B, C). Another critical function of tissue-resident macrophages including AM is the removal of apoptotic cells (efferocytosis) (Morioka et al, 2019). We compared efferocytosis between CSF2-cFLiMo-AM in Csf2ra-/- mice and AM in WT mice by intratracheal (i.t.) installation of labelled apoptotic thymocytes. CSF2-cFLiMo-AM and AM were equally potent at phagocytosing apoptotic cells from the bronchoalveolar space (Fig. 4D).', metadata={'title': 'Long-term culture of fetal monocyte precursors in vitro allowing the generation of bona fide alveolar macrophages in vivo', 'source': 'https://biorxiv.org/content/10.1101/2021.06.04.447115v2.full-text'}),
      0.9189490675926208)]



## From Graph


```python
# Now we initialize from existing graph
existing_graph = Neo4jVector.from_existing_graph(
    embedding=OpenAIEmbeddings(),
    index_name="vector",
    node_label="Chunk",
    text_node_properties=["text", "title"], # not all the properties, only those that contain text.
    embedding_node_property="embedding",
)


```


```python
type(existing_graph)
```




    langchain.vectorstores.neo4j_vector.Neo4jVector




```python
existing_graph.retrieve_existing_index()
```




    1536




```python
existing_graph.similarity_search('macrophage', k=1)
```




    [Document(page_content='\ntext: Tissue-resident macrophages (MFTR) are heterogeneous cell populations, present in almost all tissues and play multiple tissue-specific functions in homeostasis and diseases (Davies et al, 2013; Hoeffel & Ginhoux, 2015). MF-based therapies have been proposed as potential strategies in various diseases (Duan & Luo, 2021; Mass & Lachmann, 2021; Moroni et al, 2019; Peng et al, 2020).\ntitle: Long-term culture of fetal monocyte precursors in vitro allowing the generation of bona fide alveolar macrophages in vivo', metadata={'source': 'https://biorxiv.org/content/10.1101/2021.06.04.447115v2.full-text'})]



<a id='loading-docs'></a>
# Loading more Documents:



```python
for p in r.results[4:13]:
    try:
        store.add_documents(p.langchain_doc)
    except TypeError as e:
        warn(f'No HTML: {e}')
```

    Created a chunk of size 1197, which is longer than the specified 1000
    Created a chunk of size 1274, which is longer than the specified 1000
    Created a chunk of size 1647, which is longer than the specified 1000
    Created a chunk of size 1902, which is longer than the specified 1000
    Created a chunk of size 1529, which is longer than the specified 1000
    Created a chunk of size 1496, which is longer than the specified 1000
    Created a chunk of size 1123, which is longer than the specified 1000
    Created a chunk of size 1078, which is longer than the specified 1000
    Created a chunk of size 1122, which is longer than the specified 1000
    Created a chunk of size 1342, which is longer than the specified 1000
    Created a chunk of size 1292, which is longer than the specified 1000
    Created a chunk of size 1133, which is longer than the specified 1000
    Created a chunk of size 1627, which is longer than the specified 1000
    Created a chunk of size 1483, which is longer than the specified 1000
    Created a chunk of size 1387, which is longer than the specified 1000
    Created a chunk of size 1177, which is longer than the specified 1000
    Created a chunk of size 1695, which is longer than the specified 1000
    Created a chunk of size 1495, which is longer than the specified 1000
    Created a chunk of size 1233, which is longer than the specified 1000
    Created a chunk of size 1192, which is longer than the specified 1000
    Created a chunk of size 1187, which is longer than the specified 1000
    Created a chunk of size 1174, which is longer than the specified 1000
    Created a chunk of size 1123, which is longer than the specified 1000
    Created a chunk of size 1152, which is longer than the specified 1000
    Created a chunk of size 1570, which is longer than the specified 1000
    Created a chunk of size 1949, which is longer than the specified 1000
    Created a chunk of size 2081, which is longer than the specified 1000
    Created a chunk of size 1684, which is longer than the specified 1000
    Created a chunk of size 1417, which is longer than the specified 1000
    Created a chunk of size 1135, which is longer than the specified 1000
    Created a chunk of size 1802, which is longer than the specified 1000
    Created a chunk of size 2324, which is longer than the specified 1000
    Created a chunk of size 2531, which is longer than the specified 1000
    Created a chunk of size 2305, which is longer than the specified 1000
    Created a chunk of size 1827, which is longer than the specified 1000
    Created a chunk of size 1184, which is longer than the specified 1000
    Created a chunk of size 1262, which is longer than the specified 1000
    Created a chunk of size 1257, which is longer than the specified 1000
    Created a chunk of size 1333, which is longer than the specified 1000
    Created a chunk of size 1973, which is longer than the specified 1000
    Created a chunk of size 1119, which is longer than the specified 1000
    Created a chunk of size 1354, which is longer than the specified 1000
    Created a chunk of size 1713, which is longer than the specified 1000
    Created a chunk of size 2247, which is longer than the specified 1000
    Created a chunk of size 1141, which is longer than the specified 1000
    Created a chunk of size 1748, which is longer than the specified 1000
    Created a chunk of size 1078, which is longer than the specified 1000
    Created a chunk of size 1617, which is longer than the specified 1000
    Created a chunk of size 1177, which is longer than the specified 1000
    Created a chunk of size 2214, which is longer than the specified 1000
    Created a chunk of size 1250, which is longer than the specified 1000
    Created a chunk of size 2109, which is longer than the specified 1000
    Created a chunk of size 1155, which is longer than the specified 1000
    Created a chunk of size 1693, which is longer than the specified 1000
    Created a chunk of size 1464, which is longer than the specified 1000
    Created a chunk of size 1908, which is longer than the specified 1000
    Created a chunk of size 1051, which is longer than the specified 1000
    Created a chunk of size 1717, which is longer than the specified 1000
    Created a chunk of size 1895, which is longer than the specified 1000
    Created a chunk of size 1343, which is longer than the specified 1000
    Created a chunk of size 1392, which is longer than the specified 1000
    Created a chunk of size 1749, which is longer than the specified 1000
    Created a chunk of size 2950, which is longer than the specified 1000
    Created a chunk of size 1353, which is longer than the specified 1000
    Created a chunk of size 1181, which is longer than the specified 1000
    Created a chunk of size 1021, which is longer than the specified 1000
    Created a chunk of size 1893, which is longer than the specified 1000
    Created a chunk of size 1382, which is longer than the specified 1000
    Created a chunk of size 1572, which is longer than the specified 1000
    Created a chunk of size 1249, which is longer than the specified 1000
    Created a chunk of size 1352, which is longer than the specified 1000
    Created a chunk of size 1622, which is longer than the specified 1000
    Created a chunk of size 1245, which is longer than the specified 1000
    Created a chunk of size 1197, which is longer than the specified 1000
    Created a chunk of size 1637, which is longer than the specified 1000
    Created a chunk of size 1650, which is longer than the specified 1000
    Created a chunk of size 1328, which is longer than the specified 1000
    Created a chunk of size 1813, which is longer than the specified 1000
    Created a chunk of size 1379, which is longer than the specified 1000
    Created a chunk of size 1778, which is longer than the specified 1000
    Created a chunk of size 1105, which is longer than the specified 1000
    Created a chunk of size 1018, which is longer than the specified 1000
    Created a chunk of size 2206, which is longer than the specified 1000
    Created a chunk of size 1385, which is longer than the specified 1000
    Created a chunk of size 1368, which is longer than the specified 1000
    Created a chunk of size 1706, which is longer than the specified 1000
    Created a chunk of size 1203, which is longer than the specified 1000
    Created a chunk of size 1673, which is longer than the specified 1000
    Created a chunk of size 1012, which is longer than the specified 1000
    Created a chunk of size 1284, which is longer than the specified 1000
    Created a chunk of size 1192, which is longer than the specified 1000
    Created a chunk of size 1273, which is longer than the specified 1000
    Created a chunk of size 1116, which is longer than the specified 1000
    Created a chunk of size 1388, which is longer than the specified 1000
    Created a chunk of size 1274, which is longer than the specified 1000
    Created a chunk of size 1415, which is longer than the specified 1000
    Created a chunk of size 1022, which is longer than the specified 1000
    Created a chunk of size 1670, which is longer than the specified 1000
    Created a chunk of size 1016, which is longer than the specified 1000
    Created a chunk of size 1322, which is longer than the specified 1000
    Created a chunk of size 1037, which is longer than the specified 1000
    Created a chunk of size 2057, which is longer than the specified 1000
    Created a chunk of size 1567, which is longer than the specified 1000
    Created a chunk of size 3516, which is longer than the specified 1000
    Created a chunk of size 1450, which is longer than the specified 1000
    Created a chunk of size 1333, which is longer than the specified 1000
    Created a chunk of size 1638, which is longer than the specified 1000
    Created a chunk of size 1570, which is longer than the specified 1000
    Created a chunk of size 1050, which is longer than the specified 1000
    Created a chunk of size 1759, which is longer than the specified 1000
    Created a chunk of size 1635, which is longer than the specified 1000
    Created a chunk of size 1031, which is longer than the specified 1000
    Created a chunk of size 1163, which is longer than the specified 1000
    Created a chunk of size 1205, which is longer than the specified 1000
    Created a chunk of size 1091, which is longer than the specified 1000
    Created a chunk of size 1055, which is longer than the specified 1000
    Created a chunk of size 1069, which is longer than the specified 1000
    Created a chunk of size 1342, which is longer than the specified 1000
    Created a chunk of size 1072, which is longer than the specified 1000
    Created a chunk of size 1100, which is longer than the specified 1000
    Created a chunk of size 1867, which is longer than the specified 1000
    Created a chunk of size 1156, which is longer than the specified 1000
    Created a chunk of size 1286, which is longer than the specified 1000
    Created a chunk of size 1204, which is longer than the specified 1000
    Created a chunk of size 1156, which is longer than the specified 1000
    Created a chunk of size 1234, which is longer than the specified 1000
    Created a chunk of size 1305, which is longer than the specified 1000
    Created a chunk of size 1152, which is longer than the specified 1000
    Created a chunk of size 1416, which is longer than the specified 1000
    Created a chunk of size 1220, which is longer than the specified 1000
    Created a chunk of size 1152, which is longer than the specified 1000
    Created a chunk of size 1260, which is longer than the specified 1000
    Created a chunk of size 1947, which is longer than the specified 1000
    Created a chunk of size 1309, which is longer than the specified 1000
    Created a chunk of size 1383, which is longer than the specified 1000
    Created a chunk of size 1072, which is longer than the specified 1000
    Created a chunk of size 1083, which is longer than the specified 1000
    Created a chunk of size 1201, which is longer than the specified 1000
    Created a chunk of size 1724, which is longer than the specified 1000
    Created a chunk of size 1615, which is longer than the specified 1000
    Created a chunk of size 1414, which is longer than the specified 1000
    Created a chunk of size 1138, which is longer than the specified 1000
    Created a chunk of size 4048, which is longer than the specified 1000
    Created a chunk of size 1488, which is longer than the specified 1000
    Created a chunk of size 2798, which is longer than the specified 1000
    Created a chunk of size 1826, which is longer than the specified 1000
    Created a chunk of size 1408, which is longer than the specified 1000
    Created a chunk of size 1702, which is longer than the specified 1000
    Created a chunk of size 1395, which is longer than the specified 1000
    Created a chunk of size 1554, which is longer than the specified 1000
    Created a chunk of size 1246, which is longer than the specified 1000
    Created a chunk of size 1122, which is longer than the specified 1000
    Created a chunk of size 1284, which is longer than the specified 1000
    Created a chunk of size 1857, which is longer than the specified 1000
    Created a chunk of size 1193, which is longer than the specified 1000
    Created a chunk of size 1243, which is longer than the specified 1000
    Created a chunk of size 1626, which is longer than the specified 1000
    Created a chunk of size 1347, which is longer than the specified 1000
    Created a chunk of size 1461, which is longer than the specified 1000
    Created a chunk of size 1800, which is longer than the specified 1000
    Created a chunk of size 1129, which is longer than the specified 1000
    Created a chunk of size 1198, which is longer than the specified 1000
    Created a chunk of size 1185, which is longer than the specified 1000
    Created a chunk of size 1059, which is longer than the specified 1000
    Created a chunk of size 1456, which is longer than the specified 1000
    Created a chunk of size 1481, which is longer than the specified 1000
    Created a chunk of size 1138, which is longer than the specified 1000
    Created a chunk of size 1589, which is longer than the specified 1000
    Created a chunk of size 1674, which is longer than the specified 1000
    Created a chunk of size 1113, which is longer than the specified 1000
    Created a chunk of size 1109, which is longer than the specified 1000
    Created a chunk of size 1233, which is longer than the specified 1000
    Created a chunk of size 1981, which is longer than the specified 1000
    Created a chunk of size 3724, which is longer than the specified 1000
    Created a chunk of size 1729, which is longer than the specified 1000
    Created a chunk of size 1288, which is longer than the specified 1000
    Created a chunk of size 1951, which is longer than the specified 1000
    Created a chunk of size 1023, which is longer than the specified 1000
    Created a chunk of size 1137, which is longer than the specified 1000
    Created a chunk of size 1121, which is longer than the specified 1000
    Created a chunk of size 1686, which is longer than the specified 1000
    Created a chunk of size 1167, which is longer than the specified 1000
    Created a chunk of size 1119, which is longer than the specified 1000
    Created a chunk of size 1186, which is longer than the specified 1000
    Created a chunk of size 1067, which is longer than the specified 1000
    Created a chunk of size 1401, which is longer than the specified 1000
    Created a chunk of size 1495, which is longer than the specified 1000
    Created a chunk of size 1077, which is longer than the specified 1000
    Created a chunk of size 1446, which is longer than the specified 1000
    Created a chunk of size 1379, which is longer than the specified 1000
    Created a chunk of size 1294, which is longer than the specified 1000
    Created a chunk of size 1211, which is longer than the specified 1000
    Created a chunk of size 1156, which is longer than the specified 1000
    Created a chunk of size 1437, which is longer than the specified 1000
    Created a chunk of size 1751, which is longer than the specified 1000
    Created a chunk of size 1397, which is longer than the specified 1000
    Created a chunk of size 1613, which is longer than the specified 1000
    Created a chunk of size 1135, which is longer than the specified 1000
    Created a chunk of size 1066, which is longer than the specified 1000
    Created a chunk of size 1135, which is longer than the specified 1000
    Created a chunk of size 2279, which is longer than the specified 1000
    Created a chunk of size 1140, which is longer than the specified 1000
    Created a chunk of size 1768, which is longer than the specified 1000
    Created a chunk of size 2995, which is longer than the specified 1000
    Created a chunk of size 1922, which is longer than the specified 1000
    Created a chunk of size 1583, which is longer than the specified 1000
    Created a chunk of size 1047, which is longer than the specified 1000
    Created a chunk of size 1038, which is longer than the specified 1000
    Created a chunk of size 1014, which is longer than the specified 1000
    Created a chunk of size 1397, which is longer than the specified 1000
    /home/ted/code/nlp_etl_presentation/biorxivist/biorxivist/webtools.py:148: UserWarning: Unable to locate an anchor with the tags: {'data-panel-name': 'article_tab_full_text'}.
      warn(f'Unable to locate an anchor with the tags: {tag_dict}.')
    /tmp/ipykernel_47315/383292953.py:5: UserWarning: No HTML: The link must be a string completing a valid URL not <class 'NoneType'>.
      warn(f'No HTML: {e}')


# Setup `Neo4jVector` as a retreiver


```python
retriever = store.as_retriever()

```

## Questions Answering with Sources


```python
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
```


```python
chain = RetrievalQAWithSourcesChain.from_chain_type(
    ChatOpenAI(temperature=0), retriever=retriever
)
```


```python
answer = chain(
    {"question": "What is the role of TGF-beta 1 in monocyte maturation?"},
    return_only_outputs=True,
)
```


```python
answer
```




    {'answer': 'TGF-beta 1 plays a role in the development of cLP tissue-resident macrophages and is linked to the transition of monocytes to macrophages. Loss of TGFβ-Receptor on macrophages resulted in a minor impairment of macrophage differentiation.\n',
     'sources': 'https://biorxiv.org/content/10.1101/601963v1.full-text, https://biorxiv.org/content/10.1101/2021.06.04.447115v2.full-text'}




```python
answer = answer = chain(
    {"question": "How are mice used in TGF-bet 1 research?"},
    return_only_outputs=True,
)
```


```python
answer
```




    {'answer': 'Mice were infected with Helicobacter hepaticus (Hh) in TGF-bet 1 research.\n',
     'sources': 'https://biorxiv.org/content/10.1101/601963v1.full-text'}




```python
answer = answer = chain(
    {"question": "What factors have been found to impact the activity of alveolar macrophages?"},
    return_only_outputs=True,
)
```


```python
answer
```




    {'answer': 'Factors that impact the activity of alveolar macrophages include the presence of GM-CSF-induced PPARγ, absence of PPARγ, GM-CSF, or GM-CSFR subunits Csf2ra and Csf2rb, and mutations in CSF2RA and CSF2RB genes. Additionally, the differentiation of M-CSF-derived BMM or GM-CSF-derived BMM can lead to the development of alveolar macrophages.\n',
     'sources': 'https://biorxiv.org/content/10.1101/2021.06.04.447115v2.full-text'}




```python
answer = answer = chain(
    {"question": "What factors have been found to induce anti-inflamatory states in maturing monocytes?"},
    return_only_outputs=True,
)
```


```python
answer
```




    {'answer': 'The factors that have been found to induce anti-inflammatory states in maturing monocytes are TGFβ and IL10 cytokines.\n',
     'sources': 'https://biorxiv.org/content/10.1101/601963v1.full-text'}




```python
answer = answer = chain(
    {"question": "How have monocytes been linked to CXCL4 signaling?"},
    return_only_outputs=True,
)
```


```python
answer
```




    {'answer': 'Monocytes have been linked to CXCL4 signaling through the differentiation of monocyte-derived dendritic cells (moDCs) in the presence of CXCL4. This process was studied to understand the effects of CXCL4 on the trajectory of monocyte differentiation into moDCs and moDC maturation.\n',
     'sources': 'https://biorxiv.org/content/10.1101/807230v1.full-text'}




```python

```
