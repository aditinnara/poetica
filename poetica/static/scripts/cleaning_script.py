import pandas as pd
import os


def clean_poetry_db():
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

    df.to_csv('poetry_db.csv', encoding='utf-8')


def get_poem_id(title, poet):
    if title == "":
        return -1
    if poet == "":
        return -1

    file_dir = os.path.dirname(__file__)
    csv_path = os.path.join(file_dir, "..", "database", "working_poetry_db.csv")
    df = pd.read_csv(csv_path)

    id = df.loc[(df['Title'] == title) & (df['Poet'] == poet)]['Id']
    print(id)




