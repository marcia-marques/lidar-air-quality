import requests
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup


def my_to_datetime(date_str):
    """
    Transform dates with with 01 - 24 hours to 00 - 23 hours.
    It is based on this question on Stack Over Flow:
        https://stackoverflow.com/questions/43359479/pandas-parsing-2400-instead-of-0000
    Parameters
    ----------
    date_str : str
        string with date.
    Returns
    -------
    Timestamp
        date as Timestamp.
    """
    if date_str[11:13] != '24':
        return pd.to_datetime(date_str, format='%d/%m/%Y_%H:%M')
    date_str = date_str[0:11] + '00' + date_str[13:]
    return pd.to_datetime(date_str, format='%d/%m/%Y_%H:%M') + dt.timedelta(days=1)


def cetesb_data_download(cetesb_login, cetesb_password,
                         start_date, end_date,
                         parameter, station, file_name=None, csv=False):
    """
    Download a parameter for one Air Quality Station station
    from CETESB AQS network
    Parameters
    ----------
    cetesb_login : str
        cetesb qualar username.
    cetesb_password : str
        cetesb qualar username's password.
    start_date : str
        date to start download in %dd/%mm/%YYYY.
    end_date : str
        date to end download in %dd/%mm/%YYYY.
    parameter : int
        parameter code.
    station : int
        AQS code.
    file_name : str, optional
        Name of csv file.
    csv : Bool, optional
        Export to csv file. The default is False.
    Returns
    -------
    dat_complete : pandas DataFrame
        DataFrame with a column with date and parameter values.
    """

    login_data = {
        'cetesb_login': cetesb_login,
        'cetesb_password': cetesb_password
    }

    search_data = {
        'irede': 'A',
        'dataInicialStr': start_date,
        'dataFinalStr': end_date,
        'iTipoDado': 'P',
        'estacaoVO.nestcaMonto': station,
        'parametroVO.nparmt': parameter
    }

    with requests.Session() as s:
        url = "https://qualar.cetesb.sp.gov.br/qualar/autenticador"
        r = s.post(url, data=login_data)
        url2 = "https://qualar.cetesb.sp.gov.br/qualar/exportaDados.do?method=pesquisar"
        r = s.post(url2, data=search_data)
        soup = BeautifulSoup(r.content, 'lxml')

    data = []
    table = soup.find('table', attrs={'id': 'tbl'})
    rows = table.find_all('tr')
    row_data = rows[2:]
    for row in row_data:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    dat = pd.DataFrame(data)

    # Creating a complete df with all dates
    day1 = pd.to_datetime(start_date, format='%d/%m/%Y')
    day2 = pd.to_datetime(end_date, format='%d/%m/%Y') + dt.timedelta(days=1)
    all_date = pd.DataFrame(index=pd.date_range(day1.strftime('%m/%d/%Y'),
                                                day2.strftime('%m/%d/%Y'),
                                                freq='H'))
    if len(dat) <= 1:
        dat = pd.DataFrame(columns=['day', 'hour', 'name', 'pol_name', 'units', 'val'])
    else:
        dat = dat[[3, 4, 6, 7, 8, 9]]
        dat.columns = ['day', 'hour', 'name', 'pol_name', 'units', 'val']
        dat['date'] = dat.day + '_' + dat.hour

        # Changing date type to string to datestamp
        dat['date'] = dat.date.apply(my_to_datetime)

        # Changing val type from string/object to numeric
        dat['val'] = dat.val.str.replace(',', '.').astype(float)

        # Filling empty dates
        dat.set_index('date', inplace=True)

    dat_complete = all_date.join(dat)
    dat_complete = dat_complete.drop(['day', 'hour'], axis=1)
    if file_name:
        file_name = file_name + ' .csv'
    else:
        file_name = str(parameter) + '_' + str(station)
    if csv:
        dat_complete.to_csv(file_name, index_label='date')
    else:
        return dat_complete


def all_met(cetesb_login, cetesb_password, start_date, end_date, station,
            in_k=False, rm_flag=True, file_name=None, csv_met=False):
    """
    Download meteorological parameters
    Parameters
    ----------
    cetesb_login : str
        cetesb qualar username.
    cetesb_password : str
        cetesb qualar username's password.
    start_date : str
        date to start download in %dd/%mm/%YYYY.
    end_date : str
        date to end download in %dd/%mm/%YYYY.
    station : int
        AQS code.
    in_k : Bool, optional
        Temperature in Kelvin. The default is False.
    rm_flag : Bool, optional
        Filter wind calm and no values wind direction. The default is True.
    file_name : str, optional
        Name of csv file.
    csv_met : Bool, optional
        Export to csv file. The default is False.
    Returns
    -------
    all_met_df : pandas DataFrame
        Data Frame with date index  (America/Sao_Paulo),
        TC, RH, WS and WD columns.
    """
    tc = cetesb_data_download(cetesb_login, cetesb_password,
                              start_date, end_date, 25, station)
    rh = cetesb_data_download(cetesb_login, cetesb_password,
                              start_date, end_date, 28, station)
    ws = cetesb_data_download(cetesb_login, cetesb_password,
                              start_date, end_date, 24, station)
    wd = cetesb_data_download(cetesb_login, cetesb_password,
                              start_date, end_date, 23, station)
    if in_k:
        K = 273.15
    else:
        K = 0

    all_met_df = pd.DataFrame({
        't2': tc.val + K,
        'rh2': rh.val,
        'ws': ws.val,
        'wd': wd.val
    }, index=tc.index)

    all_met_df.index = all_met_df.index.tz_localize('America/Sao_Paulo')

    # Filtering 777 and 888 values
    if rm_flag:
        filter_flags = all_met_df['wd'] <= 360
        all_met_df['wd'].where(filter_flags, inplace=True)

    if file_name:
        file_name = file_name + ' .csv'
    else:
        file_name = 'all_met_' + str(station) + '.csv'

    # Export to csv
    if csv_met:
        all_met_df.to_csv(file_name, index_label='date')
    else:
        return all_met_df
