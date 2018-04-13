import csv as csv
import numpy as np
import pandas as pd


raw_data_sheet = csv.reader(open('../data/masterfantasydata.csv','rb'))
header = raw_data_sheet.next()
data = []


########## Get Canadian players variables #####################
for row in raw_data_sheet:
    data.append(row)
data = np.array(data)

names = data[0::,0]
positionX = data[0::,1]
positionY = data[0::,2]
games = np.array(data[0::,3].astype(np.float))

# All used variables normaized to # of games
goals = np.array(data[0::,4].astype(np.float))/games
assists = np.array(data[0::,5].astype(np.float))/games
penaltyMinutes = np.array(data[0::,6].astype(np.float))/games
PPpoints = np.array(data[0::,7].astype(np.float))/games
faceoffWins =  np.array(data[0::,10].astype(np.float))/games
hits =  np.array(data[0::,8].astype(np.float))/games
blocks =  np.array(data[0::,9].astype(np.float))/games
salary = np.array(data[0::,11].astype(np.float))

########## Get all players variables #####################
all_NHL_data = csv.reader(open('../data/allNHL.csv','rb'))
header2 = all_NHL_data.next()
NHLdata = []

for row in all_NHL_data:
    NHLdata.append(row)
NHLdata = np.array(NHLdata)

nhlgames = np.mean(NHLdata[0::,5].astype(np.float))

# All used variables normaized to # of games
mean_goals = np.mean(NHLdata[0::,6].astype(np.float))/nhlgames
mean_assists = np.mean(NHLdata[0::,7].astype(np.float))/nhlgames
mean_penaltyMinutes = np.mean(NHLdata[0::,10].astype(np.float))/nhlgames
mean_PPpoints = np.mean(NHLdata[0::,12].astype(np.float))/nhlgames
mean_faceoffWins = np.mean(NHLdata[0::,24].astype(np.float))/nhlgames
mean_hits =  np.mean(NHLdata[0::,23].astype(np.float))/nhlgames
mean_blocks =  np.mean(NHLdata[0::,22].astype(np.float))/nhlgames

########### Calculate percent from mean ##################
pGoals = (goals - mean_goals)/mean_goals
pAssists = (assists - mean_assists)/mean_assists
pMinutes = (penaltyMinutes - mean_penaltyMinutes)/mean_penaltyMinutes
pPPpoints = (PPpoints - mean_PPpoints)/mean_PPpoints
pFaceoffWins = (faceoffWins - mean_faceoffWins)/mean_faceoffWins
pHits = (hits - mean_hits)/mean_hits
pBlocks = (blocks - mean_blocks)/mean_blocks

sum_percent = pGoals + pAssists + pMinutes + pPPpoints + pHits + pBlocks + pFaceoffWins

########### Create Dataframe and write CSV #################
d = {'name':names,'positionX':positionX,'positionY':positionY,'pGoals':pGoals,'pAssists':pAssists,'pPenaltyMin':pMinutes,'pPPpoints':pPPpoints,'pFaceoffWins':pFaceoffWins,"pHits":pHits,"pBlocks":pBlocks,'games':games}
df = pd.DataFrame( data=d )
dfCut =  df[df.games > 15]
df.to_csv("../data/stats_in_percent.csv")
dfCut.to_csv("../data/cut_stats_in_percent.csv")

########### Create Dataframe to be fed to Optimization ######

d2 = {'name':names,'position':positionX,'positionB':positionY,'salary':salary,'sum_percent':sum_percent,'games':games}
df2 = pd.DataFrame( data=d2 )
df2 = df2[df2.games > 15]
df2.drop('games',axis=1)
df2.to_csv("to_knapsackPosY.csv",index=false)
                      
