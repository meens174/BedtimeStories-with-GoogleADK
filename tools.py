import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play


def generate_audio( text: str):
        """Generates Audio

        Args:
            text (_type_): the story passed on by the story telling agent
            
        """
        load_dotenv()
        api_key = os.getenv('ELEVENLABS_API_KEY')
        elevenlabs_client = ElevenLabs(api_key=api_key)
        # self.interaction.append({"role": "assistant", "content": text})
        print(f"\nAI Guide: {text}")

        audio_stream = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id="cgSgspJ2msm6clMCkdW9",
            # voice = "Hope",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
            # stream = True,
            # api_key=self.api_key
        )

        play(audio_stream)