import pandas as pd
import xmltodict
import datetime as dt
import matplotlib.pyplot as plt

def weight_df_from_file(filename):
    with open(filename) as health_export_file:
        health_data_dict = xmltodict.parse(health_export_file.read())
    
    health_data = health_data_dict['HealthData']
    health_records = health_data['Record']
    TYPE = '@type'
    record_types = set(map(lambda record: record[TYPE], health_data['Record']))

    def get_records(record_type):
        return [record for record in health_records if record[TYPE] == record_type]
    
    records_by_type = {record_type: get_records(record_type) for record_type in record_types}
    BODY_MASS = 'HKQuantityTypeIdentifierBodyMass'

    weight_records = records_by_type[BODY_MASS]

    def date_from_record(record):
        return dt.datetime.strptime(record['@startDate'].split(' ', maxsplit=1)[0], '%Y-%m-%d').date()

    def weight_from_record(record):
        return record['@value']

    def row_dict_from_record(record):
        return {'date': date_from_record(record), 'weight': weight_from_record(record)}
    
    weight_df = pd.DataFrame([row_dict_from_record(weight_record) for weight_record in weight_records])
    weight_df['date'] = pd.to_datetime(weight_df['date'])
    weight_df['weight'] = weight_df['weight'].astype(float)
    weight_df = weight_df.set_index('date').sort_index()
    weight_df['7day_rolling_avg_weight'] = weight_df['weight'].rolling(window=dt.timedelta(days=7)).mean()

    return weight_df


def plot_from_file(filename):
    weight_df = weight_df_from_file(filename)
    weight_df[dt.date(2025, 1, 1):]['7day_rolling_avg_weight'].astype(float).plot()
    plt.ylabel('lbs')
    for w in range(180, 201, 10):
        plt.axhline(w, c='k', ls=':')

    plt.legend()
    plt.title('2025 Weight Tracking')
