import requests


def key_phrase_extraction(message):

    documents = {"documents": [{"id": message.chat.id, "language": "ru", "text": message.text}]}
    headers = {"Ocp-Apim-Subscription-Key": "50eb5695624243b59cc69f3c87a5289b"}
    response = requests.post(
        "https://emergencynotification.cognitiveservices.azure.com/text/analytics/v3.0/keyPhrases", headers=headers,
        json=documents)
    key_phrases = response.json()
    return key_phrases['documents'][0]['keyPhrases']
