def valToStr(val):
    return val if isinstance(val, str) else str(val)


def getItemsNameAsUrl(myDic):
    return [item['name'].replace(" ", "_") for k, item in myDic.items()]


def withoutDataDict(datas):
    if isinstance(datas, dict):
        if "data" in datas.keys():
            datas = datas['data']
    return datas
