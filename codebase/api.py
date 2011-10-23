import requests
from xml.etree import ElementTree
from urlobject import URLObject
from .models import Project


class Codebase(object):

    BASE_URL = 'http://api3.codebasehq.com'

    def __init__(self, username, key):
        self.username = username
        self.key = key

    @property
    def url(self):
        return URLObject.parse(self.BASE_URL)

    def make_request(self, url, method='GET', data=None):
        auth = (self.username, self.key)
        media_type = 'application/xml'
        headers = {'Accept': media_type, 'Content-type': media_type}
        response = requests.request(method, url, auth=auth, headers=headers, data=data)
        return ElementTree.fromstring(response.content)

    def get_all_projects(self):
        tree = self.make_request(self.url / 'projects')
        return [Project(element, api=self) for element in tree]

    def get_project(self, permalink):
        tree = self.make_request(self.url / permalink)
        return Project(tree, api=self)
