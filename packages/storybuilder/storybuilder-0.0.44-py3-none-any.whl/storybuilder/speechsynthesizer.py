import io
import os
import pydub
import pyperclip
import uuid

import azure.cognitiveservices.speech as speechsdk

class speech_synthesizer():
    def __init__(self, speech_key, service_region):
        self.speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        self.speech_config.speech_synthesis_language = ""
        self.speech_config.speech_synthesis_voice_name = ""
        self.speech_synthesizer = None
        self.ssml = False
        self.kwargs = {}
        
    def set_voice(self, language, voice_name, **kwargs):
        self.speech_config.speech_synthesis_language = language
        self.speech_config.speech_synthesis_voice_name = voice_name
        self.kwargs = {}
        for key in kwargs:
            self.kwargs[key] = kwargs[key]
        
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
        if len(kwargs) > 0:
            self.ssml = True
        else:
            self.ssml = False

    def synthesize(self, text, output_path='synthesize', output_file_name=''):
        if self.ssml:
            ssml = "<speak version='1.0' xml:lang='en-US' xmlns='http://www.w3.org/2001/10/synthesis' "
            ssml += "xmlns:mstts='http://www.w3.org/2001/mstts' xmlns:emo='http://www.w3.org/2009/10/emotionml'> "
            ssml += f"<voice name='{self.speech_config.speech_synthesis_voice_name}'>"
            express_str = ""
            if "role" in self.kwargs:
                role_str = self.kwargs['role']
                express_str +=f" role='{role_str}'"
            if "style" in self.kwargs:
                style_str = self.kwargs['style']
                express_str +=f" style='{style_str}'"
            ssml += f"<mstts:express-as {express_str}>"
            prosody_open_str = ""
            prosody_close_str = ""
            if "prosody" in self.kwargs:
                prosody = self.kwargs['prosody']
                for key in prosody:
                    prosody_open_str += f" {key}='{prosody[key]}'"
                prosody_open_str = f"<prosody {prosody_open_str}>"
                prosody_close_str = "</prosody>"
            ssml += prosody_open_str + text + prosody_close_str
            ssml += "</mstts:express-as>"
            ssml += "</voice></speak>"
            result = self.speech_synthesizer.speak_ssml_async(ssml).get()
        else:
            result = self.speech_synthesizer.speak_text_async(text).get()
            
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            bytes = io.BytesIO(result.audio_data)
            sound = pydub.AudioSegment.from_file(bytes)
            
            if len(output_file_name) == 0:
                id = uuid.uuid4()
                file_name = f"voice-{id}.mp3"
            else:
                file_name = output_file_name

            sound.export(
                f"{output_path}/{file_name}",
                format="mp3",
                bitrate="190k",
                parameters=["-acodec", "libmp3lame"],
            )
            print("Finish writing to", file_name)
            return file_name
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
            return ""
                
if __name__ == "__main__":
    # Note: the voice setting will not overwrite the voice element in input SSML.
    choice = input("Please Enter Your Role(A. Tony  B. Eileen  C. John D. Xiaoshuang(Female) E. Yunxi(Male) F. Yunxi(Boy)):")

    kwargs = {}
    if choice in ("A", "a"): 
        language = "zh-CN"
        voice_name = "zh-CN-YunxiNeural"
    elif choice in ("B", "b"): 
        language = "zh-CN"
        voice_name = "zh-CN-XiaohanNeural"
    elif choice in ("C", "c"): 
        language = "zh-TW"
        voice_name = "zh-TW-YunJheNeural"
    elif choice in ("D", "d"): 
        language = "zh-CN"
        voice_name = "zh-CN-XiaoshuangNeural"
    elif choice in ("E", "e"): 
        language = "zh-CN"
        voice_name = "zh-CN-YunxiNeural"
    elif choice in ("F", "f"): 
        language = "zh-CN"
        voice_name = "zh-CN-YunxiNeural"
        kwargs["style"] = "chat"
        kwargs["role"] = "Boy"
    else:
        language = "zh-CN"
        voice_name = "zh-CN-liaoning-XiaobeiNeural"
        print("No valid role selected, go with 大碴子味")

    text = pyperclip.paste()
    if len(text) <= 1:
        text = "明月几时有？把酒问青天。不知天上宫阙，今夕是何年。我欲乘风归去，又恐琼楼玉宇，高处不胜寒。起舞弄清影，何似在人间。 转朱阁，低绮户，照无眠。不应有恨，何事长向别时圆？人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。"
    print("Synthesizing", text)

    synthesizer = speech_synthesizer()
    synthesizer.set_voice(language, voice_name, **kwargs)
    output_file = synthesizer.synthesize(text, "synthesize")    