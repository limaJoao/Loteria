from pickle import FALSE
import requests
import pandas as pd

url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados?modalidade=Lotof%C3%A1cil"

r = requests.get(url, verify=False)

requests.get()

r_text = r.text

# Facilitar a leitura pelo pd.read_html
r_text = r_text.replace('\\r\\n', '')
r_text = r_text.replace('"\r\n}', '')
r_text = r_text.replace('{\r\n "html": "', '')
r_text

df = pd.read_html(r_text)

type(df)
type(df[0])

df = df[0].copy()

# Limpar as linhas com objetos nulos. um objeto nulo não é igual nada nem ele mesmo
df = df[df['Bola1'] == df['Bola1']]

# Análise

nr_pop = list(range(1,26))

nr_pares = list(filter(lambda x: (x % 2 == 0), nr_pop))
nr_impares = list(filter(lambda x: (x % 2 != 0), nr_pop))
nr_primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]

comb = []
vars = {}

for i in nr_pop:
    vars[f'v_{i}'] = 0

lst_campos = df.columns[2:17]

# Cálculos

df_results = df[lst_campos].apply(pd.Series.value_counts, axis=1).fillna(0)

df_comb = pd.DataFrame({'pares': df_results[nr_pares].sum(axis=1),
                        'impares': df_results[nr_impares].sum(axis=1),
                        'primos': df_results[nr_primos].sum(axis=1)})

# Fazendo as somas

df_results = pd.DataFrame({'numero': nr_pop, 'freq': df_results.sum(axis=0)}).reset_index(drop=True)
df_comb = df_comb.groupby(df_comb.columns.tolist(),as_index=False).size()

# ordenando

df_results.sort_values(by=['freq'], ascending=False)
df_comb = df_comb.sort_values(by=['size'], ascending=False)