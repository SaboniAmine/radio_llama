import requests
import os
from abc import abstractmethod
import time
import dotenv
import json

dotenv.load_dotenv()

CHUNK_SIZE = 1024



class TextToSpeech:
    @abstractmethod
    def transform(self, text: str, voice_id: str, save: bool = False):
        raise NotImplementedError


class ElevenLabsTextToSpeech(TextToSpeech):
    def transform(self, text: str, voice_id: str, save: bool = False):
        url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": os.getenv('API_KEY')
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.71,
                "similarity_boost": 0.87
            }
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            print(response.json())
            return None
        if save:
            timestamp = int(time.time())
            with open("elevenlabs_" + str(timestamp) + ".mp3", 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
        return response.content


from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser


model = ChatMistralAI(model="mistral-large-latest")

parser = StrOutputParser()

messages = [
    HumanMessage(content="""<role>
Tu es un animateur radio chevronné qui anime régulièrement des émissions sur une webradio Jazz.

<objectif>
Ton objectif est d'écrire le contenu d'une intervention de 6 secondes.
Ton objectif est de parlé de la musique qui vient de se finir et de lancer la musique suivante, en l'accompagnant d'une anecdote sur l'artiste ou le morceau.

<ton>
Utilise un ton joyeux et agréable à écouter
Sois enthousiaste et engageant

Pour écrire le script , suis les étapes ci-dessous :
1 - Réfléchis aux éléments clés à inclure dans ton script selon les objectifs définis
2 - Rédige plusieurs versions du script en t'efforçant de respecter le ton fourni. Évite les formulations monotones ou ennuyeuses.
3 - Peaufine le script jusqu'à obtenir une version finale de 6 qui sonne bien à l'oral et donne envie aux auditeurs d'en savoir plus.
4 - Vérifie que le script final reflète bien le style d'inspiration et le ton fourni, tout en restant fidèle à ta propre voix et ton propre style d'animation.

<tache>
Écris le script final de 6 secondes maximum pour l'intervention radio.

<output_format>
Formate le script au format json avec une clé "script" contenant le texte du script final.

<infos>
Musique précédente :
    titre : Hit The Road Jack
    artiste : Ray Charles
    date de sortie : 1960
    genre : rythm and blues, Jazz

Musique suivante :
    titre : What a Wonderful World
    artiste : Louis Armstrong
    date de sortie : 1967
    genre : Jazz
""")]

chain = model | parser

result = chain.invoke(messages)

voices = {
    "Female-Animation" : "KmqhNPEmmOndTBOPk4mJ",    # Lucie
    # "Male-Deep" : "wyZnrAs18zdIj8UgFSV8",           # Martin Dupont Profond (Articulation lente et hachée)
    "Male-Calm" : "GK4x7OSjC6JLlDqAZnAE",           # Léo Latti
    "Male-Pleasant" : "1ns94GwK9YDCJoL6Nglv",       # Nicolas animateur
    "Female-Pleasant" : "qMfbtjrTDTlGtBy52G6E",     # Emilie Lacroix
    "Male-Serious" : "AmMsHJaCw4BtwV3KoUXF",        # Nicolas Petit
    "Female-Confident" : "glDtoWIoIgk38YbycCwG",    # Clara Dupont
    "Male-Narration" : "aQROLel5sQbj1vuIVi6B",      # Nicolas - Narration
}

text_to_speech = json.loads(result)["script"]
voice_id_eleven = voices["Male-Calm"]

print("Text to Speech :")
print(text_to_speech)

t2s = ElevenLabsTextToSpeech()
t2s.transform(text_to_speech, voice_id_eleven, save=True)
