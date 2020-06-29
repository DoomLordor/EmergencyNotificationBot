def key_phrase_extraction(client, message):
    response_keys = ''
    try:
        documents = [message]
        test = client.extract_key_phrases(documents=documents)
        response = test[0]
        if not response.is_error:
            response_keys = response.key_phrases
        else:
            response_keys = "Ключевые фразы отсутствуют"
    except Exception as err:
        print("Encountered exception. {}".format(err))
    return response_keys
