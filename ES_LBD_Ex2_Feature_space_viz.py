#		python code
#		script_name: Feature_space_viz
#
#		author: Anna Xambó
#		description: Scatter plot of two different instruments. We need to add a sound of silence in one track of the DAW to make P5 work. Press Run, click on the Processing icon, and then press play.
#

from earsketch import *
#from math import *

init()
setTempo(120)

# Added a sound of silence, workaround to make P5 work (it needs an audio file in the DAW)
fitMedia(TESTSTUDIO_SILENCE,1,1,3)

# Visualization setup
group1_legend = "strings"
group2_legend = "electric bass"
group1_color = "#000000"
group2_color = "#999999"
text_color = "#000000"
background_color = "#FFFFFF"
size_marker = 8

# Dataset
# TODO a more automatic way to pull lists of genres?
group1_files = [RD_CINEMATIC_SCORE_STRINGS_1, RD_CINEMATIC_SCORE_STRINGS_2, RD_CINEMATIC_SCORE_STRINGS_3, RD_CINEMATIC_SCORE_STRINGS_4, RD_CINEMATIC_SCORE_STRINGS_5, RD_CINEMATIC_SCORE_STRINGS_6, RD_CINEMATIC_SCORE_STRINGS_7, RD_CINEMATIC_SCORE_STRINGS_8, RD_CINEMATIC_SCORE_STRINGS_9, RD_CINEMATIC_SCORE_STRINGS_10, RD_CINEMATIC_SCORE_STRINGS_11, RD_CINEMATIC_SCORE_STRINGS_12, RD_CINEMATIC_SCORE_STRINGS_13, RD_CINEMATIC_SCORE_STRINGS_14, RD_CINEMATIC_SCORE_STRINGS_15, RD_CINEMATIC_SCORE_STRINGS_16, RD_RNB_ACOUSTIC_NYLONSTRING_1, RD_RNB_ACOUSTIC_NYLONSTRING_2, RD_RNB_ACOUSTIC_NYLONSTRING_3, RD_RNB_ACOUSTIC_NYLONSTRING_4, RD_RNB_ACOUSTIC_NYLONSTRING_5, RD_RNB_ACOUSTIC_NYLONSTRING_6, RD_RNB_ACOUSTIC_NYLONSTRING_7, RD_WORLD_PERCUSSION_ETHNICSTRING_1, RD_WORLD_PERCUSSION_ETHNICSTRING_2, RD_WORLD_PERCUSSION_ETHNICSTRING_3, RD_WORLD_PERCUSSION_ETHNICSTRING_4, RD_WORLD_PERCUSSION_ETHNICSTRING_5]

group2_files = [RD_EDM_WARMBASSLINE_1, RD_EDM_WOBBLEBASS_1, RD_ROCK_POPELECTRICBASS_1,RD_ROCK_POPELECTRICBASS_2, RD_ROCK_POPELECTRICBASS_3, RD_ROCK_POPELECTRICBASS_4, RD_ROCK_POPELECTRICBASS_5, RD_ROCK_POPELECTRICBASS_6, RD_ROCK_POPELECTRICBASS_7, RD_ROCK_POPELECTRICBASS_8, RD_ROCK_POPELECTRICBASS_9, RD_ROCK_POPELECTRICBASS_10, RD_ROCK_POPELECTRICBASS_11, RD_ROCK_POPELECTRICBASS_12, RD_ROCK_POPELECTRICBASS_13, RD_ROCK_POPELECTRICBASS_14, RD_ROCK_POPELECTRICBASS_15, RD_ROCK_POPELECTRICBASS_16, RD_ROCK_POPELECTRICBASS_17, RD_ROCK_POPELECTRICBASS_18, RD_ROCK_POPELECTRICBASS_19, RD_ROCK_POPELECTRICBASS_20, RD_ROCK_POPELECTRICBASS_21, RD_ROCK_POPELECTRICBASS_22, RD_ROCK_POPELECTRICBASS_23, RD_ROCK_POPELECTRICBASS_24, RD_ROCK_POPELECTRICBASS_25]

# Analysis setup
# A vector of 2 vectors (one for each feature) for each sound collection.
# [[feature1_audio1, feature1_audio2,...],[feature2_audio1, feature2_audio2...]]
group1_files_features = [[] for x in xrange(2)]
group2_files_features = [[] for x in xrange(2)]
group1_files_features_norm = [[] for x in xrange(2)]
group2_files_features_norm = [[] for x in xrange(2)]

def extractFeaturesFromDataset(dataset, featuresVector):
  if (len(dataset) < 2): 
    print("Add more than one sound to the collection")
  else:
    for i in range(0, len(dataset)):
      feature1 = analyze(dataset[i], SPECTRAL_CENTROID)
      feature2 = analyze(dataset[i], RMS_AMPLITUDE)
      featuresVector[0].append(float(feature1))
      featuresVector[1].append(float(feature2))

def normalize(value, minval, maxval):
  rangeMinMax = maxval - minval
  return (value - minval) / rangeMinMax 

def normalizeFeaturesVector(featuresVector, normFeaturesVector):
  # Normalize value by value starting by feature
  for i in range(0, 2):
  # Go value by value of featuresVector and compute a normalized value in normFeaturesVector
    for j in range(0, len(featuresVector[0])):
      result = normalize(featuresVector[i][j], min(featuresVector[i]), max(featuresVector[i]))
      normFeaturesVector[i].append(float(result))
    
extractFeaturesFromDataset(group1_files, group1_files_features)
extractFeaturesFromDataset(group2_files, group2_files_features)

normalizeFeaturesVector(group1_files_features, group1_files_features_norm)
normalizeFeaturesVector(group2_files_features, group2_files_features_norm)

# Plot
# TODO on rollover show audio filename
def onLoop():
  drawRectangle(0,0,getCanvasWidth(), getCanvasHeight(), background_color)
  for i in range(0, len(group1_files)):
    scatter(group1_files_features_norm[0][i], group1_files_features_norm[1][i], size_marker, group1_color)
    #text(music_files[i], music_files_features[0][i], music_files_features[1][i])
      
  for i in range(0, len(group2_files)):
    scatter(group2_files_features_norm[0][i], group2_files_features_norm[1][i], size_marker, group2_color)
  
  xlabel("mean spectral centroid")
  ylabel("std rms")
  legend(group1_legend, group1_color, 0, 10, getCanvasWidth()-80)
  legend(group2_legend, group2_color, 0, 25, getCanvasWidth()-80)
  canvas_pause()


def scatter(x_f1, y_f2, diameter, color):
  width = offset + (getCanvasWidth()*x_f1)
  drawCircle(width, getCanvasHeight()*y_f2, diameter, color)

def text(title, x_f1, y_f2):
    drawText(title, getCanvasWidth()*x_f1, getCanvasHeight()*y_f2, text_color)

def xlabel(title):
  drawText(title, getCanvasWidth()/2, getCanvasHeight()*0.9, text_color)

def ylabel(title):
  drawText(title, 1, getCanvasHeight()*0.5, text_color)

def legend(label, color, x, y, offsetX):
  drawText(label, offsetX+10, y, text_color)
  drawCircle(offsetX, y+7, size_marker, color)
    
finish()
