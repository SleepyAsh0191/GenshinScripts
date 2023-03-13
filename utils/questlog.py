import json
import os
import itertools
from pathlib import Path

import utils.rewards as rewards

hangoutChaptersIDs = [101401, 103201, 103601, 103401]

def batchExtractChapters(textmap, args):
    # Loading all required json files
    files = {"ChapterExcelConfigData": {},  #Chapter
            "MainQuestExcelConfigData": {}, # Main Quest
            "QuestExcelConfigData": {},
            "QuestSummarizationTextExcelConfigData": {}, # Quest summaries
            "TalkExcelConfigData": {},
            "DialogExcelConfigData": {},
            "NpcExcelConfigData": {},     # NPC Names
            "RewardExcelConfigData": {},  # Rewards
            "MaterialExcelConfigData": {}}

    for file in files:
        with open(os.path.join(os.path.dirname(__file__), f'../data/Excel/{file}.json')) as json_file:
            files[file] = json.load(json_file)

    # Skipping Hangout quests, as it has a different configuration
    files["ChapterExcelConfigData"] = list(filter(lambda x:x["id"] not in hangoutChaptersIDs, files["ChapterExcelConfigData"]))

    length = len(files["ChapterExcelConfigData"])

    for count, ch in enumerate(files["ChapterExcelConfigData"]):
        print(f'Chapter progress : {count+1}/{length} [{ch["id"]}]')
        chapter(textmap, ch, files, args)

def batchExtractQuests(textmap, args):
    files = {"MainQuestExcelConfigData": {}, # Main Quest
            "QuestExcelConfigData": {},
            "QuestSummarizationTextExcelConfigData": {}, # Quest summaries
            "TalkExcelConfigData": {},
            "DialogExcelConfigData": {},
            "NpcExcelConfigData": {},     # NPC Names
            "RewardExcelConfigData": {},  # Rewards
            "MaterialExcelConfigData": {}}

    for file in files:
        with open(os.path.join(os.path.dirname(__file__), f'../data/Excel/{file}.json')) as json_file:
            files[file] = json.load(json_file)

    questData = list(filter(lambda x: x if "chapterId" not in x else None, files["MainQuestExcelConfigData"]))
    length = len(questData)

    for count, q in enumerate(questData):
        print(f'Quest progress : {count+1}/{length} [{q["id"]}]')
        quest(textmap, q, files, args)

def chapterLogger(textmap, chapterId, args):
    files = {"ChapterExcelConfigData": {},  # Chapter
            "MainQuestExcelConfigData": {}, # Main Quest
            "QuestExcelConfigData": {},
            "QuestSummarizationTextExcelConfigData": {}, # Quest summaries
            "TalkExcelConfigData": {},
            "DialogExcelConfigData": {},
            "NpcExcelConfigData": {},     # NPC Names
            "RewardExcelConfigData": {},  # Rewards
            "MaterialExcelConfigData": {}}

    for file in files:
        with open(os.path.join(os.path.dirname(__file__), f'../data/Excel/{file}.json')) as json_file:
            files[file] = json.load(json_file)
    
    chapterData = list(filter(lambda x: x['id'] == chapterId, files["ChapterExcelConfigData"]))

    chapter(textmap, chapterData[0], files, args)

def chapter(textmap, ch, files, args):

    filePath = os.path.join(f'res/Chapter/{textmap[str(ch["chapterNum"])]} [{ch["id"]}] - {args.lang}.txt')
    Path("res/Chapter/").mkdir(parents=True, exist_ok=True)

    print(f'File written : {filePath}')
    # These two lines might be used later
    # beginQuest = chapterQuest[0]['BeginQuestId']
    # endQuest = chapterQuest[0]['EndQuestId']
    print(f'{textmap[str(ch["chapterNum"])]} [{ch["id"]}]')
    with open(filePath, 'w', encoding='utf-8') as file:
        file.write(f'{textmap[str(ch["chapterNum"])]}\n\n')
        file.write(f'{textmap[str(ch["chapterTitle"])]}\n\n')
    
    # Searching for the Chapter ID and associated quests
    mainQuests = list(filter(lambda d: (d['chapterId'] == ch['id'] if "chapterId" in d else None), files["MainQuestExcelConfigData"]))
    mainQuests = sorted(mainQuests, key=lambda i: i['id'])

    length = len(mainQuests)

    for current, mq in enumerate(mainQuests):
        print(f'Progress : {current+1}/{length}')
        quest(textmap, mq, files, args, filePath)


def questLogger(textmap, questId, args):
    files = {"MainQuestExcelConfigData": {}, # Main Quest
            "QuestExcelConfigData": {},
            "QuestSummarizationTextExcelConfigData": {}, # Quest summaries
            "TalkExcelConfigData": {},
            "DialogExcelConfigData": {},
            "NpcExcelConfigData": {},     # NPC Names
            "RewardExcelConfigData": {},  #Rewards
            "MaterialExcelConfigData": {}}

    for file in files:
        with open(os.path.join(os.path.dirname(__file__), f'../data/Excel/{file}.json')) as json_file:
            files[file] = json.load(json_file)
    
    mainquest = list(filter(lambda d: d['id'] == questId, files["MainQuestExcelConfigData"]))

    quest(textmap, mainquest[0], files, args)

def quest(textmap, mainquest, files, args, filePath=""):
    #MainQuestExcelConfigData.json -> Contains Quest ID
    #TalkExcelConfigData.json  "QuestId" -> Quest ID in MainQuestExcelConfigData.json (Id)
    #                          "InitDialog" -> Beginning dialog ID in DialogExcelConfigData.json (Id)
                                
    #QuestExcelConfigData.json   "mainId" -> Quest ID in MainQuestExcelConfigData.json (Id)
    #                            "SubId" -> Quest part ID in TalkExcelConfigData.json (Id)

    #DialogExcelConfigData.json   Iterate over NextDialogs [], if there's more than one choice, then the traveler is talking

    #MainQuestExcelConfigData (Id)-> QuestExcelConfigData.json (mainId) -> (SubId) orderby "Order" asc -> TalkExcelConfigData.json (Id) -> (InitDialog) -> DialogExcelConfigData.json (Id) -> for text in NextDialogs[] -> empty then next

    # In "talkRole", if "Type" is "TALK_ROLE_PLAYER" then traveler is talking
    #                else if it's "TALK_ROLE_NPC", then "id" corresponds to "id" in NpcExcelConfigData.json (and then you get the NPC name) 

    # Checking if the file already exists. Useful to not overwrite the file for each quest when the function is called
    textfile = Path(filePath)
    if textfile.is_file():
        openmode = 'a'
    else:
        filePath = os.path.join(f'res/Quest/{textmap["1672777464"]} - {textmap[str(mainquest["title"])]} [{mainquest["id"]}] - {args.lang}.txt')
        Path("res/Quest/").mkdir(parents=True, exist_ok=True)
        if Path(filePath).is_file():    # In order to append to the existing file the new version of the quest
            openmode = 'a'
        else:
            openmode = 'w'

    with open(filePath, openmode, encoding='utf-8') as file:

        file.write(f'Main Quest : {textmap[str(mainquest["title"])]} [{mainquest["id"]}]\n\n')
        file.write(f'{textmap[str(mainquest["descTextMapHash"])]}\n\n')
        # Writing rewards
        text = ''
        for r in mainquest["rewardIdList"]:
            text += rewards.rewardsFormatter(textmap, {"RewardExcelConfigData": files["RewardExcelConfigData"], "MaterialExcelConfigData": files["MaterialExcelConfigData"]}, r) + "\n"
        file.write(f'{textmap["276798818"]} : {text}\n' if len(mainquest["rewardIdList"]) > 0 else "\n")

        print(f'Main Quest : {textmap[str(mainquest["title"])]} [{mainquest["id"]}]')

        quest = list(filter(lambda d: d['mainId'] == mainquest['id'], files["QuestExcelConfigData"]))
        quest = sorted(quest, key=lambda i: i['order'])

        length = len(quest)

        for subcount, q in enumerate(quest):
            # if q['SubId'] >= beginQuest and q['SubId'] <= endQuest:
            print(f'Objective progress : {subcount+1}/{length} [{q["subId"]}]')
            file.write(f'\n--> {textmap[str(q["descTextMapHash"])]}\n\n')

            # Finding a summary of the objective (if exists)
            summary = list(filter(lambda x: x['id'] == q["subId"], files["QuestSummarizationTextExcelConfigData"]))
            if len(summary) == 1:
                file.write(f'{textmap[str(summary[0]["descTextMapHash"])]}\n\n')
            else:
                file.write('\n\n')

            talk = list(filter(lambda d: d['id'] == q['subId'], files["TalkExcelConfigData"]))
            for t in talk:
                dialog = list(filter(lambda d: (d['id'] == t['initDialog'] if 'initDialog' in t else None), files["DialogExcelConfigData"]))
                for d in dialog:
                    # Putting branchID=[0] explicitely, as using list.append() inside could cause problems
                    dialogManager(textmap, d, files, file, [],  0, [0])
                    
        file.write("\n\n================================\n\n")

def dialogManager(textmap, dialog, files, file, IDList=[], branchLevel=0, branchID=[0], branchReturn=False, limitID=-1):
    # Just formatting
    leveling = ' '
    for _ in itertools.repeat(None, branchLevel):
        leveling += '---'
    leveling += ' '

    file.write(f'{str(branchID[branchLevel]) + leveling if branchID[branchLevel] > 0 else ""}[{dialog["id"]}] {characterSearch(dialog, files["NpcExcelConfigData"], textmap)} : {textmap[str(dialog["talkContent"])]}\n')
    IDList.append(dialog['id'])
    
    # Bug resolution : infinite recursion for chapterID=2010, when having the same ID in NextDialog than the current dialog
    # This is actually a problem from the Genshin data, the following lines will resolve this
    if dialog['id'] == 105010427:
        dialog['nextDialogs'] = [105010428,105010429]

    nextDialog = list(filter(lambda f: f['id'] in dialog['nextDialogs'] and f['id'] != dialog['id'], files["DialogExcelConfigData"]))

    if len(nextDialog) == 1:
        # If we're at the last branch nextDialog ID == limitID, then we're at the end of the branch
        if nextDialog[0]['id'] == limitID and branchReturn:
            branchID.pop()
            dialogManager(textmap, nextDialog[0], files, file, IDList, branchLevel-1, branchID, False)
        # In the case of having the next ID as the end of the branch, but there is a branch remaining (ex: Chapter 1 Act 4)
        elif nextDialog[0]['id'] == limitID and not branchReturn:
            return -1
        # If IDs aren't consecutive for the first branch, then the next ID is the end of the branch
        elif nextDialog[0]['id'] != dialog['id'] + 1 and branchID[branchLevel] == 1:
            return nextDialog[0]['id']
        # When quest text go back to the first question (ex questID=309)
        elif dialog["id"] > nextDialog[0]['id'] and nextDialog[0]['id'] in IDList:
            return -1
        # Else we have the normal behaviour
        else:
            return dialogManager(textmap, nextDialog[0], files, file, IDList, branchLevel, branchID, branchReturn, limitID)

    elif len(nextDialog) > 1:
        limitID = -1
        branchID.append(1)
        branchReturn = False
        for i, branch in enumerate(nextDialog):
            if i == 0:  # We get the limit ID
                limitID = dialogManager(textmap, branch, files, file, IDList, branchLevel+1, branchID, branchReturn)
            else:   # And for the others, we stop at the limit ID found
                if branch['id'] not in IDList:
                    if i == len(nextDialog) - 1:
                        branchReturn = True
                    branchID[branchLevel+1] = i+1
                    dialogManager(textmap, branch, files, file, IDList, branchLevel+1, branchID, branchReturn, limitID)
    return -1
        
def characterSearch(dialog, npcexcel, textmap):
    # Bugfix for chapterID=2011; DialogID=111000819 -> missing Type in TalkRole
    if "type" in dialog["talkRole"]:
        if dialog["talkRole"]["type"] == "TALK_ROLE_PLAYER":
            return textmap["4100208827"]
        elif dialog["talkRole"]["type"] == "TALK_ROLE_NPC":
            if dialog["talkRole"]['id'] != "":
                npcname = list(filter(lambda d: d['id'] == int(dialog["talkRole"]["id"]), npcexcel))
                return textmap[str(npcname[0]["nameTextMapHash"])]
            return ""
    elif dialog["talkRole"]["id"] == "":
        if dialog["id"] == 111000819:
            return textmap["4100208827"]
    return "" 