import boto3

# Créer une session DynamoDB
dynamodb = boto3.client('dynamodb')

# Appeler la méthode describe-table pour récupérer les informations de la table
response = dynamodb.describe_table(TableName='trenitalia-test')

# Récupérer le nombre d'éléments de la table
item_count = response['Table']['ItemCount']

# Afficher le nombre d'éléments
print(item_count)
