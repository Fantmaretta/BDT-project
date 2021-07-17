import pandas as pd

d = {'localita': [], 'measure': [], 'accuracy': [], 'count': [], 'tot': [], 'fraction': []}

df = pd.DataFrame(data=d)

new_row = {'localita': 'ala', 'measure': 1, 'accuracy': 1, 'count': 1, 'tot': 1, 'fraction': 9}

df = df.append(new_row, ignore_index=True)

print(df)