import os
import openai
import websockets
import asyncio
import base64
import json
import pyttsx3
import time
import pyaudio


openai.api_key = os.getenv("OPENAI_API_KEY")
auth_key = 'YOUR_API_KEY'

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
engine = pyttsx3.init()
while True:
    async def send_receive():
        async with websockets.connect(
                URL,
                extra_headers=(("Authorization", auth_key),),
                ping_interval=5,
                ping_timeout=20
        ) as _ws:
            session_begins = await _ws.recv()

            async def send():
                while True:
                    try:
                        data = stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({"audio_data": str(data)})
                        await _ws.send(json_data)
                    except websockets.exceptions.ConnectionClosedError as e:
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"
                    await asyncio.sleep(0.01)
                return True

            async def receive():
                while True:
                    try:
                        result_str = await _ws.recv()
                    except websockets.exceptions.ConnectionClosedError as e:
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"
            send_result, receive_result = await asyncio.gather(send(), receive())
            prompt = receive_result
            try:
                response = openai.Completion.create(
                    engine="davinci",
                    prompt=prompt,
                    temperature=0.9,
                    max_tokens=150,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0.6,
                    stop=["\n", " Human:", " AI:"]
                )
                engine.say(str(response))
            except:
                pass
    time.sleep(2)
