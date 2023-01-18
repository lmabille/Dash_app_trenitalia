import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from datetime import datetime


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
    date = datetime.fromtimestamp(stop['departing_time']/1000)  if int(stop['departing_time']) > 0 else None
    stop['departing_time'] = date


for stop in stop_in_station:
    if stop['train_number'] in dict:
        dict[stop['train_number']].append(stop)
    else:
        dict[stop['train_number']] = [stop]

my_dic = {}
big_dic = {}
for train_number in dict.keys():
    liste_de_trajet = dict[train_number]
    for trajet in liste_de_trajet:
        if trajet['departing_time']:
            my_date = f"{trajet['departing_time'].day}.{trajet['departing_time'].month}"
            if my_date in my_dic:
                my_dic[my_date].append(trajet)
            else:
                my_dic[my_date] = [trajet]
    for elt in my_dic.keys():
        if elt in big_dic.keys():
            big_dic[elt].append(my_dic)
        else:
            big_dic[elt] = [my_dic]
    my_dic = {}

print(ici)









print(len(stop_in_station))


df = pd.DataFrame(list(dict.items()), columns=['train_type', 'minutes_delayed'])

df.to_csv('difference_color.csv', index=False)


# Créer un graphique en bar avec plotly express
fig = px.bar(df, x='train_type', y='minutes_delayed')



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