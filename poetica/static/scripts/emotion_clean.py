import pandas as pd
import numpy as np


def update_emotions_allrows(df):
    for index, row in df.iterrows():
        d = row.to_dict()
        del d['Id']
        del d['First Emotion']
        del d['Second Emotion']
        del d['Third Emotion']

        top_three = sorted(d, key=d.get, reverse=True)[:3]

        df.at[index, 'First Emotion'] = top_three[0]
        df.at[index, 'Second Emotion'] = top_three[1]
        df.at[index, 'Third Emotion'] = top_three[2]

    return df


def update_emotion_onerow(poem_id, df):

    row = df.loc[df.index == poem_id]
    index_tmp = df.index[df['Id'] == poem_id]
    index = df.at[index_tmp[0], 'Id']

    d = row.to_dict('records')[0]

    del d['Id']
    del d['First Emotion']
    del d['Second Emotion']
    del d['Third Emotion']

    top_three = sorted(d, key=d.get, reverse=True)[:3]

    df.at[index, 'First Emotion'] = top_three[0]
    df.at[index, 'Second Emotion'] = top_three[1]
    df.at[index, 'Third Emotion'] = top_three[2]

    return df


def add_to_emotion(emotion, poem_id, df):

    row = df.loc[df['Id'] == poem_id]
    index_tmp = df.index[df['Id'] == poem_id]
    index = df.at[index_tmp[0], 'Id']

    df.at[index, emotion] += 1

    df = update_emotion_onerow(poem_id, df)
    return df


df = pd.read_csv('emotions_db.csv')
df = update_emotions_allrows(df)
df.to_csv('emotions_db.csv', encoding='utf-8', index=False)

# df = add_to_emotion("sadness", 0, df)
#
# df.to_csv('emotions_updated.csv', encoding='utf-8', index=False)




