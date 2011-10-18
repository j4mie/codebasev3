import base64
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
        tree = self.make_request(self.url / 'projects')
        return [Project(element, self) for element in tree]

    def get_project(self, permalink):
        tree = self.make_request(self.url / permalink)
        return Project(tree, self)
