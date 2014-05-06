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

#Extract topics
lda = models.ldamodel.LdaModel(corpus = mm, id2word = id2word, num_topics = 20, update_every=1, chunksize = 10, passes = 5)

lda.print_topics(20)

"""
2014-05-06 15:33:29,188 : INFO : topic #0 (0.050): 0.077*volume visualization + 0.047*graph visualization + 0.020*segmented data + 0.018*uncertainty visualization + 0.016*external memory algorithms + 0.015*silhouette enhancement + 0.014*focus+context techniques + 0.014*small world graphs + 0.013*multi-variate visualization + 0.013*non-photorealistic techniques
2014-05-06 15:33:29,188 : INFO : topic #1 (0.050): 0.060*graphics hardware + 0.060*visualization + 0.029*programmable graphics hardware + 0.015*implicit stream flow + 0.014*human-computer interaction + 0.014*motion estimation + 0.014*motion visualization + 0.014*eigenvector analysis + 0.012*mathematical visualization + 0.011* visualization
2014-05-06 15:33:29,188 : INFO : topic #2 (0.050): 0.107*volume rendering + 0.033*transfer function + 0.023*virtual endoscopy + 0.016*confocal microscopy + 0.015*progressive rendering + 0.015*projected tetrahedra + 0.015*classification + 0.012*filtering + 0.012*level-of-detail + 0.011*volume reconstruction
2014-05-06 15:33:29,189 : INFO : topic #3 (0.050): 0.031*city block + 0.024*line placement + 0.021*shading + 0.016*unstructured grids + 0.013*astronomy + 0.010*photometric calibration + 0.010*layered surfaces + 0.009*multi-attribute visualization + 0.009*resource allocation + 0.009*time-dependent attributes
2014-05-06 15:33:29,189 : INFO : topic #4 (0.050): 0.028*surface reconstruction + 0.021*computer graphics + 0.019*treemaps + 0.015*principal component analysis + 0.013*trees + 0.013*surface representation + 0.013*mpu implicits + 0.011*wave subspaces + 0.011*kullback-leibler decomposition + 0.011*waves
2014-05-06 15:33:29,189 : INFO : topic #5 (0.050): 0.055*scientific visualization + 0.020*meshing + 0.018*coordination + 0.018*unstructured data + 0.018*guaranteed quality triangulation + 0.018*smooth surfaces + 0.016*3d visualization + 0.013*human visual system + 0.012*morse-smale complex + 0.012*color
2014-05-06 15:33:29,190 : INFO : topic #6 (0.050): 0.039*visualization systems + 0.021*visibility culling + 0.020*large data visualization + 0.015*plenoptic opacity function + 0.015*volume splatting + 0.015*hardware acceleration + 0.014*knot theory + 0.014*xml + 0.014*visualization reference models + 0.013*network sampling
2014-05-06 15:33:29,190 : INFO : topic #7 (0.050): 0.029*streamlines + 0.023*exploratory visualization + 0.022*focus+context + 0.021*3d vector field visualization + 0.020*degenerate tensors + 0.017*hyperstreamlines + 0.015*hierarchical clustering + 0.015*features in volume data sets + 0.015*symmetric tensors + 0.015*path lines
2014-05-06 15:33:29,190 : INFO : topic #8 (0.050): 0.127*flow visualization + 0.029*feature extraction + 0.021*visual data mining + 0.019*vortex breakdown + 0.017*reaction-diffusion + 0.013*computational fluid dynamics (cfd) + 0.013*engine simulation + 0.013*cutting planes + 0.013*vortex analysis + 0.013*undo/redo
2014-05-06 15:33:29,190 : INFO : topic #9 (0.050): 0.030*non-photorealistic rendering + 0.027*isosurface extraction + 0.023*topology preservation + 0.021*spectating + 0.017*finite-difference- time-domain (fdtd) + 0.017*c-aperture + 0.012*process visualization + 0.012*p2p file-sharing networks visualization + 0.012*empty space skipping + 0.012*ray coherence
2014-05-06 15:33:29,191 : INFO : topic #10 (0.050): 0.020*visualization in medicine + 0.019*filters + 0.018*tractography + 0.017*visual debugging + 0.017*tensor field visualization + 0.014*large data set visualization + 0.014*spring embedder + 0.012*multi-resolution + 0.011*spherical space + 0.011*non-euclidean geometry
2014-05-06 15:33:29,191 : INFO : topic #11 (0.050): 0.036*large data + 0.023*data mining + 0.021*augmented reality + 0.021*knowledge discovery + 0.021*data exploration + 0.018*out-of-core methods + 0.015*interactive + 0.014*interactive visualization + 0.013*network security + 0.012*data flow networks
2014-05-06 15:33:29,191 : INFO : topic #12 (0.050): 0.136*information visualization + 0.026*graph drawing + 0.019*visual knowledge discovery + 0.018*time series + 0.015*density-based visualization + 0.013*dynamic layout + 0.012*aggregated data + 0.012*event analysis + 0.012*dynamic visualization + 0.010*injection system
2014-05-06 15:33:29,192 : INFO : topic #13 (0.050): 0.078*visual analytics + 0.021*toolkits + 0.019*volume raycasting + 0.019*gpu rendering + 0.016*applications of volume graphics and volume visualization + 0.016*earth / space / and environmental sciences visualization + 0.011*2d/3d combination display + 0.011*body-centered cubic grid + 0.011*radial basis function interpolation + 0.011*microarray data
2014-05-06 15:33:29,192 : INFO : topic #14 (0.050): 0.079*isosurfaces + 0.026*segmentation + 0.017*raycasting + 0.017*multiresolution + 0.016*molecular visualization + 0.015*vessel visualization + 0.015*body-centered cubic lattice + 0.015*feature detection + 0.015*vector fields + 0.014*curved planar reformation
2014-05-06 15:33:29,192 : INFO : topic #15 (0.050): 0.044*parallel coordinates + 0.022*motion + 0.019*high-dimensional data + 0.016*user interfaces + 0.016*virtual reality + 0.014*feature animation + 0.011*boids + 0.011*artificial life + 0.010*scatterplots + 0.010*multi-variate data
2014-05-06 15:33:29,192 : INFO : topic #16 (0.050): 0.026*cut-planes + 0.024*computational geometry and object modeling + 0.021*point-based visualization + 0.020*proteomics + 0.017*cognitive walkthrough + 0.014*differential proteomics + 0.014*difference visualization + 0.013*large volumetric data + 0.013*real-time visualization + 0.013*point-based rendering
2014-05-06 15:33:29,193 : INFO : topic #17 (0.050): 0.018*space-time finite elements + 0.018*design + 0.017*discontinuous galerkin methods + 0.015*archaeology + 0.015*unsteady flow visualization + 0.013*visual structure + 0.013*visual clutter + 0.013*view-dependent visualization + 0.013*adaptive textures + 0.013*out-of-core algorithm
2014-05-06 15:33:29,193 : INFO : topic #18 (0.050): 0.057*perception + 0.044*interaction + 0.035*evaluation + 0.025*situation awareness + 0.021*finite element modeling + 0.020*uncertainty + 0.014*adjacency matrix + 0.012*contours + 0.011*geovisualization + 0.007*network visualization
2014-05-06 15:33:29,193 : INFO : topic #19 (0.050): 0.041*diffusion tensor imaging + 0.037*gpu + 0.027*line integral convolution + 0.022*multi-dimensional scaling + 0.018*public space + 0.016*strain tensor + 0.014*cluster-based visualization + 0.012*social networks + 0.010*tensor field + 0.009*illustrative rendering
"""