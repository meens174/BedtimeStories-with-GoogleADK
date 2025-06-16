import os
import subprocess
from typing import IO
from io import BytesIO
from elevenlabs.client import ElevenLabs
from elevenlabs import  save, play
from elevenlabs import VoiceSettings
from dotenv import load_dotenv
# from pydub import AudioSegment
# from pydub.playback import play
import streamlit as st
import time
     
def generate_audio(text: str) -> IO[bytes]:
    """Generates Audio

    Args:
        text (_type_): the story passed on by the story telling agent

    """
    load_dotenv()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    elevenlabs_client = ElevenLabs(api_key=api_key)
    # self.interaction.append({"role": "assistant", "content": text})
    print(f"\nAI Guide: {text}")


    response  = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id="cgSgspJ2msm6clMCkdW9",
            optimize_streaming_latency="0",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
            voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
        )
    # save(response,'story.mp3')
    # with open('story.mp3', "rb") as f:
    #     mp3_data = f.read()
        
    # mp3_stream = BytesIO(mp3_data)
    # # subprocess.run(["ffplay", "-nodisp", "-autoexit", "story_audio.wav"],check = True)

    # # # Create a BytesIO object to hold audio data
    audio_stream = BytesIO()
    st.write("Streaming audio...")
    # # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)
    # # Reset stream position to the beginning
    audio_stream.seek(0)
    st.audio(audio_stream, autoplay=True)
   


    # # play(audio_stream)

    # # Example BytesIO object containing raw audio data


    # # # Run FFmpeg to play audio
    # process = subprocess.Popen(
    #     ["ffplay", "-i", "pipe:0","-f", "mp3","-nodisp", "-autoexit"],  # FFplay reads from stdin
    #     stdin=subprocess.PIPE,
    #     stdout=subprocess.DEVNULL,  # Suppress stdout output
    #     stderr=subprocess.DEVNULL   # Suppress stderr output
    # )

    # # Send BytesIO data to FFmpeg
    # process.communicate(input=audio_stream.getvalue())
    # Simulating streaming by loading chunks dynamically
  



    
