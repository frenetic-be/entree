'''
.. module:: entree.projects
.. moduleauthor:: Julien Spronck
.. created:: Feb 2018

Module for all projects
'''

from entree.projects.flask import Flask
from entree.projects.python import Python
from entree.projects.sqlalchemy import SQLAlchemy
from entree.projects.base import ProjectBase

CLASSES = ProjectBase.__subclasses__()
CLASSES = {pcls.__name__.lower(): pcls for pcls in CLASSES}
