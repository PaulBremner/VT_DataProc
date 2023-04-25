import pandas as pd
import glob

jsonfiles = glob.glob('FixedData/*.json')

print(jsonfiles[0])

df = pd.read_json(jsonfiles[0], lines=True)
pd.set_option('display.max_columns', None)
print(df.head())

dataDict = df.to_dict()
#each key in the dict contains a dict where the keys are the row numbers for each line of data (this essentially means it behaves like an array)
print(dataDict['name'])
#For each object it might be tagged multiple times. Measures of performance are accuracy of final tag state (compare tag colour to hazard distances, correct if <threshold distance), count tagging corrections, not sure how to get task speed other than total task time (time each tag occurs likely not useful).
#for each participant
    #for each object get the final tag state and compare this with the hazard levels.
    #count the number of times tag 0,0,0 (detagging) is used
#System performance - number of tags robot RTL active, number of tags self RTL active, total time each RTL active.
