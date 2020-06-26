key = "50eb5695624243b59cc69f3c87a5289b"
endpoint = "https://emergencynotification.cognitiveservices.azure.com/"
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def key_phrase_extraction_example(client, message):
    response_keys=''
    try:
        documents = [message]
        test=client.extract_key_phrases(documents=documents)
        response = test[0]
        print(test)
        if not response.is_error:
            response_keys = response.key_phrases
        else:
            response_keys = "Ключевые фразы отсутствуют"
    except Exception as err:
        print("Encountered exception. {}".format(err))

    return response_keys