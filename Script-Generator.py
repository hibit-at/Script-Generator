import json
import pprint
import csv
import cmath
import math
import copy
import os

json_open = open('./template.json', 'r')
j = json.load(json_open)

print("template.jsonを読み込みました")

csv_file = open("./input.csv", "r",encoding="utf-8-sig")
c = csv.DictReader(csv_file)

points = []

for row in c:
    points.append(row)

n = len(points)

bpm = points[0]["marker"]

for i in range(n-1):
    new_j = copy.deepcopy(j["Movements"][0])
    j["Movements"].append(new_j)

for i,p in enumerate(points):
    #パラメータ抽出
    sX = float(p['sX'])
    sY = float(p['sY'])
    sZ = float(p['sZ'])
    sRZ = float(p['sRZ'])
    eX = float(p['eX'])
    eY = float(p['eY'])
    eZ = float(p['eZ'])
    eRZ = float(p['eRZ'])
    Ease = int(p['Ease'])
    sOffX = float(p['sOffX'])
    sOffY = float(p['sOffY'])
    eOffX = float(p['eOffX'])
    eOffY = float(p['eOffY'])
    duration = float(p['Duration'])

    #位置のセット
    j["Movements"][i]["Duration"] = duration*60/float(bpm)
    j["Movements"][i]["StartPos"]["x"] = sX
    j["Movements"][i]["StartPos"]["y"] = sY
    j["Movements"][i]["StartPos"]["z"] = sZ
    j["Movements"][i]["EndPos"]["x"] = eX
    j["Movements"][i]["EndPos"]["y"] = eY
    j["Movements"][i]["EndPos"]["z"] = eZ

    sX -= sOffX
    eX -= eOffX
    sY -= (1.5 + sOffY)
    eY -= (1.5 + eOffY)

    #角度の計算1
    c = complex(-sX,-sZ)
    rad = cmath.phase(c)
    deg = -math.degrees(rad)+90
    if sX == 0 and sZ == 0:
        deg = 0
    j["Movements"][i]["StartRot"]["y"] = deg 
    print(deg)
    
    c = complex(-eX,-eZ)
    rad = cmath.phase(c)
    deg = -math.degrees(rad)+90
    if eX == 0 and eZ == 0:
        deg = 0
    j["Movements"][i]["EndRot"]["y"] = deg

    #角度の計算2 
    c2 = complex(abs(c),sY)
    rad2 = cmath.phase(c2)
    deg2 = math.degrees(rad2)
    j["Movements"][i]["StartRot"]["x"] = deg2

    c2 = complex(abs(c),eY)
    rad2 = cmath.phase(c2)
    deg2 = math.degrees(rad2)
    print(-deg2)
    j["Movements"][i]["EndRot"]["x"] = deg2

    #Easeの判定
    if Ease == 1:
        j["Movements"][i]["EaseTransition"] = "true"
    else:
        j["Movements"][i]["EaseTransition"] = "false"

    #z軸回りの角度
    j["Movements"][i]["StartRot"]["z"] = sRZ
    j["Movements"][i]["EndRot"]["z"] = eRZ

pprint.pprint(j)

with open('output.json', 'w') as f:
    json.dump(j, f, indent=4)

print("作業を完了しました")
end = input()