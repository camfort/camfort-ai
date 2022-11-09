import sqlite3
from openai.embeddings_utils import cosine_similarity
from openai.embeddings_utils import get_embedding
from openai import api_key
import pandas as pd
import argparse

defaultdbfile = 'vectors.db'
tabname = 'embeddings'

def main():
    global api_key
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', '-D', type=str, default=defaultdbfile, help='SQLite3 database filename for storing vectors')
    parser.add_argument('--api-key', type=str, default=None, help='OpenAI API key (or use env var OPENAI_API_KEY)')
    parser.add_argument('input', type=str, help='Search terms')

    args = parser.parse_args()
    if args.api_key is not None:
        api_key = args.api_key

    con = sqlite3.connect(args.database)

    query = "SELECT path, name AS fname, firstLine, lastLine, vectorid, elem AS emb FROM embeddings JOIN vectors ON embeddings.vectorid = vectors.id ORDER BY vectorid, ord"
    df = pd.read_sql_query(query, con).groupby('vectorid').agg({'emb': list, 'path': 'first', 'fname': 'first', 'firstLine': 'first', 'lastLine': 'first'}).reset_index()

    search_functions(df, args.input)

def search_functions(df, code_query, n=3, pprint=True, n_lines=7):
    embedding = get_embedding(code_query, engine='code-search-babbage-text-001')
    df['similarities'] = df.emb.apply(lambda x: cosine_similarity(x, embedding))

    res = df.sort_values('similarities', ascending=False).head(n)
    if pprint:
        for r in res.iterrows():
            print(f'{r[1].path}:{r[1].firstLine}: function or subroutine {r[1].fname}: score={str(round(r[1].similarities, 3))}')
            print('-'*70)
    return res


if __name__=="__main__":
  main()
