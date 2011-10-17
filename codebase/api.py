import base64
import requests
from xml.etree import ElementTree
from urlobject import URLObject
from .utils import etree_to_dict
from .models import Project


class Codebase(object):

    BASE_URL = 'http://api3.codebasehq.com'

    def __init__(self, username, key):
        self.username = username
        self.key = key

    @property
    def url(self):
        return URLObject.parse(self.BASE_URL)

    def get_auth_header(self):
        auth = (self.username, self.key)
        return base64.encodestring('%s:%s' % auth).replace('\n', '')

    def get_headers(self):
        return {
            'Accept': 'application/xml',
            'Content-type': 'application/xml',
            'Authorization': self.get_auth_header(),
        }

    def make_request(self, url):
        response = requests.get(url, headers=self.get_headers())
        return ElementTree.fromstring(response.content)

    def get_all_projects(self):
        projects = self.make_request(self.url / 'projects')
        return [Project(etree_to_dict(project), self) for project in projects]

    def get_project(self, permalink):
        project = self.make_request(self.url / permalink)
        return Project(etree_to_dict(project), self)
