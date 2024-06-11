import os
import uuid

from .storyprofiles import CHARACTER_VOICE_PROFILES
from .speechsynthesizer import speech_synthesizer

#Replace with your azure subscription and region
AZURE_SPEECH_KEY = os.environ.get('AZURE_SPEECH_KEY')
AZURE_SERVICE_REGION = os.environ.get('AZURE_SPEECH_REGION')

class VoiceSynthesizer:
    def __init__(self, azureSubscription=AZURE_SPEECH_KEY, azureRegion=AZURE_SERVICE_REGION, voiceProfiles=CHARACTER_VOICE_PROFILES):
        self.voiceProfiles = voiceProfiles
        self.subscription = azureSubscription
        self.region = azureRegion

    def _newAudioFileName(self, language=None):
        if language and language.lower() not in ('cn', 'zh-cn'):
            return f'voice-{str(uuid.uuid4())}.{language}.mp3'
        else:
            return f'voice-{str(uuid.uuid4())}.mp3'
            
    def _fixAudioFileName(self, fileName, language):
        if f'{language}.mp3' in '.'.join(fileName.split('.')[-2:]):
            return fileName
        else:
            return '.'.join(fileName.split('.')[:-1])+f'.{language}.mp3'            

    @staticmethod
    def correctPronunciation(text, language, correctionDict):
        if language in correctionDict:
            for key in correctionDict[language]:
                text = text.replace(key, correctionDict[key])
        return text
    
    def synthesizeFile(self, character, text, language, outputPath, fileName=None, stopSymbols=['|', '\n']):
        synthesizer = speech_synthesizer(speech_key=self.subscription, service_region=self.region)

        character = 'M' if character == '' else character
        synthesizer.set_voice(
            language,
            CHARACTER_VOICE_PROFILES[character][language]['voiceName'],
            **CHARACTER_VOICE_PROFILES[character][language]['kwargs'])
        if fileName == None or len(fileName) < 1:
            fileName = self._newAudioFileName(language)
            print(f'No input file_name, generate new file name as: {fileName}')
        elif language.lower() not in ('cn', 'zh-cn'):
            fileName = self._fixAudioFileName(fileName, language)
            print(f'Filename with language code: {fileName}')

        print('Original:', text)
        newText = text
        for symbol in stopSymbols:
            newText = newText.split(symbol)[0]
        print('Corrected:', newText)

        try:
            synthesizer.synthesize(newText, outputPath, fileName)
        except Exception as e:
            print(e)

        return {
            "fileName": fileName,
            "originalText": text,
            "correctedText": newText,
            "character": character,
        }