import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from PIL import Image

VISIBLE_ACTORS=("boy", "girl", "eily", "eilly")
INVISIBLE_ACTORS=("", "M", "F")
SCENARIO_ACTORS=("ending", "exam", "concentrak", "notes")

def remove_emojis(text):
    emojiPattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F926-\U0001F991"
                    "]+", flags = re.UNICODE)
    return re.sub(emojiPattern, '', text)

def has_chinese_char(text):
  """Checks if a string contains at least one Chinese character.

  Args:
      text: The string to be checked.

  Returns:
      True if the string contains at least one Chinese character, False otherwise.
  """
  # Check if any character in the string falls within the Unicode range of Chinese characters
  return any(u'\u4e00' <= char <= u'\u9fff' for char in text)

def update_object(original, update, default_locale=None):
    """Updates the original object from the update object.

    Args:
        original: The object to be updated.
        update: The object containing updates.

    Returns:
        A new object with the updates applied. Ignore if update is None.
    """
    if update == None:
        return original
    
    if isinstance(update, dict):
        return {
            **(original \
                if isinstance(original, dict) \
                else ({} if original == None else {default_locale: original})), \
            **{key: update[key] for key in update}
        }
    elif isinstance(original, dict) and default_locale != None:
        original[default_locale] = update
    else:
        original = update
    return original

def get_actors(objects):
    assert isinstance(objects, list)
    actor = None
    narrator = None
    defaultObject = None
    actorId = -1
    narratorId = -1
    defaultObjectId = -1
    for i, object in enumerate(objects):
        if object.get("name", None) in VISIBLE_ACTORS:
            actor = object["name"]
            actorId = i
        elif object.get("name", None) in INVISIBLE_ACTORS:
            narrator = object["name"]
            narratorId = i
        else:
            defaultObject = object.get("name", None)
            defaultObjectId = i
    return actor, actorId, narrator, narratorId, defaultObject, defaultObjectId

def update_visible_actor(objects, actor):
    assert isinstance(objects, list) and actor in VISIBLE_ACTORS
    if len(objects) == 0:
        objects.append({"name": actor})
    else:
        for i, object in enumerate(objects):
            if object["name"] in VISIBLE_ACTORS:
                objects[i]["name"] = actor

def update_invisible_actor(objects, actor):
    assert isinstance(objects, list) and actor in INVISIBLE_ACTORS
    if len(objects) == 0:
        objects.append({"name": actor})
    else:
        for i, object in enumerate(objects):
            if object["name"] in INVISIBLE_ACTORS:
                objects[i]["name"] = actor

def switch_to_test_path(path):
    if path.startswith("/story/"):
        return "/test/" + path[len("/story/"):]
    else:
        return path

def reset_voices_to_test(scriptList, oldNarrator, newNarrator):
    assert isinstance(scriptList, list) \
        and (oldNarrator in VISIBLE_ACTORS or oldNarrator in INVISIBLE_ACTORS) \
        and (newNarrator in VISIBLE_ACTORS or newNarrator in INVISIBLE_ACTORS)
    for i, script in enumerate(scriptList):
        if "narrator" in script and script["narrator"] == oldNarrator and "sound" in script \
            and isinstance(script["sound"], str) and len(script["sound"]) > 0:
            scriptList[i]["narrator"] = newNarrator
            scriptList[i]["sound"] = switch_to_test_path(script["sound"])
            scriptList[i].pop("languages", None)

def get_image_from_board(boardObject):
    image = None
    rect = None
    caption = None
    if "content" in boardObject:
        rect = boardObject["rect"]
        image = boardObject["content"].get("image", None)
        video = boardObject["content"].get("src", None)
        videoType = boardObject["content"].get("videoType", None)
        caption = boardObject["content"].get("caption", None)
    return rect, image, video, videoType, caption

def get_html_from_board(boardObject):
    html = None
    rect = boardObject.get("rect", None)
    if "content" in boardObject:
        html = boardObject["content"].get("html", None)
    return rect, html

def get_question_from_board(boardObject):
    question = None
    options = None
    answer = None
    rect = None
    colsPerRow = 1
    fontSize = 20
    fontColor = "white"
    rect = boardObject.get("rect", rect)
    if "content" in boardObject:
        question = boardObject["content"].get("question", question)
        options = boardObject["content"].get("options", options)
        answer = boardObject["content"].get("answer", answer)
        colsPerRow = boardObject["content"].get("colsPerRow", colsPerRow)
        fontSize = boardObject["content"].get("fontSize", fontSize)
        fontColor = boardObject["content"].get("fontColor", fontColor)
    return rect, question, options, answer, colsPerRow, fontSize, fontColor

def get_subscript_from_interaction(interactionObject):
    actor = -1
    voice = -1
    figure = -1
    text = None
    duration = ""
    if "content" in interactionObject:
        text = interactionObject["content"].get("text", text)
        voice = interactionObject["content"].get("voice", voice)
        actor = interactionObject.get("actor", actor)
        figure = interactionObject.get("figure", figure)
        duration = interactionObject.get("duration", duration)
    return actor, figure, text, voice, duration

def get_bullets_from_html(html:str):
    # Define a pattern to match the content within list items (ul or li tags)
    pattern = r"<(ul|li)>(.*?)</(ul|li)>"

    # Extract content from html using findall
    matches = re.findall(pattern, html, flags=re.DOTALL)

    extracted = []
    if matches:
        # Remove tags using re.sub
        extracted = [re.sub(r"<[^>]+>", "", match[1]) for match in matches]
    return extracted

# Extract all text recursively, excluding script and style tags
def retrieve_element_text(element):
    text_object_list = []
    if element.name:
        for child in element.children:
            text_object_list.extend(retrieve_element_text(child))
    elif element.string:
        text_object_list.append({element.parent.name: element.string.strip()})  # Add current element's text
    return text_object_list

def extract_html_elements(html_text:str):
    soup = BeautifulSoup(html_text, "lxml")
    
    # Extract all text into a list
    extracted_text_object_list = retrieve_element_text(soup)
    
    # Optional: Flatten the list of lists (if nested due to structure)
    if any(isinstance(item, list) for item in extracted_text_object_list):
        extracted_text_object_list = [item for sublist in extracted_text_object_list for item in sublist]

    html_template = html_text
    for string in extracted_text_object_list:
        key = next(iter(string), None)
        if key != None:
            html_template = html_template.replace(">"+string[key]+"<", ">{"+key+"}<")
    
    # Regular expression pattern to match any number of continuous <li> elements
    # Explanation of the pattern:
    # - "<li>(.*?)</li>": Matches the first <li> tag and its content (non-greedy)
    # - "(?:<li>(.*?)</li>)*": Matches zero or more repetitions of subsequent <li> tags and their content (non-greedy)
    pattern = r"<li>(.*?)</li>(?:<li>(.*?)</li>)*"
        
    # Replace each group with a single '{}'
    html_template = re.sub(pattern, "<li>{li}</li>", html_template)

    return extracted_text_object_list, html_template

def retrieve_svg_size(image_path):
    # Load the SVG file
    tree = ET.parse(image_path)
    root = tree.getroot()

    # Extract attributes from the <svg> tag
    width = root.get("width", 0)  # Get the width attribute
    height = root.get("height", 0)  # Get the height attribute
    viewBox = root.get("viewBox", "0, 0, 0, 0")  # Get the viewBox attribute

    split_pattern = r"[ ,]+"

    return [int(width), int(height)], [
        int(float(num)) for num in re.split(split_pattern, viewBox)
    ]

def retrieve_pixel_size(image_path):
    width = height = 0
    try:
        # Open the image using the Python Imaging Library (PIL)
        image = Image.open(image_path)

        # Get the width and height of the image in pixels
        width, height = image.size

        image.close()
    except OSError as e:
        print(f"Error opening image: {e}")

    # Return the width and height as a tuple
    return width, height

def get_image_size(file_path):
    width = height = 0
    try:
        if ".svg" in file_path[-4:]:
            dim2, dim4 = retrieve_svg_size(file_path)
            if dim2 == [0, 0]:
                width = dim4[2]
                height = dim4[3]
            else:
                width = dim2[0]
                height = dim2[1]
        elif (
            ".jpg" in file_path[-4:]
            or ".jpeg" in file_path[-5:]
            or ".png" in file_path[-4:]
            or ".gif" in file_path[-4:]
        ):
            width, height = retrieve_pixel_size(file_path)
    except:
        print("Retrieve image size error for", file_path)
    return width, height

def is_valid_http_url(url_str):
    return url_str.startswith("https://") or url_str.startswith("http://")