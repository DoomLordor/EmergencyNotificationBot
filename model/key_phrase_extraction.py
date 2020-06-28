import requests #для когнитивки
def key_phrase_extraction(client, message):
    response_keys = ''
    documents = {"documents": [{"id": message.chat.id, "language": "ru", "text": message.text}]}
    headers = {"Ocp-Apim-Subscription-Key": "50eb5695624243b59cc69f3c87a5289b"}
    response = requests.post("https://emergencynotification.cognitiveservices.azure.com/text/analytics/v3.0/keyPhrases", headers=headers, json=documents)
    key_phrases = response.json()
    #pprint(key_phrases)
    dictbuf=key_phrases['documents']
    dictbuf1=dictbuf[0]
    response_keys = dictbuf1['keyPhrases']
    #print(response_keys)
    return response_keys
