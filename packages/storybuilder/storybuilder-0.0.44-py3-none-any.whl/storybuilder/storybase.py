from typing import List, Dict, Union
import copy

from .utility import *

RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
RESET  = "\033[0m"

DEFAULT_LANGUAGE="zh-CN"
LANGUAGE_ENG="en-US"
DEFAULT_NARRATOR="M"
VISIBLE_ACTORS=("boy", "girl", "eily", "eilly")
VISIBLE=0
INVISIBLE_ACTORS=("", "M", "F")
INVISIBLE=1
SCENARIO_ACTORS=("ending", "exam", "concentrak", "notes")
SCENARIO=2
LOCAL_DEFAULT_ROOT="./test"

BREAK_TIME="<break time=\"1500ms\"/>"
BULLET_KEY="li"


ENDING_SOUND="/story/audios/OurMusicBox - 24 Hour Coverage - intro.mp3"

class MText:
    def __init__(self, value:Union[str, dict[str, str]], language:str=None):
        if isinstance(value, MText):
            self.data = copy.deepcopy(value.data)
        elif isinstance(value, str):
            self.data = value if language == None else {language: value}
        elif isinstance(value, dict) and any(isinstance(v, str) for v in value.values()):
            self.data = {}
            for key in value:
                if isinstance(value[key], str):
                    self.data[key] = value[key]
        else:
            self.data = ""
    
    def len(self):
        return len(self.data)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.data == other
        elif isinstance(other, MText):
            return self.data == other.data
        return False        
      
    def copy(self):
        return copy.deepcopy(self)
    
    def firstValidPair(self):
        if isinstance(self.data, dict):
            key = next(iter(self.data), None)
            return key, self.data[key] if key != None else None
        else:
            return None, self.data
    
    def merge(self, newData):
        if isinstance(self.data, str):
            if isinstance(newData, dict):
                result = MText({**{DEFAULT_LANGUAGE:self.data}, **newData})
            elif isinstance(newData, MText):
                result = MText(self.data, DEFAULT_LANGUAGE).merge(newData.data)
            elif newData != None and len(newData) > 0:
                result = MText(newData)
            else:
                result = self.copy()
        else:
            if isinstance(newData, dict):
                result = MText({**self.data, **newData})
            elif isinstance(newData, MText):
                result = self.merge(newData.data)
            elif newData != None and len(newData) > 0:
                result = MText({**self.data, **{DEFAULT_LANGUAGE:newData}})
            else:
                result = self.copy()
        return result

    def export(self):
        if isinstance(self.data, str):
            return self.data
        elif isinstance(self.data, dict):
            data = {}
            for key in self.data.keys():
                if isinstance(self.data[key], str) and len(self.data[key])>0:
                    data[key] = self.data[key]
            if len(data) > 0:
                return data
            return None

class MList:
    def __init__(self, value:Union[str, list, dict[str, list]], language:str=None):
        if isinstance(value, str):
            self.data = [value] if language == None else {language: [value]}
        elif isinstance(value, list):
            self.data = value if language == None else {language: value}
        elif isinstance(value, dict) and any(isinstance(v, list) for v in value.values()):
            self.data = {}
            for key in value:
                if isinstance(value[key], list):
                    self.data[key] = value[key]
        elif isinstance(value, MList):
            self.data = copy.deepcopy(value.data)
        else:
            self.data = []

    def __eq__(self, other):
        if isinstance(other, list):
            return self.data == other
        elif isinstance(other, MList):
            return self.data == other.data
        return False

    def copy(self):
        return copy.deepcopy(self)
    
    def getMTextByPos(self, pos):
        if pos < len(self.firstValidPair()[1]) and pos >= 0:
            if isinstance(self.data, dict):
                result = {}
                for key in self.data:
                    result[key] = self.data[key][pos]
                return MText(result)
            return MText(self.data[pos])
        
    def getListByLanguage(self, language):
        if isinstance(self.data, dict) and language in self.data.keys():
            return copy.deepcopy(self.data[language])
        elif isinstance(self.data, list) and language == DEFAULT_LANGUAGE:
            return copy.deepcopy(self.data)
        return []

    def firstValidPair(self):
        if isinstance(self.data, dict):
            key = next(iter(self.data), None)
            return key, self.data[key] if key != None else None
        else:
            return None, self.data

    def export(self):
        if isinstance(self.data, list):
            return self.data
        elif isinstance(self.data, dict):
            data = {}
            for key in self.data.keys():
                if isinstance(self.data[key], list):
                    data[key] = self.data[key]
            if len(data) > 0:
                return data
            return None
        
class HTML:
    def __init__(self, template:str=None, textList:List[Dict[str, str]]=None):
        self.template = template
        self.bullets = []
        self.elements = []
        if isinstance(textList, list):
            for textObject in textList:
                if isinstance(textObject, dict):
                    key = next(iter(textObject), None)
                    if key != None and key == BULLET_KEY: #bullet tag
                        self.bullets.append(textObject[key])
                    elif key != None:
                        self.elements.append(textObject)

    @staticmethod
    def loadFromText(htmlText:str):
        textList, template = extract_html_elements(htmlText)
        return HTML(template=template, textList=textList)
    
    def copy(self):
        return copy.deepcopy(self)

    def setTemplate(self, template):
        self.template = template

    def addElement(self, tag, text):
        self.elements.append({tag: text})

    def updateElement(self, pos, tag, text):
        if pos < len(self.elements) and pos >= 0:
            self.elements[pos] = {tag: text}

    def removeElement(self, pos):
        if pos < len(self.elements) and pos >= 0:
            self.elements.pop(pos)

    def addBullet(self, text):
        self.bullets.append(text)

    def updateBullet(self, pos, text):
        if pos < len(self.bullets) and pos >= 0:
            self.bullets[pos] = text

    def removeBullet(self, pos):
        if pos < len(self.bullets) and pos >= 0:
            self.bullets.pop(pos)

    def exportBullets(self):
        return self.bullets.copy()

    def exportElements(self):
        return self.elements.copy()

    def export(self):
        result = self.template
        if isinstance(result, str):
            for entry in self.elements:
                key = next(iter(entry), None)
                if key != None:
                    result = result.replace("{"+key+"}", entry[key], 1)
            result = result.replace("{"+BULLET_KEY+"}", ("</"+BULLET_KEY+"><"+BULLET_KEY+">").join(self.bullets))
        return result
    
    def exportScripts(self):
        if isinstance(self.template, str):
            resultList = []
            outScripts = copy.deepcopy(self.elements)
            pattern = r"\{([a-zA-Z0-9]+)\}"  # Matches { followed by alphanumeric characters
            # Find all occurrences and extract the placeholder names
            placeholders = [match.group(1) for match in re.finditer(pattern, self.template)]
            for placeholder in placeholders:
                if placeholder == BULLET_KEY:
                    resultList.append(BREAK_TIME.join(self.bullets))
                else:
                    for j, pair in enumerate(outScripts):
                        if next(iter(pair), None) == placeholder:
                            resultList.append(next(iter(pair.values()), None))
                            outScripts.pop(j)
                            break

            return BREAK_TIME.join(resultList)

        return None
        
class MHTML:
    def __init__(self, template:str, data):
        self.template = template
        self.data = data
    
    @staticmethod
    def loadFromText(htmlText:MText):
        if isinstance(htmlText, MText):
            htmlObject = htmlText.export()
        elif isinstance(htmlText, dict) or isinstance(htmlText, str):
            htmlObject = htmlText
        else:
            return MHTML(None, None)
        template = None
        if isinstance(htmlObject, str):
            htmlData = HTML.loadFromText(htmlObject)
            return MHTML(htmlData.template, htmlData)
        else:
            htmlDict = {}
            for key in htmlObject:
                htmlDict[key] = HTML.loadFromText(htmlObject[key])
            if DEFAULT_LANGUAGE not in htmlObject:
                print(f"{YELLOW}WARNING{RESET}: No language version for {DEFAULT_LANGUAGE} detected, switch to first available language")
                template = htmlDict[next(iter(htmlDict), None)].template
            else:
                template = htmlDict[DEFAULT_LANGUAGE].template

            return MHTML(template, htmlDict)
    
    def copy(self):
        return copy.deepcopy(self)
    
    def setTemplate(self, template:str):
        if isinstance(self.data, HTML):
            self.data.setTemplate(template)
        elif isinstance(self.data, dict):
            data = {}
            for key in self.data:
                data[key] = self.data[key].setTemplate(template)

    def addElement(self, tag, text, **kwargs):
        if tag == BULLET_KEY:
            self.addBullet(text)
        else:
            if isinstance(text, str):
                if isinstance(self.data, HTML):
                    self.data.addElement(tag, text)
                elif isinstance(self.data, dict):
                    if kwargs.get("targetLanguage", None) != None:
                        self.data[kwargs["targetLanguage"]].addElement(tag, text)
                    else:
                        for key in self.data:
                            self.data[key].addElement(tag, text)
            elif isinstance(text, dict):
                if isinstance(self.data, HTML):
                    self.data = {DEFAULT_LANGUAGE: self.data}
                if isinstance(self.data, HTML) or isinstance(self.data, dict):
                    for key in text:
                        if key not in self.data:
                            self.data[key] = self.data[DEFAULT_LANGUAGE]
                        for key in self.data:
                            self.addElement(tag, text[key] if key in text else text[next(iter(text), None)], targetLanguage=key)
            elif isinstance(text, MText):
                self.addElement(tag, text.data)

    def updateElement(self, pos, tag, text, **kwargs):
        if pos < len(self.data.bullets \
                     if isinstance(self.data, HTML) \
                     else (self.data[DEFAULT_LANGUAGE].bullets \
                            if isinstance(self.data, dict) \
                            else [])) and pos >= 0:
            self.data.bullets[pos] = text

            if isinstance(text, str):
                if isinstance(self.data, HTML):
                    self.data.updateElement(pos, tag, text)
                elif isinstance(self.data, dict):
                    if kwargs.get("targetLanguage", None) != None:
                        self.data[kwargs["targetLanguage"]].updateElement(pos, tag, text)
                    else:
                        for key in self.data:
                            self.data[key].updateElement(pos, tag, text)
            elif isinstance(text, dict):
                if isinstance(self.data, HTML):
                    self.data = {DEFAULT_LANGUAGE: self.data}
                if isinstance(self.data, HTML) or isinstance(self.data, dict):
                    for key in text:
                        if key not in self.data:
                            self.data[key] = self.data[DEFAULT_LANGUAGE]
                        for key in self.data:
                            self.updateElement(pos, tag, text[key] if key in text else text[next(iter(text), None)], targetLanguage=key)
            elif isinstance(text, MText):
                self.updateElement(pos, tag, text.data)
        
            return True
        
        return False

    def removeElement(self, pos):
        if pos < len(self.data.bullets \
                     if isinstance(self.data, HTML) \
                     else (self.data[DEFAULT_LANGUAGE].bullets \
                            if isinstance(self.data, dict) \
                            else [])) and pos >= 0:
            if isinstance(self.data, HTML):
                self.data.removeElement(pos)
            elif isinstance(self.data, dict):
                for key in self.data:
                    self.data[key].removeElement(pos)
            
            return True
        
        return False

    def addBullet(self, text, **kwargs):
        if isinstance(text, str):
            if isinstance(self.data, HTML):
                self.data.addBullet(text)
            elif isinstance(self.data, dict):
                if kwargs.get("targetLanguage", None) != None:
                    self.data[kwargs["targetLanguage"]].addBullet(text)
                else:
                    for key in self.data:
                        self.data[key].addBullet(text)
        elif isinstance(text, dict):
            if isinstance(self.data, HTML):
                self.data = {DEFAULT_LANGUAGE: self.data}
            if isinstance(self.data, HTML) or isinstance(self.data, dict):
                for key in text:
                    if key not in self.data:
                        self.data[key] = self.data[DEFAULT_LANGUAGE]
                    for key in self.data:
                        self.addBullet(text[key] if key in text else text[next(iter(text), None)], targetLanguage=key)
        elif isinstance(text, MText):
            self.addBullet(text.data)

    def updateBullet(self, pos, text, **kwargs):
        if pos < len(self.data.bullets \
                     if isinstance(self.data, HTML) \
                     else (self.data[DEFAULT_LANGUAGE].bullets \
                            if isinstance(self.data, dict) \
                            else [])) and pos >= 0:
            self.data.bullets[pos] = text

            if isinstance(text, str):
                if isinstance(self.data, HTML):
                    self.data.updateBullet(pos, text)
                elif isinstance(self.data, dict):
                    if kwargs.get("targetLanguage", None) != None:
                        self.data[kwargs["targetLanguage"]].updateBullet(pos, text)
                    else:
                        for key in self.data:
                            self.data[key].updateBullet(pos, text)
            elif isinstance(text, dict):
                if isinstance(self.data, HTML):
                    self.data = {DEFAULT_LANGUAGE: self.data}
                if isinstance(self.data, HTML) or isinstance(self.data, dict):
                    for key in text:
                        if key not in self.data:
                            self.data[key] = self.data[DEFAULT_LANGUAGE]
                        for key in self.data:
                            self.updateBullet(pos, text[key] if key in text else text[next(iter(text), None)], targetLanguage=key)
            elif isinstance(text, MText):
                self.updateBullet(pos, text.data)
        
            return True
        
        return False

    def removeBullet(self, pos):
        if pos < len(self.data.bullets \
                     if isinstance(self.data, HTML) \
                     else (self.data[DEFAULT_LANGUAGE].bullets \
                            if isinstance(self.data, dict) \
                            else [])) and pos >= 0:
            if isinstance(self.data, HTML):
                self.data.removeBullet(pos)
            elif isinstance(self.data, dict):
                for key in self.data:
                    self.data[key].removeBullet(pos)
            
            return True
        
        return False

    def exportBullets(self):
        if isinstance(self.data, HTML):
            return self.data.exportBullets()
        elif isinstance(self.data, dict):
            data = {}
            for key in self.data:
                data[key] = self.data[key].exportBullets()
            return data
        return None

    def exportElements(self):
        if isinstance(self.data, HTML):
            return self.data.exportElements()
        elif isinstance(self.data, dict):
            data = {}
            for key in self.data:
                data[key] = self.data[key].exportElements()
            return data
        return None

    def export(self):
        if isinstance(self.data, HTML):
            return self.data.export()
        elif isinstance(self.data, dict):
            data = {}
            for key in self.data:
                data[key] = self.data[key].export()
            return data
        return None
    
    def exportScripts(self):
        if isinstance(self.data, HTML):
            return self.data.exportScripts()
        elif isinstance(self.data, dict):
            data = {}
            for key in self.data:
                data[key] = self.data[key].exportScripts()
            return data
        return None

class Content:
    def __init__(self, popup:int=None, voice:int=None, text:MText=None, image:MText=None, src:MText=None, videoType:str=None, \
                 magnify:bool=None, caption:MText=None, fontSize:Union[str, int]=None, fontColor:str=None, colsPerRow:int=None, border:str=None, \
                 rect:list=None, question:MText=None, options:MList=None, answer:Union[str, MList]=None, html:MHTML=None, type:str=None):
        self.popup = popup
        self.voice = voice
        self.text = MText(text) if text !=None else None
        self.image = MText(image) if image !=None else None
        self.src = MText(src) if src!=None else None
        self.videoType = videoType
        self.magnify = magnify
        self.caption = MText(caption) if caption!=None else None
        self.fontSize = fontSize if (isinstance(fontSize, str) and fontSize.endswith("px")) else \
            str(fontSize)+"px" if isinstance(fontSize, int) else None
        self.fontColor = fontColor
        self.colsPerRow = colsPerRow
        self.border = border
        self.rect = rect[:4] if (isinstance(rect, list) and len(rect)>=4) else None
        self.question = MText(question) if question!=None else None
        self.options = MList(options) if options!=None else None
        self.answer = MList(answer) if answer!=None else None
        self.html = html
        self.type = type

    @staticmethod
    def load(object):
        if isinstance(object, dict):
            return Content(
                popup = object.get("popup", None),
                voice = object.get("voice", None),
                text = MText(object["text"]) if object.get("text", None) != None else None,
                image = MText(object["image"]) if object.get("image", None) != None else None,
                src = MText(object["src"]) if object.get("src", None) != None else None,
                videoType = object.get("videoType", None),
                magnify = object.get("magnify", None),
                caption = MText(object["caption"]) if object.get("caption", None) != None else None,
                fontSize = object.get("fontSize", None),
                fontColor = object.get("fontColor", None),
                colsPerRow = object.get("colsPerRow", None),
                border = object.get("border", None),
                rect = object.get("rect", None),
                question = MText(object["question"]) if object.get("question", None) != None else None,
                options = MList(object["options"]) if object.get("options", None) != None else None,
                answer = MList(object["answer"]) if object.get("answer", None) != None else None,
                html = MHTML.loadFromText(MText(object["html"])) if object.get("html", None) != None else None,
                type = object.get("type", None)
            )
        return None

    def copy(self):
        return copy.deepcopy(self)

    def export(self):
        data = {}
        if self.popup!=None:
            data["popup"] = self.popup
        if self.voice!=None:
            data["voice"] = self.voice
        if self.text!=None and self.text.export()!=None:
            data["text"] = self.text.export()
        if self.image!=None and self.image.export()!=None:
            data["image"] = self.image.export()
        if self.src!=None and self.src.export()!=None:
            data["src"] = self.src.export()
        if self.videoType!=None:
            data["videoType"] = self.videoType
        if self.magnify==True:
            data["magnify"] = self.magnify
        if self.caption!=None and self.caption.export()!=None:
            data["caption"] = self.caption.export()
        if self.fontSize!=None:
            data["fontSize"] = self.fontSize
        if self.fontColor!=None:
            data["fontColor"] = self.fontColor
        if self.colsPerRow!=None:
            data["colsPerRow"] = self.colsPerRow
        if self.border!=None:
            data["border"] = self.border
        if self.rect!=None:
            data["rect"] = self.rect
        if self.question!=None and self.question.export()!=None:
            data["question"] = self.question.export()
        if self.options!=None and self.options.export()!=None:
            data["options"] = self.options.export()
        if self.answer!=None and self.answer.export()!=None:
            data["answer"] = self.answer.export()
        if self.html!=None and self.html.export()!=None:
            data["html"] = self.html.export()
        if self.type!=None:
            data["type"] = self.type

        if len(data) > 0:
            return data
        
        return None

class Board:
    def __init__(self, content:Content=None, type:str=None, rect:list=None, contentList:list=None):
        self.content=content if isinstance(content, Content) else Content()
        self.type=type
        self.rect=rect[:4] if (isinstance(rect, list) and len(rect)>=4) else None
        self.contentList = copy.deepcopy(contentList) if isinstance(contentList, list) else []

    @staticmethod
    def load(object):
        if isinstance(object, dict) and object.get("content", None) != None:
            contentList = []
            if isinstance(object.get("contentList", None), list):
                for content in object["contentList"]:
                    contentList.append(Content.load(content))
            return Board(
                content = Content.load(object["content"]),
                type = object["type"] \
                    if object.get("type", None)!=None \
                    else (object["content"].get("type", None) \
                        if isinstance(object["content"], dict) \
                        else None),
                rect = object["rect"] \
                    if object.get("rect", None)!=None \
                    else (object["content"].get("rect", None) \
                        if isinstance(object["content"], dict) \
                        else None),
                contentList = contentList if len(contentList)>0 else None
            )
        return Board()
        
    def copy(self):
        return copy.deepcopy(self)

    def export(self):
        data = {}

        if isinstance(self.content, Content) and self.content.export()!=None:
            data["content"] = self.content.export()
        if self.type!=None:
            data["type"] = self.type
        if self.rect!=None:
            data["rect"] = self.rect
        if self.contentList!=None and len(self.contentList) > 0:
            data["contentList"] = []
            for i, content in enumerate(self.contentList):
                if isinstance(content, Content) and content.export() != None:
                    data["contentList"].append(content.export())
                else:
                    print(f"Invalid Content instance {content} at index {i}")
        return data
    
class Scene:
    def __init__(self, value:str=None, index:str=None, bgColor:str=None):
        self.value = value
        self.index = index
        self.bgColor = bgColor

    @staticmethod
    def load(object):
        if isinstance(object, str):
            return Scene(value = object)
        elif isinstance(object, dict):
            return Scene(
                index = object.get("index", None),
                bgColor = object.get("bgColor", None)
                )
        else:
            return Scene()

    def copy(self):
        return copy.deepcopy(self)
    
    def export(self):
        result = ""
        if isinstance(self.value, str):
            result = self.value
        else:
            data = {}
            if isinstance(self.index, str) and len(self.index) > 0:
                data["index"] = self.index
            if isinstance(self.bgColor, str) and len(self.bgColor) > 0:
                data["bgColor"] = self.bgColor
            if len(data) > 0:
                result = data
    
        return result

class Script:
    def __init__(self, subscript:MText=None, sound:str=None, narrator:str=None, alternative:MText=None, languages:list=None):
        self.subscript = MText(subscript) if subscript!=None else None
        self.sound = sound
        self.narrator = narrator
        self.alternative = MText(alternative) if alternative!=None else None
        self._languages = []
        if isinstance(languages, list) or isinstance(languages, tuple):
            for language in languages:
                if isinstance(language, str) and len(language) > 0:
                    self._languages.append(language)
        elif isinstance(languages, str) and len(languages) > 0:
            self._languages = [languages]
        
    def copy(self):
        return copy.deepcopy(self)

    def reset2test(self, newNarrator=None):
        assert (newNarrator in VISIBLE_ACTORS or newNarrator in INVISIBLE_ACTORS) \
            or newNarrator == None
        if self.sound != None and isinstance(self.sound, str) and len(self.sound) > 0:
            self.sound = switch_to_test_path(self.sound)
            self.narrator = newNarrator if newNarrator != None else self.narrator
            self.languages = None                

    def export(self):
        data = {}
        if isinstance(self.subscript, MText) and self.subscript.export() != None:
            data["subscript"] = self.subscript.export()
        else:
            return None

        if self.sound != None:
            data["sound"] = self.sound
        if self.narrator != None:
            data["narrator"] = self.narrator
        if isinstance(self.alternative, MText) and self.alternative.export() != None:
            data["alternative"] = self.alternative.export()
        if isinstance(self._languages, list) and len(self._languages) > 0:
            data["languages"] = self._languages

        return data

class Interaction:
    def __init__(self, start="", duration="", actorId=None, content:Content=None, figure=None, \
                 position=None, transform=None, onResult=None, onPoster=None, type=None):
        self.start = start
        self.duration = duration
        self.onResult = onResult
        self.onPoster = onPoster
        self.actorId = actorId
        self.figure = figure
        self.position = position
        self.transform = transform
        self.content = content if isinstance(content, Content) else Content()
        self.type = type

    def copy(self):
        return copy.deepcopy(self)
    
    def merge(self, interaction):
        updated = self.copy()
        if isinstance(interaction, Interaction):
            updated.start = interaction.start if interaction.start != "" else updated.start
            updated.duration = interaction.duration if interaction.duration != "" else updated.duration
            updated.onResult = interaction.onResult if interaction.onResult != None else updated.onResult
            updated.onPoster = interaction.onPoster if interaction.onPoster != None else updated.onPoster
            updated.actorId = interaction.actorId if interaction.actorId != None else updated.actorId
            updated.figure = interaction.figure if interaction.figure != None else updated.figure
            updated.position = interaction.position if interaction.position != None else updated.position
            updated.transform = interaction.transform if interaction.transform != None else updated.transform
            updated.content = interaction.content if interaction.content.export() != None else updated.content
            updated.type = interaction.type if interaction.type != None else updated.type

        return updated
    
    def export(self):
        data = {}
        data["start"] = self.start
        data["duration"] = self.duration
        if isinstance(self.content, Content) and self.content.export()!=None:
            data["content"] = self.content.export()
        if self.onResult != None:
            data["onResult"] = self.onResult
        if self.onPoster != None:
            data["onPoster"] = self.onPoster
        if self.position != None and isinstance(self.position, list):
            data["position"] = self.position
        if self.transform != None and isinstance(self.transform, str) \
            and len(self.transform) > 0:
            data["transform"] = self.transform
        if self.figure != None:
            data["figure"] = self.figure
        if self.actorId != None:
            data["actor"] = self.actorId
        if self.type != None:
            data["type"] = self.type

        if len(data) > 2:
            return data
        else:
            return None

# default interaction with actor posture
class PostureInteraction(Interaction):
    def __init__(self, actorId=-1, figure=None, position=None, transform=None):
        super().__init__(type="motion", actorId=actorId, figure=figure, \
                            position=position, transform=transform)
        
class Event:
    def __init__(self, id=None, scene:Scene=None, board:Board=None, objects:list=None, interactions:list=None):
        self.id = id
        self.scene = scene.copy()
        self.board = board.copy()
        self.objects = [actor.copy() for actor in self.objects if isinstance(actor, Actor)]
        self.interactions = [interaction.copy() for interaction in self.interactions if isinstance(interaction, Interaction)]
    
    def export(self):
        data = {}
        if self.id != None:
            data["id"] = self.id
        if isinstance(self.scene, Scene):
            data["scene"] = self.scene.export()
        if isinstance(self.board, Board):
            data["board"] = self.board.export()
        if isinstance(self.objects, list):
            data["objects"] = [actor.export() for actor in self.objects if isinstance(actor, Actor)]
        if isinstance(self.interactions, list):
            data["interactions"] = [interaction.export() for interaction in self.interactions if isinstance(interaction, Interaction)]
        
        if len(data) > 0:
            return data
        else:
            None

class Actor:
    def __init__(self, name):
        if name in (VISIBLE_ACTORS+INVISIBLE_ACTORS+SCENARIO_ACTORS):
            self.name = name
        elif isinstance(name, str) and name.lower() in ('eily', 'eilly'):
            self.name = 'eilly'
        else:
            self.name = None
    
    @staticmethod
    def load(object):
        if isinstance(object, dict):
            return Actor(object.get("name", None))
        return None

    def match(self, name):
        return self.name!=None \
            and name!=None \
            and (self.name == name \
                or (isinstance(self.name, str) and self.name.lower() in ('eily', 'eilly') \
                and isinstance(name, str) and name.lower() in ('eily', 'eilly')))
    
    def category(self):
        if isinstance(self.name, str):
            if self.name.lower() in VISIBLE_ACTORS:
                return VISIBLE
            elif self.name.lower() in INVISIBLE_ACTORS:
                return INVISIBLE
            elif self.name.lower() in SCENARIO_ACTORS:
                return SCENARIO
        return None

    def export(self):
        data = {}
        if self.name != None:
            data["name"] = self.name
        
        if len(data) > 0:
            return data
        return None