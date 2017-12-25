#coding=utf-8

import requests

# rep = requests.post('http://192.168.4.221:8283/api/flow/socialization',
#               data={
#                   'id': '4110582f08a241bca7bd94ace329db3b'
#               })
# print rep.content

# rep = requests.get('http://192.168.4.221:8283/api/flow/getmutualflow')
# print rep.content

# rep = requests.get('http://192.168.4.221:8283/api/fs/listbydirid/200010035470499')
# print rep.content

# rep = requests.post('http://192.168.4.221:8283/api/fs/listinput',
#                     data={
#                         'dirid': '200010035469342'
#                     })
# print rep.content

# rep = requests.get('http://192.168.4.221:8283/api/fs/listbydirid/200010035470499')
# print rep.content

# rep = requests.get('http://192.168.4.213:8283/api/fs/listbydirid/200010035468331')
# print rep.content

# import flask
# rep = requests.post('http://192.168.4.213:8283/api/fs/listinput',
#                     data={
#                         'dirid': '200010035468331'
#                     })
# print rep.content

# rep = requests.post('http://192.168.4.221:8283/api/task/querybyargs',
#                     data={
#                         'sortName': 'endTime',
#                         'sortOrder': 'desc',
#                         'pageSize': 10,
#                         'pageNumber': 1
#                     })
# print rep.content


# rep = requests.get('http://192.168.4.221:8283/api/fs/listbydirid/200010035482406')
# print rep.content
# /api/fs/listbydirid/<id>
# 200010035482406

rep = requests.get('http://192.168.4.221:8283/api/flow/01b0c09b7cb943949919ed43c63144a8')
print rep.content


# url = 'http://192.168.4.221:8283/api/fs/listioput/db7c18d0bcdb4daca0561cc281203b9a'
# rep = requests.get(url)
# print rep.content