import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models
import os

#Filepath variable
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


#load id2word Dictionary
id2word = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))

#load Corpus iterator
mm = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))

print mm

#Extract topics
lda = models.ldamodel.LdaModel(corpus = mm, id2word = id2word, num_topics = 16, update_every=1, chunksize = 10, passes = 5)

lda.print_topics(16)



"""
Latest from abstracts
2014-05-16 15:00:16,256 : INFO : topic #0 (0.062): 0.041*perception + 0.039*interaction + 0.036*evaluation + 0.013*geovisualization + 0.002*causality + 0.002*analysis + 0.001*whiteboards + 0.001*reasoning + 0.001*diagrams + 0.000*icons
2014-05-16 15:00:16,257 : INFO : topic #1 (0.062): 0.020*classification + 0.014*level-of-detail + 0.014*collaboration + 0.010*taxonomy + 0.002*embedding + 0.001*oac + 0.000*time + 0.000*multi-scale + 0.000*visualization + 0.000*design
2014-05-16 15:00:16,257 : INFO : topic #2 (0.062): 0.029*multiresolution + 0.023*segmentation + 0.017*filtering + 0.017*simplification + 0.007*sampling + 0.006*reconstruction + 0.002*clutter + 0.002*overplotting + 0.002*lens + 0.002*scalability
2014-05-16 15:00:16,257 : INFO : topic #3 (0.062): 0.007*trajectories + 0.004*narrative + 0.004*viability + 0.004*surfaces + 0.002*optimization + 0.001*accessibility + 0.001*persistence + 0.000*subsets + 0.000*geovisualization + 0.000*classification
2014-05-16 15:00:16,257 : INFO : topic #4 (0.062): 0.033*streamlines + 0.004*curves + 0.003*events + 0.001*exemplar + 0.000*deformation + 0.000*trends + 0.000*template + 0.000*delaunay + 0.000*direction + 0.000*community
2014-05-16 15:00:16,258 : INFO : topic #5 (0.062): 0.010*framework + 0.009*theory + 0.009*merging + 0.005*constraints + 0.004*illumination + 0.004*vortex + 0.002*orientation + 0.001*grids + 0.001*bias + 0.001*election
2014-05-16 15:00:16,258 : INFO : topic #6 (0.062): 0.099*isosurfaces + 0.015*context + 0.015*trees + 0.012*interactive + 0.007*combinations + 0.006*community + 0.006*graphs + 0.005*exploration + 0.004*sparklines + 0.004*navigation
2014-05-16 15:00:16,258 : INFO : topic #7 (0.062): 0.024*hyperstreamlines + 0.018*out-of-core + 0.012*insight + 0.010*microscopy + 0.003*time-dependent + 0.003*blending + 0.001*biomedical + 0.001*medical + 0.001*text + 0.001*memory
2014-05-16 15:00:16,258 : INFO : topic #8 (0.062): 0.009*aggregation + 0.007*visibility + 0.006*entropy + 0.004*multi-variate + 0.004*comparative + 0.001*k-means + 0.000*delaunay + 0.000*template + 0.000*direction + 0.000*community
2014-05-16 15:00:16,259 : INFO : topic #9 (0.062): 0.013*color + 0.012*voronoi + 0.006*correlation + 0.006*x-ray + 0.002*directional + 0.002*scale + 0.002*2d + 0.002*points + 0.001*history + 0.001*rhetoric
2014-05-16 15:00:16,259 : INFO : topic #10 (0.062): 0.028*focus+context + 0.010*distortion + 0.010*template + 0.010*delaunay + 0.009*detail + 0.008*parameterization + 0.003*tracking + 0.002*search + 0.001*statistics + 0.000*multi-attribute
2014-05-16 15:00:16,259 : INFO : topic #11 (0.062): 0.019*design + 0.006*clustering + 0.004*trends + 0.002*aesthetics + 0.002*highlighting + 0.001*requirements + 0.001*prototypes + 0.001*sketching + 0.000*evaluation + 0.000*events
2014-05-16 15:00:16,259 : INFO : topic #12 (0.062): 0.019*shading + 0.012*experiment + 0.003*transparency + 0.002*painting + 0.001*features + 0.000*delaunay + 0.000*template + 0.000*direction + 0.000*community + 0.000*overplotting
2014-05-16 15:00:16,260 : INFO : topic #13 (0.062): 0.055*visualization + 0.026*gpu + 0.013*clusters + 0.004*occlusion + 0.002*time-varying + 0.001*lines + 0.001*engagement + 0.000*validation + 0.000*overplotting + 0.000*clutter
2014-05-16 15:00:16,260 : INFO : topic #14 (0.062): 0.022*motion + 0.018*uncertainty + 0.006*direction + 0.000*layout + 0.000*attention + 0.000*perception + 0.000*template + 0.000*delaunay + 0.000*classification + 0.000*community
2014-05-16 15:00:16,260 : INFO : topic #15 (0.062): 0.012*animation + 0.010*scatterplots + 0.010*glyphs + 0.004*preprocessing + 0.004*light + 0.002*maps + 0.002*interpolation + 0.001*automotive + 0.000*filtering + 0.000*template
[Finished in 9.7s]"""