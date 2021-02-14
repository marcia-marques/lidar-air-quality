from qualar import qualar as ql
from login import user, password

"""
Script to download data from CETESB stations
https://qualar.cetesb.sp.gov.br/qualar/home.do
qualar package was developed by @quishqa
"""

start_date = '31/12/2018'
end_date = '01/01/2020'
# variable = 57  # MP2.5
# variable = 12  # MP 10
stations = [95, 72, 99, 91, 85, 270, 96, 63, 103, 83, 73, 64]
file_names = ['../data/ciduni', '../data/parquedpedro', '../data/pinheiros',
              '../data/cerqcesar', '../data/mooca', '../data/margtiete',
              '../data/nsenhora', '../data/santana', '../data/taboao',
              '../data/ibirapuera', '../data/congonhas', '../data/santoamaro']

# MP2.5
for station, file_name in zip(stations, file_names):
    ql.cetesb_data_download(user, password,
                            start_date, end_date,
                            57, station,
                            file_name+'_mp25', csv=True)

# MP10
for station, file_name in zip(stations, file_names):
    ql.cetesb_data_download(user, password,
                            start_date, end_date,
                            12, station,
                            file_name+'_mp10', csv=True)

# Meteo
for station, file_name in zip(stations, file_names):
    ql.all_met(user, password,
               start_date, end_date,
               station,
               file_name=file_name+'_met', csv_met=True)
