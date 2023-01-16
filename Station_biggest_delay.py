import boto3
from boto3.dynamodb.conditions import Key, Attr

# Initialiser une session DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('trenitalia-test')

# Effectuer une requête pour récupérer tous les éléments de la table
response = table.scan()

# Récupérer les valeurs uniques de la colonne "column_name"
unique_values = set(item['train_number'] for item in response['Items'])

print(len(unique_values)) # Toutes les valeurs d'un numéro de train

trajets = [] # liste de liste : chaque élément contient
# des trajets d'un train effectué à différents jours

for route in unique_values:
    response = table.scan(
        FilterExpression=Attr('train_number').eq(int(route))
    )
    trajets.append(response)


for trajet in trajets:
    for train in trajet:

