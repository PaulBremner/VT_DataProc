import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

columns = list(range(17,69))#ignore the free entry Q for stats
df = pd.read_csv("SonificationForMRT.csv", usecols=columns, skiprows=[1,2])
#print(df.head(10))
#print(df.dtypes)
df.reset_index(inplace=True)

df['condition'] = np.where(df.Q1.str.contains('SB1'), 'SB1', 'SB2')#create a new column that contains the sound condition

print(df.head(10))

age = df['Q3'].describe()
print(age)
print(df['Q2'].value_counts())


#col numbers as in excel - 1 indexed

TinA = []  #21, 39
for i in range(1,20):
    TinA.append("TinA" + str(i))

NTLX = []#40. 45
for i in range(1,7):
    NTLX.append("NTLX" + str(i))

NTLXW = [] #46, 51
for i in range(1,7):
    NTLXW.append("NTLXW" + str(i))

IPQ = [] #52, 60
for i in range(1,10):
    IPQ.append("IPQ" + str(i))

SoundEval = [] #61, 69
for i in range(1,10):
    SoundEval.append("SoundEval" + str(i))

cols = ['index'] + TinA + NTLX + NTLXW + IPQ + SoundEval + ['condition']

df_final = df.drop(columns = ['Q1', 'Q2', 'Q3'])

df_final.columns = cols
print(df_final.head(10))
#exit()

df_questions = pd.DataFrame(columns=cols)

df_final['IPQ3'] = 6 - df_final['IPQ3']
df_final['IPQ6'] = 6 - df_final['IPQ6']
df_final['NTLX4'] = 10 - df_final['NTLX4']

for i in [10, 15, 7, 16, 5]:
    df_final['TinA' + str(i)] = 6 - df_final['TinA' + str(i)]

for c in NTLXW:
    df_final[c] = 6 - df_final[c]

df_final['RC'] =df_final[['TinA10', 'TinA1', 'TinA6', 'TinA13', 'TinA15', 'TinA19']].mean(axis=1)#reliability/competance
df_final['UP'] =df_final[['TinA2', 'TinA7', 'TinA11', 'TinA16']].mean(axis=1)#understanding predictability
df_final['F'] =df_final[['TinA3', 'TinA17']].mean(axis=1)#familiarity
df_final['IofD'] =df_final[['TinA4', 'TinA8']].mean(axis=1)#intent of devs
df_final['PtoT'] =df_final[['TinA5', 'TinA12', 'TinA18']].mean(axis=1)#Propensity to trust
df_final['T'] =df_final[['TinA9', 'TinA14']].mean(axis=1)#Trust in system

for c in NTLX:
    df_final[c] = df_final[c] * df_final[c[:4] + 'W' + c[4:]]

df_final['NTLX'] = df_final[NTLX].mean(axis=1)

#pd.set_option('display.max_columns', None)
print(df_final.head(10))

proc_cols = SoundEval + ['RC', 'UP', 'F', 'IofD', 'PtoT', 'T', 'NTLX']

for c in proc_cols:
    stat, p = stats.shapiro(df_final[df.condition == 'SB1'][c])
    #print(c + " p = " + str(p))
    stat, p = stats.shapiro(df_final[df.condition == 'SB2'][c])
    #print(c + " p = " + str(p))
    #stat, p = stats.shapiro(np.log(df_final[c]))
    #print("log " + c + " p = " + str(p))

# stress and presence data not normal so use non-parametric tests
df_final[''] = ""

for c in proc_cols:
    print(c)
    b = df_final.query('condition == "SB1"')[c]
    a = df_final.query('condition == "SB2"')[c]
    a = a.dropna()
    b = b.dropna()

    #print(a)
    print(b.describe())
    print(a.describe())
    sns.violinplot(x = '', hue='condition', y=c, data=df_final)#, split=True)#, inner="points")
    plt.show()

    if c != 'NTLX':
        print(stats.mannwhitneyu(a, b))
    else:
        print(stats.ttest_ind(a, b))
exit()

# plt.hist(df_final['P'])
# plt.show()
#
# plt.hist(df_final['SP'])
# plt.show()
#
# plt.hist(df_final['INV'])
# plt.show()
#
# plt.hist(df_final['EXP'])#
# plt.show()
#
# plt.hist(df_final['SUS'])#
# plt.show()
#
# plt.hist(df_final['NTLX'])
# plt.show()

#TODO add cols for the processed data for each questionnaire
# IPQ
# Reverse coding:
# 23_3
# 23_6
# 1 - pres
# 2,3,4 - Spatial presence
# 5,6 - Involvement
# 7,8 - Experienced Realism
#
# NTLX
# 4 is reverse scored
# Mean of all ratings*weight for that rating (0-5) = workload score. Low score means low workload
#
# SUS
# Reverse coded:
# 2,4,5, 8, 10
# After reverse coding sum all answers - 10 and *2.5. >68 is good
#
# For stress do each item individually