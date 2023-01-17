import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Opening JSON file
with open('stations_selection.json') as json_file:
    Id_StationName = json.load(json_file)
dict_ID_StationName = {}
for station in Id_StationName:
    dict_ID_StationName[station['id']] = station['name']


# Initialiser une session DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('trenitalia-test')

# Effectuer une requête pour récupérer tous les éléments de la table
response = table.scan()
stop_in_station = response['Items']
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    stop_in_station.extend(response['Items'])

dict = {} # IdStation_NumberOfDelay

for stop in stop_in_station:
    if stop['delay']:
        if dict_ID_StationName[stop['current_station']] in dict.keys():
            dict[dict_ID_StationName[stop['current_station']]] += 1
        else:
            dict[dict_ID_StationName[stop['current_station']]] = 1

print(len(stop_in_station))



df = pd.DataFrame(list(dict.items()), columns=['station_name', 'number_of_train_delayed'])

# Créer un graphique en bar avec plotly express
fig = px.bar(df, x='station_name', y='number_of_train_delayed')



# Récupérer les valeurs uniques de la colonne "column_name"
# unique_values = set(item['train_number'] for item in response['Items'])


app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':

    app.run_server(debug=True)