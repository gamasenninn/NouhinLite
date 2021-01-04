import requests
import json

'''
print("\n------Get Main Menu ----")

response = requests.get("http://localhost:8080")
print(response.text[:100])

print("\n------API Get /api/納品 ----")

response = requests.get("http://localhost:9090/api/納品")
print(response.text)

print("\n------API Get /api/納品明細 ----")

response = requests.get("http://localhost:8080/api/納品明細")
print(response.text)
'''
'''
print("\n------API Post /api/納品 ----")
data = {'納品日': "2021/01/03",'納品先': "XYZ商店",'担当者': "小野",'摘要': "POST"}
response = requests.post(
    'http://localhost:8080/api/納品',
    json.dumps(data),
    headers={'Content-Type': 'application/json'})
print(response.text)
'''

print("\n------API Put /api/納品 ----")
data = {'ID':1,'納品日': "2021/01/03",'納品先': "PUT商店",'担当者': "小野",'摘要': "PUT"}
response = requests.put(
    'http://localhost:9090/api/納品',
    json.dumps(data),
    headers={'Content-Type': 'application/json'}
    )
print(response.text)


'''
print("\n------API Delete /api/納品 ----")
response = requests.delete(
    'http://localhost:8080/api/納品/6',
    headers={'Content-Type': 'application/json'})
print(response.text)
'''    
