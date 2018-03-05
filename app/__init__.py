#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: entree.app
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

# Import dependencies
import datetime
import io
import os
import re
import shutil
import time
import traceback
import zipfile

from flask import Flask, render_template, url_for
from flask import jsonify, request, redirect, send_file, send_from_directory

from entree.projects import CLASSES, CLASS_LONG_NAMES
from entree.utils import copy_file_structure, create_single_file

__version__ = '1.0'

app = Flask(__name__)

FILEROOT, FILEBASE = os.path.split(__file__)


# Routes
# Main route
@app.route('/')
def home():
    '''Main flask route
    '''
    error = request.args.get('error')
    if error is None:
        error = ''
    return render_template('index.html', project_types=CLASS_LONG_NAMES,
                           error=error)


# form submission route
@app.route('/submit', methods=['POST'])
def submit():
    try:
        fields = sorted(list(request.form.keys()))
        if fields != ['email', 'name', 'projectname', 'projecttype', 'url']:
            raise ValueError('Wrong fields in request')

        # Get data from form
        # Project name and type
        modname = request.form['projectname']

        if not re.match('^[a-zA-Z][a-zA-Z0-9_]*$', modname):
            return redirect(url_for('home', error='Wrong format for '
                                                  'project name'))

        project_type = request.form['projecttype']
        if project_type not in CLASS_LONG_NAMES:
            return redirect(url_for('home', error='Project type unsupported'))

        # Author information
        config = {}
        config['author'] = request.form['name']

        if '@' in request.form['email']:
            emailsplit = request.form['email'].split('@')
        else:
            emailsplit = ['', '']

        config['author_email_prefix'] = emailsplit[0]
        config['author_email_suffix'] = emailsplit[1]

        config['author_url'] = request.form['url']

        creation_date = datetime.datetime.now()

        # Get the class corresponding to the given project type
        project_cls = [class_ for class_ in CLASSES.values()
                       if class_.project_long_name == project_type][0]
        # Create a zip file with the content
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zipf:
            # Copy entire file structure from template directory to the project
            # directory
            copy_file_structure('.', project_cls.template_path(),
                                replace=project_cls.replace, zipf=zipf,
                                files_to_ignore=['.DS_Store'],
                                modname=modname, config=config,
                                creation_date=creation_date)
            # Create files common to all projects
            for name in os.listdir(project_cls.common_template_path()):
                tpath = project_cls.common_template_path()
                template_path = os.path.join(tpath, name)
                create_single_file('.', name, template_path, zipf=zipf,
                                   modname=modname, config=config,
                                   creation_date=creation_date)
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename=modname+'.zip',
                         as_attachment=True)
    except:
        traceback.print_exc()
        return redirect(url_for('home', error='Oh no! Looks like '
                                'there was a problem.'))
    # return send_from_directory(directory=rootdir,
    #                            filename=modname+'.zip')
    # # Redirect to home page
    # return redirect('/')

if __name__ == "__main__":
    app.run()
