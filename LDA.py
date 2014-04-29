import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from nltk.corpus import stopwords


#load id2word Dictionary
id2word = corpora.Dictionary.load('/Users/charleywu/Github/LDA/tmp/KeyVis.dict')

#load Corpus iterator
mm = corpora.MmCorpus('/Users/charleywu/Github/LDA/tmp/KeyVis_tfidf.mm')

print mm

#Extract 100 LDA topics, using 1 pass and updating every 1 chunk (10,000 documents)
lda = models.ldamodel.LdaModel(corpus = mm, id2word = id2word, num_topics = 20, update_every=1, chunksize = 100, passes = 3)

lda.print_topics(20)

"""2014-04-29 17:41:49,998 : INFO : topic #0 (0.050): 0.079*transfer + 0.070*function + 0.065*network + 0.056*design + 0.046*vessel + 0.043*unstructured + 0.041*tractography + 0.031*lighting + 0.027*history + 0.022*grids
2014-04-29 17:41:49,998 : INFO : topic #1 (0.050): 0.112*surface + 0.067*feature + 0.054*point-based + 0.032*web + 0.030*non-photorealistic + 0.026*mapping + 0.026*estimation + 0.022*geographic + 0.018*biomedical + 0.017*selection
2014-04-29 17:41:49,998 : INFO : topic #2 (0.050): 0.085*field + 0.068*clustering + 0.043*imaging + 0.036*isosurface + 0.036*contour + 0.033*drawing + 0.031*smooth + 0.031*triangulation + 0.021*pixel + 0.021*diagrams
2014-04-29 17:41:49,998 : INFO : topic #3 (0.050): 0.056*reconstruction + 0.042*systems + 0.032*computational + 0.031*processing + 0.031*line + 0.029*bioinformatics + 0.027*proteomics + 0.026*distributed + 0.024*fairing + 0.023*differential
2014-04-29 17:41:49,998 : INFO : topic #4 (0.050): 0.106*graphics + 0.105*large + 0.056*techniques + 0.031*energy + 0.029*data + 0.029*shading + 0.027*temporal + 0.025*cubes + 0.021*marching + 0.019*projection
2014-04-29 17:41:49,999 : INFO : topic #5 (0.050): 0.116*tensor + 0.099*focus+context + 0.055*information + 0.049*diffusion + 0.034*solid + 0.031*texture + 0.025*geospatial + 0.024*illustrative + 0.022*reality + 0.020*visualization
2014-04-29 17:41:49,999 : INFO : topic #6 (0.050): 0.173*flow + 0.077*extraction + 0.051*vortex + 0.051*visualization + 0.039*particle + 0.035*/ + 0.029*bifurcations + 0.028*blood + 0.028*unsteady + 0.025*glyphs
2014-04-29 17:41:49,999 : INFO : topic #7 (0.050): 0.076*analysis + 0.069*interactive + 0.056*data + 0.049*time-varying + 0.049*exploration + 0.047*image + 0.039*space + 0.032*finite + 0.031*" + 0.028*method
2014-04-29 17:41:49,999 : INFO : topic #8 (0.050): 0.100*topology + 0.070*graph + 0.028*splatting + 0.028*sampling + 0.027*semantic + 0.026*simulation + 0.026*dynamics + 0.025*time-dependent + 0.025*interpolation + 0.024*software
2014-04-29 17:41:49,999 : INFO : topic #9 (0.050): 0.080*scientific + 0.061*hardware + 0.058*vector + 0.052*3d + 0.052*out-of-core + 0.040*streamlines + 0.033*view-dependent + 0.032*microscopy + 0.031*visualization + 0.030*fields
2014-04-29 17:41:50,000 : INFO : topic #10 (0.050): 0.063*surfaces + 0.054*views + 0.050*molecular + 0.040*coordinated + 0.035*multiple + 0.030*trees + 0.030*human + 0.029*tracing + 0.026*filtering + 0.023*level
2014-04-29 17:41:50,000 : INFO : topic #11 (0.050): 0.145*volume + 0.140*rendering + 0.058*gpu + 0.033*shaders + 0.031*raycasting + 0.030*programmable + 0.026*mesh + 0.021*statistical + 0.019*hardware + 0.017*spatial
2014-04-29 17:41:50,000 : INFO : topic #12 (0.050): 0.111*medicine + 0.103*motion + 0.043*endoscopy + 0.042*animation + 0.040*surgery + 0.025*artificial + 0.018*planning + 0.018*visualization + 0.016*charts + 0.015*distortion
2014-04-29 17:41:50,000 : INFO : topic #13 (0.050): 0.077*detection + 0.073*perception + 0.054*networks + 0.049*tensors + 0.040*geometry + 0.036*realtime + 0.029*enhancement + 0.029*illustration + 0.027*degenerate + 0.024*hyperstreamlines
2014-04-29 17:41:50,000 : INFO : topic #14 (0.050): 0.053*user + 0.048*data + 0.046*multi-dimensional + 0.044*modeling + 0.040*parallel + 0.040*set + 0.038*coordinates + 0.036*lines + 0.033*visualization + 0.029*information
2014-04-29 17:41:50,001 : INFO : topic #15 (0.050): 0.090*evaluation + 0.060*knowledge + 0.046*functions + 0.044*discovery + 0.042*visual + 0.033*representation + 0.030*curved + 0.029*security + 0.029*analytics + 0.028*sensemaking
2014-04-29 17:41:50,001 : INFO : topic #16 (0.050): 0.051*multi-variate + 0.044*exploratory + 0.042*virtual + 0.039*color + 0.039*data + 0.037*classification + 0.035*visualization + 0.034*time + 0.032*topological + 0.032*information
2014-04-29 17:41:50,001 : INFO : topic #17 (0.050): 0.102*isosurfaces + 0.061*mining + 0.050*uncertainty + 0.044*layout + 0.041*methods + 0.040*haptics + 0.039*theory + 0.036*social + 0.029*computer + 0.028*management
2014-04-29 17:41:50,001 : INFO : topic #18 (0.050): 0.060*tree + 0.048*treemaps + 0.044*model + 0.044*models + 0.038*multiresolution + 0.033*graphs + 0.031*multi-scale + 0.031*comparison + 0.029*query + 0.028*quality
2014-04-29 17:41:50,001 : INFO : topic #19 (0.050): 0.093*visual + 0.091*interaction + 0.089*analytics + 0.044*tracking + 0.038*system + 0.030*human-computer + 0.027*geovisualization + 0.024*scalable + 0.022*hierarchies + 0.022*spatio-temporal
[Finished in 2.7s]"""