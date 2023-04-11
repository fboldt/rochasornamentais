import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json('data/processeddata.json')
fig, ax = plt.subplots()
df['year'].value_counts().plot(ax=ax, kind='bar')

plt.suptitle('frequency for year')
plt.ylabel('frequency')

plt.tight_layout()
plt.savefig("./plot/frequencia_anos.png", format="PNG")
