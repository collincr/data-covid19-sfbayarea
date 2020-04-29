import io
import requests
import pandas as pd

county_fips = {"San Mateo": 6081,
               "Santa Clara": 6085,
               "Contra Costa": 6013}

def get_request_csv(url):
    sesh = requests.Session()
    req = sesh.get(url)
    content = req.content.decode("utf-8")

    return content

def parse_dataframe(df):
    dff = df[(df["countyFIPS"]==county_fips["Contra Costa"]) |
             (df["countyFIPS"]==county_fips["San Mateo"]) |
             (df["countyFIPS"]==county_fips["Santa Clara"])]

    values = dff.iloc[:,4:]
    values_t = values.T
    values_t.index = pd.DatetimeIndex(values_t.index)
    values_t.columns = dff["countyFIPS"].values

    return values_t


if __name__ == "__main__":
    cases_url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"
    cases_csv = get_request_csv(cases_url)
    cases_csv_io = io.StringIO(cases_csv)
    cases_df = pd.read_csv(cases_csv_io)
    cases_dft = parse_dataframe(cases_df)

    deaths_url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv"
    deaths_csv = get_request_csv(deaths_url)
    deaths_csv_io = io.StringIO(deaths_csv)
    deaths_df = pd.read_csv(deaths_csv_io)
    deaths_dft = parse_dataframe(deaths_df)
