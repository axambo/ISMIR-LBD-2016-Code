#   python code
#   script_name: Music/speech classifier
#
#   author: Anna Xambó
#   description: Music/speech classifier by threshold. Press Run, click on the Processing icon, and then press play.
#

from earsketch import *
from random import *

init()
setTempo(120)

# Visualization setup
group1_legend = "electric bass"
group2_legend = "electric guitar"
group1_color = "#000000"
group2_color = "#999999"
text_color = "#000000"
background_color = "#FFFFFF"

# Dataset
group1_files = [RD_EDM_WARMBASSLINE_1, RD_EDM_WOBBLEBASS_1, RD_ROCK_POPELECTRICBASS_1,RD_ROCK_POPELECTRICBASS_2, RD_ROCK_POPELECTRICBASS_3, RD_ROCK_POPELECTRICBASS_4, RD_ROCK_POPELECTRICBASS_5, RD_ROCK_POPELECTRICBASS_6, RD_ROCK_POPELECTRICBASS_7, RD_ROCK_POPELECTRICBASS_8, RD_ROCK_POPELECTRICBASS_9, RD_ROCK_POPELECTRICBASS_10, RD_ROCK_POPELECTRICBASS_11, RD_ROCK_POPELECTRICBASS_12, RD_ROCK_POPELECTRICBASS_13, RD_ROCK_POPELECTRICBASS_14, RD_ROCK_POPELECTRICBASS_15, RD_ROCK_POPELECTRICBASS_16, RD_ROCK_POPELECTRICBASS_17, RD_ROCK_POPELECTRICBASS_18, RD_ROCK_POPELECTRICBASS_19, RD_ROCK_POPELECTRICBASS_20, RD_ROCK_POPELECTRICBASS_21, RD_ROCK_POPELECTRICBASS_22, RD_ROCK_POPELECTRICBASS_23, RD_ROCK_POPELECTRICBASS_24, RD_ROCK_POPELECTRICBASS_25]

group2_files = [RD_ROCK_POPELECTRICLEAD_1, RD_ROCK_POPELECTRICLEAD_2, RD_ROCK_POPELECTRICLEAD_3, RD_ROCK_POPELECTRICLEAD_4, RD_ROCK_POPELECTRICLEAD_5, RD_ROCK_POPELECTRICLEAD_6, RD_ROCK_POPELECTRICLEAD_7, RD_ROCK_POPELECTRICLEAD_8, RD_ROCK_POPELECTRICLEAD_9, RD_ROCK_POPELECTRICLEAD_10, RD_ROCK_POPELECTRICLEAD_11, RD_ROCK_POPELECTRICLEAD_12, RD_ROCK_POPELECTRICLEAD_13, RD_ROCK_POPELECTRICLEAD_14, RD_ROCK_POPLEADSTRUM_GUITAR_1, RD_ROCK_POPLEADSTRUM_GUITAR_2, RD_ROCK_POPLEADSTRUM_GUITAR_3, RD_ROCK_POPLEADSTRUM_GUITAR_4, RD_ROCK_POPLEADSTRUM_GUITAR_5, RD_ROCK_POPLEADSTRUM_GUITAR_6,  RD_ROCK_POPLEADSTRUM_GUITAR_7, RD_ROCK_POPLEADSTRUM_GUITAR_8, RD_ROCK_POPLEADSTRUM_GUITAR_9, RD_ROCK_POPLEADSTRUM_GUITAR_10, RD_ROCK_POPRHYTHM_GUITAR_1, RD_ROCK_POPRHYTHM_GUITAR_2, RD_ROCK_POPRHYTHM_GUITAR_3, RD_ROCK_POPRHYTHM_GUITAR_4, RD_ROCK_POPRHYTHM_GUITAR_5, RD_ROCK_POPRHYTHM_GUITAR_6, RD_ROCK_POPRHYTHM_GUITAR_7, RD_ROCK_POPRHYTHM_GUITAR_8, RD_ROCK_POPRHYTHM_GUITAR_9, RD_ROCK_POPRHYTHM_GUITAR_10, RD_ROCK_POPRHYTHM_GUITAR_11, RD_ROCK_POPRHYTHM_GUITAR_12, RD_ROCK_POPRHYTHM_GUITAR_13, RD_ROCK_POPRHYTHM_GUITAR_14, RD_ROCK_POPRHYTHM_GUITAR_15]

# Analysis setup
subgroup1_files = []
subgroup2_files = []
subgroup1_by_feature = []
subgroup2_by_feature = []
playlist = [[] for x in xrange(2)] # playlist[0] = song name, playlist[1] = original group 1 or 2
playlist_by_feature = []
playlist_by_feature_norm = []
classifier_list = []
num_song_files = 10
analysis_method = SPECTRAL_CENTROID
threshold_mode = [0.8, 0] #threshold_mode[0] = value; #threshold_mode[1] = 0: TODO manual, 1: automatic above threshold is category1, 2: automatic above threshold is category2; # If threshold_mode[0] is set to 0.0, threshold will be computed automatically; else it will use the manual value.
threshold_norm = [0.0, 0]
hop = 0.0625 # analyze in 1/16th note chunks 
start = 1
end = 11.0 # num measures = num_song_files + 1
feature_vector_time = []
feature_vector_time_norm = []

# This function creates a list of sounds from a group of sounds with size 'numfiles' 
def randomGroup (dataset, group, numfiles):
  for i in range (0, numfiles):
    index = randint(0, len(dataset)-1)
    file = dataset[index] 
    group.append(file)

# This function creates a list of mixed sounds from two groups of sounds with size 'numfiles'
def randomMix (group1, group2, newgroup, numfiles):
  for i in range (0, numfiles):
    group = randint(1,2)
    index = randint(0, len(group1)-1)
    if(group==1):
      newgroup[0].append(group1[index])
      newgroup[1].append(group1_legend)
    else:
      newgroup[0].append(group2[index]) 
      newgroup[1].append(group2_legend)

# This function sequentially places files on a track from a group of sounds, it analyzes the track by a selected feature, and normalizes and stores the values for visualization purposes
def randomFitMedia (track, group):
  for i in range (1, len(group)+1):
    index = i-1
    fitMedia(group[index], 1, i, i+1)
  # Analyzed feature_vector_time
  analyzeTrackFeature()
  # Normalize feature_vector_time for visualization purposes
  normalizeFeaturesVector(feature_vector_time, feature_vector_time_norm)

# This function analyzes and stores the value of an analysis feature for a given group of sounds 
def computeFeatureVector (group, featurevector, feature):  
  for i in range(0, len(group)):
      feature1 = analyze(group[i], feature)
      featurevector.append(float(feature1))

# This function calculates an automatic threshold from two given groups of sounds or leaves the manual value.
def computeThreshold (group1, group2, featurevector1, featurevector2, feature): 
  # Compute the feature vector of each group
  computeFeatureVector (group1, featurevector1, feature)
  computeFeatureVector (group2, featurevector2, feature)
  # Decide threshold and mode
  
  if ( threshold_mode[0] > 0.0 ):
    threshold_mode[1] = 0
  else:  
    averagefv1 = sum(featurevector1) / float(len(featurevector1))
    averagefv2 = sum(featurevector2) / float(len(featurevector2))
    if ( averagefv1 < averagefv2 ): #anything above this threshold belongs to category2
      threshold_mode[0] = (min(featurevector2) - max(featurevector1)) / 2
      threshold_mode[1] = 2
    else: #anything above this threshold belongs to category1
      threshold_mode[0] = (min(featurevector1) - max(featurevector2)) / 2
      threshold_mode[1] = 1

# This function calculates and stores the category of a list of sounds
def computeCategory (thresholdmode, featurelist, classifierlist, category1, category2):
  if (thresholdmode[1] == 0): 
    for i in range(0, len(featurelist)):
      if (featurelist[i] < thresholdmode[0]): classifierlist.append(category1)
      else: classifierlist.append(category2) 
  elif (thresholdmode[1] == 2):
      for i in range(0, len(featurelist)):
        if (featurelist[i] < thresholdmode[0]): classifierlist.append(category1)
        else: classifierlist.append(category2)
  elif (thresholdmode[1] == 1):
    for i in range(0, len(featurelist)):
      if (featurelist[i] < thresholdmode[0]): classifierlist.append(category2) 
      else: classifierlist.append(category1) 


# This function analyzes a track using a selected analysis method and window size
def analyzeTrackFeature():
  position = 1
  while (position < end):
    feature1 = analyzeTrackForTime(1, analysis_method, position, position + hop)  # analyze tracks at current time
    feature_vector_time.append(feature1)
    position = position + hop

# This function normalizes a value given a range
def normalize(value, minval, maxval):
  rangeMinMax = maxval - minval
  #print ("rangeMinMax") 
  #print (rangeMinMax)
  #print("value")
  #print(value)
  #print("normalized value")
  #print ((value - minval) / rangeMinMax)
  return (value - minval) / rangeMinMax

# This function goes value by value of featuresVector and computes a normalized value in normFeaturesVector for visualization purposes
def normalizeFeaturesVector(featuresVector, normFeaturesVector):
  for i in range( 0, len(featuresVector) ):
    result = normalize( featuresVector[i], min(featuresVector), max(featuresVector) )
    normFeaturesVector.append( float(result) )  

def computeAccuracy(vector1, vector2):
  counter = 0
  #print("User classification: " + str(vector1))
  #print("Real classification: " + str(vector2))  
  for i in range( 0, len(vector1) ):
    if (str(vector1[i]) == str(vector2[i])):
      counter = counter + 1
    else:
      counter = counter + 0
  result = float(counter) / len(vector1)
  return result

  #my_dict1 = {i:vector1.count(i) for i in vector1}  
  #my_dict2 = {i:vector2.count(i) for i in vector2}
  #print len(vector1)
  #print my_dict1
  #print my_dict1[group1_legend]
    
# Random selection of files from dataset to a mixed subset
randomGroup (group1_files, subgroup1_files, 10)
randomGroup (group2_files, subgroup2_files, 10)
randomMix (subgroup1_files, subgroup2_files, playlist, num_song_files)

# Placement of selected files in the DAW
randomFitMedia (1, playlist[0])

# Compute threshold and mode
computeThreshold (subgroup1_files, subgroup2_files, subgroup1_by_feature, subgroup2_by_feature, analysis_method)

# Compute the feature vector of playlist
computeFeatureVector (playlist[0], playlist_by_feature, analysis_method)

if (threshold_mode[1] == 0):
  threshold_norm[0] = threshold_mode[0]
else:  
  threshold_norm[0] = normalize (threshold_mode[0], min(feature_vector_time), max(feature_vector_time))
#threshold_norm[0] = normalize (threshold_mode[0], 0, 1)

if (threshold_mode[1] == 0):
  normalizeFeaturesVector(playlist_by_feature, playlist_by_feature_norm)
  computeCategory (threshold_norm, playlist_by_feature_norm, classifier_list, group1_legend, group2_legend)
else: 
  computeCategory (threshold_norm, playlist_by_feature, classifier_list, group1_legend, group2_legend)

result_accuracy = computeAccuracy(classifier_list, playlist[1])

def printValues():
  print("threshold value: " + str(threshold_mode[0]))
  print("threshold norm: "+ str(threshold_norm[0]))
  print("mode: " + str(threshold_mode[1]))
  print("min value: " + str(min(feature_vector_time)))
  print("max value: " + str(max(feature_vector_time)))
  print("Computed threshold value: " + str(threshold_mode[0]))
  print("mode [if mode = 2, category2 is above threshold, if mode = 1, category1 is above threshold]: " + str(threshold_mode[1]))
  print("feature vector: " + str(playlist_by_feature))
  print("feature vector norm: " + str(playlist_by_feature_norm))
  print("user classification: " + str(classifier_list))
  print("real classification: " + str(playlist[1]))
  print("result accuracy: " + str(result_accuracy))
  #print("Feature vector time analysis: " + str(feature_vector_time))
  #print("Feature vector time norm analysis: " + str(feature_vector_time_norm))

printValues()


# Plot
def onLoop():
  drawRectangle (0, 0, getCanvasWidth(), getCanvasHeight(), "#FFFFFF")
  threshold_canvas = getCanvasHeight()-(threshold_norm[0]*getCanvasHeight())
  drawLine(0, threshold_canvas, getCanvasWidth(), threshold_canvas, "#FF0000")
  num_blocks = len(feature_vector_time)
  bar_width = getCanvasWidth()/num_blocks
  measure_width = bar_width*(num_blocks/num_song_files)

  for i in range(0, num_blocks):
    drawLine(i*bar_width, getCanvasHeight()-(getCanvasHeight()*feature_vector_time_norm[i]), (i*bar_width)+bar_width, getCanvasHeight()-(getCanvasHeight()*feature_vector_time_norm[i]), "#000000")
  
  for i in range(0, 16):
    drawLine(i*measure_width, 0, i*measure_width, getCanvasHeight(), "#CCCCCC")
    drawLine(i*measure_width, getCanvasHeight()-(getCanvasHeight()*playlist_by_feature_norm[i]), (i*measure_width)+measure_width, getCanvasHeight()-(getCanvasHeight()*playlist_by_feature_norm[i]), "#000000")
  
def onMeasure():
  c_measure = getCurrentMeasure()
  #print(playlist_by_feature[c_measure])
  #print( "measure: " + str(c_measure))
  print( "instrument classified as: " + classifier_list[c_measure] + ", instrument belongs to: " + playlist[1][c_measure])

finish()