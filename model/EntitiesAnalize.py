import requests #для когнитивки
def EntitiesAnalize(client, keys):
    entities = ''
    documents = {"documents": [{"id": 1, "language": "ru", "text": keys}]}
    headers = {"Ocp-Apim-Subscription-Key": "50eb5695624243b59cc69f3c87a5289b"}
    response = requests.post("https://emergencynotification.cognitiveservices.azure.com//text/analytics/v2.1/entities", headers=headers, json=documents)
    enti_ties = response.json()
    #pprint(key_phrases)
    dictbuf=enti_ties['documents']# получил список словарей с сущностями
    dictbuf1=dictbuf[0]
    enti_ties=dictbuf1['entities']
    for i in enti_ties:
        entities=entities+i['name']+'('+i['type']+'), '
    print(entities)
    #response_keys = dictbuf1['keyPhrases']

    return entities
