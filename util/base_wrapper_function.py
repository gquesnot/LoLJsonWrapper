from my_dataenum.config_index import ConfigIndex


def valToStr(val):
    return val if isinstance(val, str) else str(val)


def getClassAsKeyClass(config, elem, key=None):
    myClass = config.class_.from_dict(elem)

    if myClass is not None:
        if config.configIndex == ConfigIndex.ID:
            key = valToStr(myClass.id)
        elif config.configIndex == ConfigIndex.NAME:
            key = valToStr(myClass.name)
        elif config.configIndex == ConfigIndex.KEY:
            key = valToStr(key)
    else:
        return None, None
    return key, myClass


def getItemsNameAsUrl(myDic):
    return [item['name'].replace(" ", "_") for k, item in myDic.items()]


def withoutDataDict(datas):
    if isinstance(datas, dict):
        if "data" in datas.keys():
            datas = datas['data']
    return datas
