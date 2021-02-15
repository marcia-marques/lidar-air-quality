import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

"""
Script to plot gantt charts for data availability
Specific for CETESB stations (MP2.5, MP10 and wind speed)
"""


def gantt_data(path, usecols, var, pos):
    """
    Returns a dataframe with data availability info.

    Parameters:
        path (str): file name
        usecols (list-like): columns to be read
        var (str): selected variable
        pos (int): position in the graph (from bottom to top)
    """
    df = pd.read_csv(path, usecols=usecols)
    df = df.set_index('date')
    df.index = pd.to_datetime(df.index)
    df = df[(df.index >= '01/01/2019') & (df.index < '01/01/2020')]
    df['avail'] = df[var].isnull()  # look for null values
    df['avail'] = df['avail'].map({False: pos})  # populate with graph position
    return df


# MP2.5
df_mp25 = pd.DataFrame()
for i, file_name in enumerate(sorted(list(glob.glob('../data/*_mp25.csv')), reverse=True)):
    temp = gantt_data(file_name, ['date', 'name', 'val'], 'val', i)
    df_mp25 = pd.concat([df_mp25, temp])
names_mp25 = sorted([value for value in df_mp25.name.unique() if type(value) != float], reverse=True)

plt.rcParams["figure.dpi"] = 600
fig, ax = plt.subplots(figsize=(12, 4.5))
for name in names_mp25:
    plt.scatter(df_mp25[df_mp25.name == name].index, df_mp25[df_mp25.name == name].avail,
                s=30 ** 2, marker="|", color="darkblue")
ax.grid(which='major', axis='x', linestyle='--')
plt.yticks(range(len(names_mp25)), names_mp25)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.title('CETESB stations MP2.5 availability')
plt.tight_layout()
# plt.show()
plt.savefig('../plots/gantt-chart-mp25.png')

# MP10
df_mp10 = pd.DataFrame()
for i, file_name in enumerate(sorted(list(glob.glob('../data/*_mp10.csv')), reverse=True)):
    temp = gantt_data(file_name, ['date', 'name', 'val'], 'val', i)
    df_mp10 = pd.concat([df_mp10, temp])
names_mp10 = sorted([value for value in df_mp10.name.unique() if type(value) != float], reverse=True)

plt.rcParams["figure.dpi"] = 600
fig, ax = plt.subplots(figsize=(12, 4.5))
for name in names_mp10:
    plt.scatter(df_mp10[df_mp10.name == name].index, df_mp10[df_mp10.name == name].avail,
                s=30 ** 2, marker="|", color="darkblue")
ax.grid(which='major', axis='x', linestyle='--')
plt.yticks(range(len(names_mp10)), names_mp10)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.title('CETESB stations MP10 availability')
plt.tight_layout()
# plt.show()
plt.savefig('../plots/gantt-chart-mp10.png')

# Meteo
df_met = pd.DataFrame()
names_met = ['Santana', 'Pinheiros', 'Parque D. Pedro II', 'Moóca', 'Marg.Tietê-Pte Remédios']
for i, file_name in enumerate(sorted(list(glob.glob('../data/*_met.csv')), reverse=True)):
    temp = gantt_data(file_name, ['date', 'ws'], 'ws', i)
    temp['name'] = names_met[i]
    df_met = pd.concat([df_met, temp])

plt.rcParams["figure.dpi"] = 600
fig, ax = plt.subplots(figsize=(12, 4.5))
for name in names_met:
    plt.scatter(df_met[df_met.name == name].index, df_met[df_met.name == name].avail,
                s=30 ** 2, marker="|", color="darkblue")
ax.grid(which='major', axis='x', linestyle='--')
plt.yticks(range(len(names_met)), names_met)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.title('CETESB stations wind speed availability')
plt.tight_layout()
# plt.show()
plt.savefig('../plots/gantt-chart-met.png')
