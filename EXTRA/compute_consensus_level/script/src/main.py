import json
from usage.database import Database

from nltk.metrics import masi_distance
from nltk.metrics.agreement import AnnotationTask

db = Database()

tables = [("allia", "alex", 302, 501, 802, 901), ("alex", "nicu", 502, 701, 902, 1001), ("allia", "nicu", 102, 301, 702, 801)]

types = ["commits", "consolidation"]

def extractDataFromDB(lowerLimit, upperLimit, table):
    data = []
    for i in range(lowerLimit, upperLimit + 1):
        db.cursor.execute(f"SELECT e.`name`, c.`commit_id` FROM `cloudformation`.`effects_{type}_{table}` c JOIN `cloudformation`.`effects` e ON e.id = c.effect_id WHERE c.commit_id = {i}")
        if db.cursor.rowcount == 0:
            continue
        codes = []
        for (effectName, _) in db.cursor:
            codes.append(effectName)
        db.connection.commit()
        db.cursor.execute(f"SELECT a.`name`, c.`commit_id` FROM `cloudformation`.`actions_{type}_{table}` c JOIN `cloudformation`.`actions` a ON a.id = c.action_id WHERE c.commit_id = {i}")
        for (actionName, _) in db.cursor:
            codes.append(actionName)
        db.connection.commit()
        db.cursor.execute(f"SELECT p.`name`, c.`commit_id` FROM `cloudformation`.`properties_{type}_{table}` c JOIN `cloudformation`.`properties` p ON p.id = c.property_id WHERE c.commit_id = {i}")
        for (propertyName, _) in db.cursor:
            codes.append(propertyName)
        db.connection.commit()
        if ("cpu" in codes or "ram" in codes):
            if ("instance" not in codes):
                codes.append("instance")
        if ("nat" in codes or "domain" in codes or "vpn" in codes):
            if ("networking" not in codes):
                codes.append("networking")
        data.append({
            'id': f"{i}",
            'codes': codes
        })
        print(f"Commit {i} has been processed from {table}")
    return data

with open ('output/alpha.txt', 'w') as f:
    f.write('')

for table in tables:
    lowerLimitP1, upperLimitP1, lowerLimitP2, upperLimitP2 = table[2], table[3], table[4], table[5]
    table1, table2 = table[0], table[1]
    for type in types:
        data1P1 = extractDataFromDB(lowerLimitP1, upperLimitP1, table1)
        data1P2 = extractDataFromDB(lowerLimitP2, upperLimitP2, table1)
        data2P1 = extractDataFromDB(lowerLimitP1, upperLimitP1, table2)
        data2P2 = extractDataFromDB(lowerLimitP2, upperLimitP2, table2)
        data1 = data1P1 + data1P2
        data2 = data2P1 + data2P2

        data = []
        for (a, b) in zip(data1, data2):
            assert a['id'] == b['id']

            data.append((0, a['id'], frozenset(a['codes'])))
            data.append((1, a['id'], frozenset(b['codes'])))

        task = AnnotationTask(distance=masi_distance)
        task.load_array(data)

        alpha = task.alpha()

        if (type == "commits"):
            with open('output/alpha.txt', 'a') as f:
                f.write(f'Alpha between {table1} and {table2} in {len(data1)} commits computed before consolidation is {alpha:.6f}\n')
            print(f'Alpha between {table1} and {table2} in {len(data1)} commits computed before consolidation is {alpha:.6f}')
        else:
            with open('output/alpha.txt', 'a') as f:
                f.write(f'Alpha between {table1} and {table2} in {len(data1)} commits computed after consolidation is {alpha:.6f}\n')
            print(f'Alpha between {table1} and {table2} in {len(data1)} commits computed after consolidation is {alpha:.6f}')

db.close()
