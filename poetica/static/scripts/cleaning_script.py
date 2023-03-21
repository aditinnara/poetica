import pandas as pd

df = pd.read_csv('PoetryFoundationData.csv')
delete_ID = []


df = df.drop('Tags', axis=1)
df = df.drop('Unnamed: 0', axis=1)

df = df.dropna()

currentPoet = ''
numPoems = 0
poetList = []

for index, row in df.iterrows():
    if (row['Poet'] == currentPoet) and (numPoems < 1):
        numPoems += 1
    elif ((row['Poet'] == currentPoet) and (numPoems >= 1)) or (row['Poet'] in poetList):
        df.drop(index, axis=0, inplace=True)
    elif row['Poet'] != currentPoet:
        poetList.append(currentPoet)
        currentPoet = row['Poet']
        numPoems = 0

df.to_csv('cleaned_poetry.csv', encoding='utf-8')





