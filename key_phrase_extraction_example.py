def key_phrase_extraction_example(client, message):
    try:
        documents = [message]

        response = client.extract_key_phrases(documents=documents)[0]
        response_keys=''
        if not response.is_error:
            ##print("\tKey Phrases:")
            ##for phrase in response.key_phrases:
                ##print("\t\t", phrase)
            response_keys = response.key_phrases
        else:
            ##print(response.id, response.error)
            response_keys = "Ключевые фразы отсутствуют"
    except Exception as err:
        print("Encountered exception. {}".format(err))

    return response_keys