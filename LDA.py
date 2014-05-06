import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from nltk.corpus import stopwords
import os

#Filepath variable
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


#load id2word Dictionary
id2word = corpora.Dictionary.load(os.path.join(__location__, '/tmp/KeyVis.dict'))

#load Corpus iterator
mm = corpora.MmCorpus(os.path.join(__location__, 'KeyVis_tfidf.mm'))

print mm

#Extract 100 LDA topics, using 1 pass and updating every 1 chunk (10,000 documents)
lda = models.ldamodel.LdaModel(corpus = mm, id2word = id2word, num_topics = 20, update_every=1, chunksize = 100, passes = 3)

lda.print_topics(20)

"""
2014-05-06 15:20:31,342 : INFO : topic #0 (0.050): 0.342*data + 0.044*reconstruction + 0.016*visibility + 0.013*bioinformatics + 0.010*comparative + 0.009*shading + 0.007*multiresolution + 0.005*multi-field + 0.004*amr + 0.003*clusters
2014-05-06 15:20:31,342 : INFO : topic #1 (0.050): 0.048*multi-variate + 0.033*lines + 0.015*perception + 0.012*maps + 0.011*hierarchical + 0.003*persistence + 0.000*time + 0.000*shaders + 0.000*out-of-core + 0.000*data
2014-05-06 15:20:31,342 : INFO : topic #2 (0.050): 0.056*space + 0.024*3d + 0.018*cartography + 0.014*memory + 0.010*search + 0.004*saliency + 0.002*x-ray + 0.000*diagrams + 0.000*graphics + 0.000*shaders
2014-05-06 15:20:31,342 : INFO : topic #3 (0.050): 0.080*clustering + 0.011*occlusion + 0.010*memory + 0.008*delaunay + 0.003*focus+context + 0.002*scale + 0.002*multi-scale + 0.000*interactive + 0.000*shaders + 0.000*out-of-core
2014-05-06 15:20:31,343 : INFO : topic #4 (0.050): 0.185*graphics + 0.072*interactive + 0.019*surfaces + 0.010*layer + 0.005*concordance + 0.005*texton + 0.000*bioinformatics + 0.000*space + 0.000*shaders + 0.000*visualization
2014-05-06 15:20:31,343 : INFO : topic #5 (0.050): 0.138*analysis + 0.068*interaction + 0.018*uncertainty + 0.004*time-dependent + 0.003*aggregation + 0.003*correlation + 0.000*visualization + 0.000*data + 0.000*toponomics + 0.000*microscopy
2014-05-06 15:20:31,343 : INFO : topic #6 (0.050): 0.042*exploration + 0.018*text + 0.007*probability + 0.002*symmetry + 0.000*visualization + 0.000*parallel + 0.000*shaders + 0.000*interactive + 0.000*data + 0.000*out-of-core
2014-05-06 15:20:31,343 : INFO : topic #7 (0.050): 0.044*vortex + 0.031*browsing + 0.006*calibration + 0.000*data + 0.000*parallel + 0.000*tracking + 0.000*shaders + 0.000*out-of-core + 0.000*visibility + 0.000*memory
2014-05-06 15:20:31,344 : INFO : topic #8 (0.050): 0.041*time-varying + 0.014*reasoning + 0.009*streamlines + 0.006*terrain + 0.000*color + 0.000*visualization + 0.000*interaction + 0.000*shaders + 0.000*data + 0.000*out-of-core
2014-05-06 15:20:31,344 : INFO : topic #9 (0.050): 0.053*layout + 0.005*aesthetics + 0.005*microscopy + 0.003*toponomics + 0.003*ensemble + 0.002*requirements + 0.000*data + 0.000*interaction + 0.000*time + 0.000*shaders
2014-05-06 15:20:31,344 : INFO : topic #10 (0.050): 0.020*gpu + 0.017*deformation + 0.015*fisheye + 0.011*motion + 0.010*raycasting + 0.006*timeline + 0.005*medical + 0.001*shaders + 0.000*out-of-core + 0.000*visibility
2014-05-06 15:20:31,344 : INFO : topic #11 (0.050): 0.085*shaders + 0.014*theory + 0.007*isosurfaces + 0.002*outflow + 0.002*transitions + 0.000*visualization + 0.000*out-of-core + 0.000*visibility + 0.000*memory + 0.000*context
2014-05-06 15:20:31,344 : INFO : topic #12 (0.050): 0.106*topology + 0.021*grids + 0.011*curve-skeleton + 0.008*toolkits + 0.000*visualization + 0.000*shaders + 0.000*out-of-core + 0.000*visibility + 0.000*memory + 0.000*context
2014-05-06 15:20:31,345 : INFO : topic #13 (0.050): 0.053*time + 0.014*resampling + 0.010*quasi-tree + 0.008*light + 0.007*trajectories + 0.007*anisotropic + 0.000*evaluation + 0.000*comparative + 0.000*perception + 0.000*layout
2014-05-06 15:20:31,345 : INFO : topic #14 (0.050): 0.025*mesh + 0.025*features + 0.024*sampling + 0.012*framework + 0.008*multi-resolution + 0.008*treemaps + 0.006*history + 0.005*segmentation + 0.000*design + 0.000*visualization
2014-05-06 15:20:31,345 : INFO : topic #15 (0.050): 0.021*color + 0.017*voronoi + 0.015*interpolation + 0.012*textures + 0.006*simplification + 0.003*compression + 0.000*shaders + 0.000*out-of-core + 0.000*data + 0.000*visibility
2014-05-06 15:20:31,345 : INFO : topic #16 (0.050): 0.431*visualization + 0.028*tracking + 0.025*parallel + 0.025*networks + 0.020*out-of-core + 0.011*biomedical + 0.011*glyphs + 0.007*cognition + 0.005*geospatial + 0.002*genealogy
2014-05-06 15:20:31,345 : INFO : topic #17 (0.050): 0.072*design + 0.047*tractography + 0.010*mapping + 0.009*simulation + 0.009*navigation + 0.007*entropy + 0.007*animation + 0.004*collaboration + 0.003*scalability + 0.003*movement
2014-05-06 15:20:31,346 : INFO : topic #18 (0.050): 0.079*evaluation + 0.046*multi-dimensional + 0.003*trees + 0.000*clustering + 0.000*shaders + 0.000*out-of-core + 0.000*visibility + 0.000*visualization + 0.000*data + 0.000*memory
2014-05-06 15:20:31,346 : INFO : topic #19 (0.050): 0.061*exploratory + 0.014*diagrams + 0.014*graphs + 0.014*context + 0.012*routing + 0.008*distortion + 0.008*ranking + 0.007*illumination + 0.007*orientation + 0.000*data
"""