import json
import os

def rewardsLogger(textmap, rewardID):
    files = {"RewardExcelConfigData": {},
            "MaterialExcelConfigData": {}}

    for file in files:
        with open(os.path.join(os.path.dirname(__file__), f'../data/Excel/{file}.json')) as json_file:
            files[file] = json.load(json_file)
    
    return rewardsFormatter(textmap, files, rewardID)

def rewardsFormatter(textmap, files, rewardID):

    rewardData = list(filter(lambda x: x['rewardId'] == rewardID, files['RewardExcelConfigData']))
    if len(rewardData) == 0:
        return ''
    
    rewardData = rewardData[0]
    # Removing empty dicts in list
    rewardList = list(filter(None, rewardData["rewardItemList"]))
    text = ''
    for reward in rewardList:
        materialData = list(filter(lambda x: x['id'] == reward["itemId"], files['MaterialExcelConfigData']))
        # Bugfix for questID=307 which rewards a weapon
        if len(materialData) == 0:
            weapon = json.load(open(os.path.join(os.path.dirname(__file__), f'../data/Excel/WeaponExcelConfigData.json')))
            weaponreward = list(filter(lambda x: x['id'] == reward["itemId"], weapon))
            # Bugfix for questID=21003 which rewards an artifact
            if len(weaponreward) == 0:
                artifact = json.load(open(os.path.join(os.path.dirname(__file__), f'../data/Excel/ReliquaryExcelConfigData.json')))
                artifactreward = list(filter(lambda x: x['id'] == reward["itemId"], artifact))
                name = artifactreward[0]['nameTextMapHash']
            else:
                name = weaponreward[0]["nameTextMapHash"]
        else:
            name = materialData[0]["nameTextMapHash"]
        text += f'{textmap[str(name)]} x{reward["itemCount"]}, '

    return text[:-2]