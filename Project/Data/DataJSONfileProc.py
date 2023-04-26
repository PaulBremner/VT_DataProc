import pandas as pd
import glob

jsonfiles = glob.glob('FixedData/*.json')

#print(jsonfiles[0])
cols = ['condition', 'tagsNoRTL', 'tagsSelfRTL', 'tagsRobotRTL', 'clearedTags', 'totalTime']
taggingdf = pd.DataFrame(columns = cols)

for jsonfile in jsonfiles:
#jsonfile = jsonfiles[0]
    df = pd.read_json(jsonfile, lines=True)
    pd.set_option('display.max_columns', None)
    #print(df.head())

    #df_hazard = pd.read_json('ObstacleData\obstacle_hazard_data.json')

    #print(df_hazard.head())
    #hazardDict = df_hazard.to_dict()

    dataDict = df.to_dict()
    #create a df with cols = ['condition', 'tagsNoRTL', 'tagsSelfRTL', 'tagsRobotRTL']
    participantData = {}
    participantData['condition'] = jsonfile[10:13]
    participantData['tagsNoRTL'] = 0
    participantData['tagsSelfRTL'] = 0
    participantData['tagsRobotRTL'] = 0
    participantData['clearedTags'] = 0
    #print(dataDict['rtlObject'])
    for rtl in dataDict['rtlObject'].values():
        if 'none' in rtl:
            participantData['tagsNoRTL'] += 1
        elif 'self' in rtl:
            participantData['tagsSelfRTL'] += 1
        elif 'Robot' in rtl:
            participantData['tagsRobotRTL'] += 1
    #print(dataDict['name'].values())

    for tag in dataDict['tag'].values():
        if tag == [0.0,0.0,0.0]:
            participantData['clearedTags'] += 1

    participantData['totalTime'] = dataDict['timestamp'][len(dataDict['timestamp'])-1]

    taggingdf.loc[len(taggingdf)] = participantData

#print(taggingdf.head())


jsonfiles = glob.glob('FixedTimeData/*.json')
#jsonfile = jsonfiles[0]

#print(jsonfile)
cols = ['condition', 'timeSelfRTL', 'timeRobotRTL']
timingdf = pd.DataFrame(columns = cols)

for jsonfile in jsonfiles:
#jsonfile = jsonfiles[0]
    df = pd.read_json(jsonfile, lines=True)
    timingDict = df.to_dict()
    participantData = {}
    participantData['condition'] = jsonfile[14:17]
    participantData['timeSelfRTL'] = timingDict['selfRTLTime'][len(timingDict['selfRTLTime'])-2]
    participantData['timeRobotRTL'] = timingDict['robotRTLTime'][len(timingDict['robotRTLTime'])-2]
    timingdf.loc[len(timingdf)] = participantData

print(timingdf.head())

#step through each thing they have tagged and log the tags to a dict with the object name as key, that way the final object tag state is stored
#then go through that dict and check in hazard list dict for what the tag should be, if it is non-hazardous or doesn't match log the error

#print("tags = " + str(len(dataDict['name'])) + " obstacles = " + str(len(hazardDict)))

#hazardCounter = 0
#for obstacle in hazardDict.keys():
#    if obstacle not in dataDict['name'].values():
        #check if the object should be tagged by checking the hazard levels against a hazard threshold
#        hazardCounter += 1
    #else:
    #    print("tagged = " + obstacle)


#print("missing obstacles " + str(hazardCounter))
#each key in the dict contains a dict where the keys are the row numbers for each line of data (this essentially means it behaves like an array)
#print(dataDict['name'])
#For each object it might be tagged multiple times. Measures of performance are accuracy of final tag state (compare tag colour to hazard distances, correct if <threshold distance), count tagging corrections, not sure how to get task speed other than total task time (time each tag occurs likely not useful).
#for each participant
    #for each object get the final tag state and compare this with the hazard levels.
    #count the number of times tag 0,0,0 (detagging) is used
#System performance - number of tags robot RTL active, number of tags self RTL active, total time each RTL active.
