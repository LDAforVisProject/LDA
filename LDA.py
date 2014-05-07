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
2014-05-06 17:57:25,243 : INFO : topic #0 (0.062): 0.104*flow visualization + 0.024*feature extraction + 0.016*vortex breakdown + 0.014*filters + 0.014*reaction-diffusion + 0.012*visual debugging + 0.012*tensor field visualization + 0.011*engine simulation + 0.011*computational fluid dynamics (cfd) + 0.011*vortex analysis
2014-05-06 17:57:25,243 : INFO : topic #1 (0.062): 0.025*surface reconstruction + 0.018*knowledge discovery + 0.017*data exploration + 0.016*confocal microscopy + 0.011*network security + 0.011*network sampling + 0.010*social networks + 0.010*level set method + 0.010*shock filter + 0.010*point sampled data
2014-05-06 17:57:25,243 : INFO : topic #2 (0.062): 0.071*isosurfaces + 0.016*raycasting + 0.015*meshing + 0.015*molecular visualization + 0.014*visibility culling + 0.014*body-centered cubic lattice + 0.013*smooth surfaces + 0.013*guaranteed quality triangulation + 0.013*large data visualization + 0.012*cognitive walkthrough
2014-05-06 17:57:25,244 : INFO : topic #3 (0.062): 0.047*scientific visualization + 0.029*gpu + 0.021*line integral convolution + 0.018*visual knowledge discovery + 0.017*multi-dimensional scaling + 0.016*unstructured data + 0.014*public space + 0.013*strain tensor + 0.012*applications of volume graphics and volume visualization + 0.012*earth / space / and environmental sciences visualization
2014-05-06 17:57:25,244 : INFO : topic #4 (0.062): 0.064*volume visualization + 0.028*diffusion tensor imaging + 0.017*segmented data + 0.015*computer graphics + 0.014*treemaps + 0.013*proteomics + 0.012*silhouette enhancement + 0.012*focus+context techniques + 0.011*stress tensor + 0.011*non-photorealistic techniques
2014-05-06 17:57:25,244 : INFO : topic #5 (0.062): 0.053*visualization + 0.043*perception + 0.022*isosurface extraction + 0.018*topology preservation + 0.017*augmented reality + 0.015*space-time finite elements + 0.013*discontinuous galerkin methods + 0.013*human-computer interaction + 0.012*archaeology + 0.011*unstructured grids
2014-05-06 17:57:25,245 : INFO : topic #6 (0.062): 0.049*graphics hardware + 0.040*graph visualization + 0.024*programmable graphics hardware + 0.015*uncertainty visualization + 0.014*external memory algorithms + 0.013*volume raycasting + 0.012*implicit stream flow + 0.012*small world graphs + 0.011*motion estimation + 0.011*motion visualization
2014-05-06 17:57:25,245 : INFO : topic #7 (0.062): 0.035*parallel coordinates + 0.026*segmentation + 0.017*multiresolution + 0.015*vector fields + 0.015*high-dimensional data + 0.014*simplification + 0.013*user interfaces + 0.011*feature animation + 0.011*delaunay triangulation + 0.010*line data
2014-05-06 17:57:25,245 : INFO : topic #8 (0.062): 0.125*information visualization + 0.015*toolkits + 0.013*density-based visualization + 0.011*aggregated data + 0.011*event analysis + 0.011*dynamic visualization + 0.009*injection system + 0.009*collaboration + 0.009*user model + 0.008*wikipedia
2014-05-06 17:57:25,246 : INFO : topic #9 (0.062): 0.058*visual analytics + 0.020*focus+context + 0.018*degenerate tensors + 0.016*hyperstreamlines + 0.014*gpu rendering + 0.013*symmetric tensors + 0.013*finite-difference- time-domain (fdtd) + 0.013*c-aperture + 0.012*topological lines + 0.011*cluster-based visualization
2014-05-06 17:57:25,246 : INFO : topic #10 (0.062): 0.084*volume rendering + 0.026*transfer function + 0.022*streamlines + 0.020*non-photorealistic rendering + 0.018*virtual endoscopy + 0.016*3d vector field visualization + 0.012*progressive rendering + 0.012*projected tetrahedra + 0.012*classification + 0.011*features in volume data sets
2014-05-06 17:57:25,246 : INFO : topic #11 (0.062): 0.027*visualization systems + 0.021*large data + 0.018*cut-planes + 0.016*motion + 0.015*vessel visualization + 0.014*curved planar reformation + 0.014*out-of-core methods + 0.013*hierarchical clustering + 0.012*exploratory data analysis + 0.011*interactive
2014-05-06 17:57:25,246 : INFO : topic #12 (0.062): 0.021*exploratory visualization + 0.019*computational geometry and object modeling + 0.017*coordination + 0.012*human visual system + 0.011*color + 0.011*knot theory + 0.011*user study + 0.010*coordinated queries + 0.010*ray coherence + 0.010*empty space skipping
2014-05-06 17:57:25,247 : INFO : topic #13 (0.062): 0.033*interaction + 0.026*evaluation + 0.022*city block + 0.019*situation awareness + 0.017*line placement + 0.016*finite element modeling + 0.015*uncertainty + 0.012*virtual reality + 0.011*adjacency matrix + 0.009*contours
2014-05-06 17:57:25,247 : INFO : topic #14 (0.062): 0.019*visual data mining + 0.014*design + 0.014*3d visualization + 0.013*principal component analysis + 0.011*undo/redo + 0.010*real-time visualization + 0.010*large volumetric data + 0.010*point-based rendering + 0.010*constructive solid geometry + 0.010*hierarchies
2014-05-06 17:57:25,247 : INFO : topic #15 (0.062): 0.024*graph drawing + 0.018*data mining + 0.017*time series + 0.016*spectating + 0.016*point-based visualization + 0.015*visualization in medicine + 0.015*shading + 0.014*tractography + 0.012*dynamic layout + 0.012*large data set visualization
"""