#!/usr/bin/env python

import os
import json
from xml.dom import minidom

root='input/eyeos'
startingId = 0
startingPermissionId = 0
users = []
permissions = []

if os.path.isfile('input/symbiose/users.json'):
	print('Info: populating an existing user database')
	inputUsersFile = open('input/symbiose/users.json')
	users = json.load(inputUsersFile)

	for userData in users:
		if userData['id'] + 1 > startingId:
			startingId = userData['id'] + 1

if os.path.isfile('input/symbiose/users_permissions.json'):
	print('Info: populating an existing permissions database')
	inputPermissionsFile = open('input/symbiose/users_permissions.json')
	permissions = json.load(inputPermissionsFile)

	for permData in permissions:
		if permData['id'] + 1 > startingPermissionId:
			startingPermissionId = permData['id'] + 1

userAttributes = {
	'username': 'username',
	'password': 'password',
	'email': 'email',
	'fullname': 'realname',
	'disabled': 'disabled'
}
defaultPermissions = ["file.user.read","file.user.write","user.self.edit"]

userFiles = os.listdir(root)

i = 0
j = 0
for basename in userFiles:
	xmldoc = minidom.parse(root+'/'+basename)

	attrs = {}

	for eyeosAttrName in userAttributes:
		symbioseAttrName = userAttributes[eyeosAttrName]

		els = xmldoc.getElementsByTagName(eyeosAttrName)

		if len(els) == 0:
			continue

		childs = els[0].childNodes

		if len(childs) == 0:
			continue

		attrs[symbioseAttrName] = childs[0].nodeValue

	if 'username' not in attrs:
		print('Warning: skipping one user without username')
		continue
	if 'password' not in attrs:
		print('Warning: skipping user "'+attrs['username']+'" without password')
		continue
	if 'email' not in attrs:
		print('Info: generating a fake e-mail adress for user "'+attrs['username']+'"')
		attrs['email'] = attrs['username']+'@example.com'
	
	if 'realname' not in attrs:
		attrs['realname'] = attrs['username']
	if 'disabled' not in attrs:
		attrs['disabled'] = False
		continue
	if attrs['disabled'] == '1':
		attrs['disabled'] = True
	else:
		attrs['disabled'] = False

	attrs['id'] = i + startingId
	attrs['password'] = 'eyeos:'+attrs['password']

	users.append(attrs)

	for perm in defaultPermissions:
		permissions.append({
			'id': j + startingPermissionId,
			'userId': attrs['id'],
			'name': perm
		})

		j += 1

	i += 1

if not os.path.isdir('output'):
	os.mkdir('output')

print(str(len(users))+' users and '+str(len(permissions))+' permissions imported.')
print('Writing files...')

outputUsersFile = open('output/users.json', 'w+')
outputPermissionsFile = open('output/users_permissions.json', 'w+')

json.dump(users, outputUsersFile)
json.dump(permissions, outputPermissionsFile)

print('Done. You can now move files in output/ to /var/lib/jsondb/core/')