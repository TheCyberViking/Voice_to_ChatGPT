# Voice_to_ChatGPT
A simple script to allow you to speak to chatGPT and for it to respond using Python3 "Speech to Text" and "Text to Speech" using your systems Text To Speech Voice

# How To
- Set your API keys within the script
- When script runs, it will use your default microphone
- When you speak and speach is noticed it will convert that to text
- That converted speech_text will be sent to OpenAI
- The response from OpenAI will be converted to audio and played out default speakers
- Script will wait 2 seconds and then wait for your response again


# Required Modules
openai
pyttsx3
pyaudio
