from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speechsdk
import matplotlib.pyplot as plt

# Azure AI Configuration
TEXT_ANALYTICS_KEY = "EWlQowRIBJZSAqg4Ayd3C5cX8c92s7gYeVpyUXjBdeQ1AkZUAnnmJQQJ99ALACYeBjFXJ3w3AAAEACOGajUF"
TEXT_ANALYTICS_ENDPOINT = "https://maxcomazureaiservicestest.cognitiveservices.azure.com/"
SPEECH_KEY = "87xEviM2aOQYL6RadXTILTfTH1xwCQNKB8ea0lOl4sQPvScvcrTHJQQJ99ALACYeBjFXJ3w3AAAEACOGarCv"
SPEECH_REGION = "eastus"

# Authenticate Text Analytics Client
def authenticate_text_client():
    credential = AzureKeyCredential(TEXT_ANALYTICS_KEY)
    client = TextAnalyticsClient(endpoint=TEXT_ANALYTICS_ENDPOINT, credential=credential)
    return client

# Analyze Sentiment with Details
def analyze_sentiment(client, text):
    response = client.analyze_sentiment(documents=[text])[0]
    sentiment_details = {
        "sentiment": response.sentiment,
        "confidence_scores": response.confidence_scores,
        "key_phrases": extract_key_phrases(client, text)
    }
    return sentiment_details

# Extract Key Phrases
def extract_key_phrases(client, text):
    response = client.extract_key_phrases(documents=[text])
    if response[0].is_error:
        return []
    return response[0].key_phrases

# Speech-to-Text from Audio File
def speech_to_text_from_file(audio_file_path):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_input = speechsdk.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    print(f"Processing audio file: {audio_file_path}")
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized. Please check the audio file.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
    return None

# Text-to-Speech
def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    print(f"Speaking: {text}")
    speech_synthesizer.speak_text_async(text).get()

# Plot Sentiment Scores
def plot_sentiment_scores(confidence_scores):
    scores = {
        "Positive": confidence_scores.positive,
        "Neutral": confidence_scores.neutral,
        "Negative": confidence_scores.negative
    }
    plt.bar(scores.keys(), scores.values())
    plt.title("Sentiment Confidence Scores")
    plt.ylabel("Confidence")
    plt.xlabel("Sentiment Type")
    plt.show()

if __name__ == "__main__":
    # Authenticate Text Analytics Client
    text_client = authenticate_text_client()

    print("Azure AI Speech Sentiment Analysis with Insights and Visualization")
    print("Type 'exit' to quit.\n")

    while True:
        # Get audio file path
        audio_file_path = input("Enter the path to your audio file (or type 'exit' to quit): ")
        if audio_file_path.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        # Step 1: Transcribe Speech from Audio File
        recognized_text = speech_to_text_from_file(audio_file_path)
        if not recognized_text:
            continue

        # Step 2: Analyze Sentiment
        try:
            sentiment_details = analyze_sentiment(text_client, recognized_text)
            sentiment = sentiment_details["sentiment"]
            confidence_scores = sentiment_details["confidence_scores"]
            key_phrases = sentiment_details["key_phrases"]

            sentiment_message = (
                f"The sentiment of the message is {sentiment}.\n"
                f"Confidence Scores - Positive: {confidence_scores.positive}, "
                f"Neutral: {confidence_scores.neutral}, Negative: {confidence_scores.negative}\n"
                f"Key Phrases: {', '.join(key_phrases) if key_phrases else 'No key phrases extracted.'}"
            )
            print(sentiment_message)

            # Step 3: Visualize Sentiment Scores
            plot_sentiment_scores(confidence_scores)

        except Exception as e:
            print(f"An error occurred: {e}")
