import json, re, os
from selenium.common.exceptions import NoSuchElementException

def optionalChaining(data, keys):
    for key in keys:
        try:
            data = data.get(key)
        except AttributeError as ae:
            return None
    return data

def readFromFile(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as file:
        json_content = json.load(file)
    return json_content

def saveToFile(json_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_content, file, ensure_ascii=False, indent=4)

def getElementText(driver, by, value):
    try:
        element = driver.find_element(by, value).text
        return element
    except NoSuchElementException as nsee:
        print('Null element')
        pass
    return None

def getElements(driver, by, value):
    try:
        element = driver.find_elements(by, value)
        return element
    except NoSuchElementException as nsee:
        print('Null element')
        pass
    return None

def getOnlyNumbers(str, i=0):
    try:
        numbers = [int(s) for s in re.findall(r'\b\d+\b', str)]
        return numbers[i]
    except IndexError as ie:
        pass
    return None