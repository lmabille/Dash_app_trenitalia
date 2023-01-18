import boto3
import pandas as pd
import os
import json
import matplotlib.pyplot as plt

dynamo_db_table_name = "trenitalia-test"
dynamo_db = boto3.resource('dynamodb')
table = dynamo_db.Table(dynamo_db_table_name)


def query_table(df):
    df = df[df['delay'] > 0]
    biggest_delays = df.groupby('train_number', as_index=False)['delay'].sum().sort_values(by=['delay'],
                                                                                           ascending=False)
    biggest_delays_nums = biggest_delays['train_number'][:5].to_list()
    delayed = df[df['train_number'].isin(biggest_delays_nums)]

    json_file = open("stations_selection.json")
    stations_selection = json.load(json_file)
    stations = {}
    for el in stations_selection:
        stations[el["id"]] = el["name"]
    stations["S11781"] = "REGGIO CALABRIA CENTRALE"
    stations['S11774'] = "VILLA SAN GIOVANNI"

    for ind, tr_num in enumerate(biggest_delays_nums):
        curr_df = delayed[delayed['train_number'] == tr_num]
        origins_id = curr_df['origin'].to_list()
        destinations = curr_df['destination'].to_list()
        delay = curr_df['delay'].to_list()
        current_station_ids = curr_df['current_station'].to_list()
        origins = [stations[i] for i in origins_id]
        current_stations = [stations[i] for i in current_station_ids]

        plt_df = pd.DataFrame({"x": current_stations, "delay": delay})
        ax = plt_df.plot.bar(x="x", y='delay', title="Delay on stations")
        ax.set_xlabel("Current station")
        ax.set_ylabel("Delay")
        plt.show()

        table_df = pd.DataFrame({"Origin": origins, "Destinations": destinations})
        print(table_df)

    json_file.close()


def export_table():
    if not "table.csv" in os.listdir():
        dynamo_db_table_name = "trenitalia-test"
        dynamo_db = boto3.resource('dynamodb')
        table = dynamo_db.Table(dynamo_db_table_name)
        response = table.scan()
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        df = pd.DataFrame(data)
        df.to_csv('table.csv')
    else:
        df = pd.read_csv("table.csv")
    query_table(df)


if __name__ == '__main__':
    export_table()
