#!/usr/bin/python
# source: 
# https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html#id3

import gitlab
import time
import os.path

URL = "https://gitlab.com/"
keyfile = open('/mnt/c/Users/GuyPainsky/Documents/Scripts/Cred/Gitlab.com-key.txt', 'r')
PersonalToken = keyfile.read()
gl = gitlab.Gitlab(URL, private_token=PersonalToken)

ExportLocation = '/mnt/c/Temp/GitProj/'

# list all the projects
projects = gl.projects.list(owned=True, all=True)
for project in projects:
    if(os.path.isfile(ExportLocation + project.name + '.tgz')):
        continue
    print('Exporting project: ' + project.name + ' - id: ' + str(project.id))

    # Create the export
#    p = gl.projects.get(my_project)
    export = project.exports.create({})

    # Wait for the 'finished' status
    export.refresh()
    while export.export_status != 'finished':
        time.sleep(60)
        export.refresh()

    # Download the result
    with open(ExportLocation + project.name + '.tgz', 'wb') as f:
        export.download(streamed=True, action=f.write)
