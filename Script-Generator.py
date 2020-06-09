import json
import pprint
import csv
import math
import cmath
import copy

json_open = open('./sample.json', 'r')
j = json.load(json_open)

print("sample.jsonを読み込みました")

csv_file = open("./input.csv", "r",encoding="utf-8-sig")
c = csv.DictReader(csv_file)

points = []

for row in c:
    points.append(row)

n = len(points)

for i in range(n-1):
    new_j = copy.deepcopy(j["Movements"][0])
    j["Movements"].append(new_j)

for i,p in enumerate(points):
    x = float(p['X'])
    y = float(p['Y'])
    z = float(p['Z'])
    duration = float(p['Duration'])
    j["Movements"][i]["Duration"] = duration
    j["Movements"][i]["StartPos"]["x"] = x
    j["Movements"][i]["StartPos"]["y"] = y
    j["Movements"][i]["StartPos"]["z"] = z
    j["Movements"][i-1]["EndPos"]["x"] = x
    j["Movements"][i-1]["EndPos"]["y"] = y
    j["Movements"][i-1]["EndPos"]["z"] = z
    y -= 1.5
    rad = math.atan2(x,z)
    deg = 270 - math.degrees(rad)
    if x == 0 and y == 0:
        deg = 0
    j["Movements"][i]["StartRot"]["y"] = deg 
    j["Movements"][i-1]["EndRot"]["y"] = deg 
    d = math.sqrt(x*x + z*z)
    rad2 = math.atan2(y,d)
    deg2 = math.degrees(rad2)
    j["Movements"][i]["StartRot"]["x"] = deg2 
    j["Movements"][i-1]["EndRot"]["x"] = deg2

pprint.pprint(j)

with open('output.json', 'w') as f:
    json.dump(j, f, indent=4)

print("作業を完了しました")
end = input()