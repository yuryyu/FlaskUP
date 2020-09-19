import io
import os
import json
import csv
import pandas as pd

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
from google.protobuf.json_format import MessageToDict, MessageToJson

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
credential_path = os.path.join(APP_ROOT, 'SpeechClassAPI-1612.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
tshift = 0.15

class STT():
    def __init__(self):        
        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=44100,
            language_code='iw-IL',
            enable_word_time_offsets=True)            
        self.sttclient = speech_v1p1beta1.SpeechClient()

    def opensoundfile(self, file_name):    
        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)
        return audio

    def recognize(self,audio):
        # Detects speech in the audio file and return results to caller
        return self.sttclient.recognize(self.config, audio)

    def parse_result(self,result):
        data={}
        for result in result.results:
            alternative = result.alternatives[0]
            print('Transcript: {}'.format(alternative.transcript))
            # data['Transcript:'] = alternative.transcript
            print('Confidence: {}'.format(alternative.confidence))
            # data['Confidence:'] = alternative.confidence
            data['Words'] = []
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time
                print('Word: {}, start_time: {}, end_time: {}'.format(
                    word,
                    start_time.seconds + start_time.nanos * 1e-9 + tshift,
                    end_time.seconds + end_time.nanos * 1e-9 + tshift))
                data['Words'].append({
                    'word': word,                    
                    'start time': round(start_time.seconds + start_time.nanos * 1e-9 + tshift, 2),
                    'end time': round(end_time.seconds + end_time.nanos * 1e-9 + tshift, 2)
                })    
        return data


def mainSTT(fname):
    st= STT()
    audio=st.opensoundfile(fname)
    rz=st.recognize(audio)    
    data = st.parse_result(rz)   
    pd.DataFrame(data['Words']).to_csv(os.path.join(APP_ROOT,'csv/out.csv'), index=False)
    # dicts = MessageToDict(rz)
    # self.json = MessageToJson(self.results)
    # with open('data_saved.json', 'w') as outfile:
    #     json.dump(data, outfile)     


if __name__ == '__main__':
    mainSTT('input_s.mp3')
    