from qualar import qualar as ql
from login import user, password

"""
Script to download data from CETESB stations
https://qualar.cetesb.sp.gov.br/qualar/home.do
qualar package was developed by @quishqa
"""

start_date = '01/03/2019'
end_date = '30/09/2019'
variable = 57  # MP2.5
stations = [95, 72, 99]
file_names = ['data/usp', 'data/sefaz', 'data/pinheiros']
file_names_met = ['data/sefaz_met', 'data/pinheiros_met']

for station, file_name in zip(stations, file_names):
    ql.cetesb_data_download(user, password,
                            start_date, end_date,
                            variable, station,
                            file_name, csv=True)

for station, file_name in zip(stations[1:], file_names_met):
    ql.all_met(user, password,
               start_date, end_date,
               station,
               file_name=file_name, csv_met=True)
