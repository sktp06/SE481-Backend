import pandas as pd

def get_data(path):
    df = pd.read_json(path, orient='records')
    df.drop(columns=['approved', 'titles', 'title_english', 'title_japanese', 'title_synonyms'], inplace=True)
    df.set_index('mal_id', inplace=True)
    df['images'] = df['images'].apply(lambda x: x['jpg']['image_url'])
    df['trailer'] = df['trailer'].apply(lambda x: x['url'])
    df['producers'] = df['producers'].apply(lambda x: [i['name'] for i in x])
    df['licensors'] = df['licensors'].apply(lambda x: [i['name'] for i in x])
    df['studios'] = df['studios'].apply(lambda x: [i['name'] for i in x])
    df['genres'] = df['genres'].apply(lambda x: [i['name'] for i in x])
    df['themes'] = df['themes'].apply(lambda x: [i['name'] for i in x])
    df['demographics'] = df['demographics'].apply(lambda x: [i['name'] for i in x])
    return df

df = get_data("assets/anime.json")