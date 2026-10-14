import json
import requests

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json=input_json, headers=headers)

    # Error handling: blank input returns status code 400
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Step 1: convert the response text into a dictionary
    formatted_response = json.loads(response.text)

    # Step 2: walk down to the emotion scores
    emotions = formatted_response['emotionPredictions'][0]['emotion']

    # Step 2 (continued): pull out the five scores we need
    result = {
        'anger': emotions['anger'],
        'disgust': emotions['disgust'],
        'fear': emotions['fear'],
        'joy': emotions['joy'],
        'sadness': emotions['sadness']
    }

    # Step 3: find the emotion with the highest score
    dominant_emotion = max(result, key=result.get)

    # Step 4: add it and return the final format
    result['dominant_emotion'] = dominant_emotion
    return result