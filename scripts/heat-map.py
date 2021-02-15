import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# MP2.5
df_mp25 = pd.DataFrame()
for i, file_name in enumerate(sorted(list(glob.glob('../data/*_mp25.csv')), reverse=True)):
    temp = pd.read_csv(file_name, usecols=['date', 'name', 'val'])
    temp = temp.set_index('date')
    temp.index = pd.to_datetime(temp.index)
    temp = temp[(temp.index >= '01/01/2019') & (temp.index < '01/01/2020')]
    df_mp25 = pd.concat([df_mp25, temp])

plt.rcParams['figure.figsize'] = [12, 3]
ax = sns.heatmap(df_mp25.pivot_table(index='name', columns=df_mp25.index.dayofyear, values='val'),
                 cmap='coolwarm')
plt.xlabel('Timestamp')
plt.ylabel(None)
ax.collections[0].colorbar.set_label('PM 2.5 ug/m³')
plt.tight_layout()
# plt.show()
plt.savefig('../plots/heat-map-mp25.png')

# MP10
df_mp10 = pd.DataFrame()
for i, file_name in enumerate(sorted(list(glob.glob('../data/*_mp10.csv')), reverse=True)):
    temp = pd.read_csv(file_name, usecols=['date', 'name', 'val'])
    temp = temp.set_index('date')
    temp.index = pd.to_datetime(temp.index)
    temp = temp[(temp.index >= '01/01/2019') & (temp.index < '01/01/2020')]
    df_mp10 = pd.concat([df_mp10, temp])

plt.clf()
plt.rcParams['figure.figsize'] = [12, 3]
ax = sns.heatmap(df_mp10.pivot_table(index='name', columns=df_mp10.index.dayofyear, values='val'),
                 cmap='coolwarm')
plt.xlabel('Timestamp')
plt.ylabel(None)
ax.collections[0].colorbar.set_label('PM 10 ug/m³')
plt.tight_layout()
# plt.show()
plt.savefig('../plots/heat-map-mp10.png')


