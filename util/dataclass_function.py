import re


def mapDataClassFields(data, toMap):
    for k, v in toMap.items():
        myData = data[k]
        if v['list']:
            if isinstance(myData, dict):
                myData = [val | {"id": key} for key, val in myData.items()]

            myData = [mapField(v['type'], val) for val in myData]
        else:
            myData = mapField(v['type'], myData)
        data[k] = myData

    return data

def mapField(Class, data):
    return Class.from_dict(data).to_dict()

def ownCapitalize(string):
    return re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), string, 1)


def strToFloatList(string, separator="/"):

    return [float(v) for v in string.split(separator)]