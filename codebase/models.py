from xml.etree import ElementTree


class Model(object):

    def __init__(self, tree, api, parent=None, created=False):
        self.api = api
        self.parent = parent
        self.tree = tree
        self.created = created

    def to_xml(self):
        return ElementTree.tostring(self.tree)

    @classmethod
    def create(cls, api, parent=None, created=True):
        tree = ElementTree.Element(cls.tag_name)
        return cls(tree, api=api, parent=parent, created=True)

    def to_xml_string(self):
        return ElementTree.tostring(self.tree)

    def save(self):
        if self.created:
            url = self.parent.url / self.root_url
            data = self.to_xml_string()
            response = self.api.make_request(url, method='POST', data=data)

    def get_many(self, cls, url=None, query=None):
        if url is None:
            url = self.url / cls.root_url
        if query is None:
            query = {}
        url = url & query
        tree = self.api.make_request(url)
        return [cls(element, api=self.api, parent=self) for element in tree]

    def get_one(self, cls, url=None):
        if url is None:
            url = self.url / cls.root_url
        element = self.api.make_request(url)
        return cls(element, api=self.api, parent=self)


class Field(object):
    """Field descriptor"""

    def __init__(self, source):
        self.source = source

    def __get__(self, instance, owner):
        return instance.tree.find(self.source).text

    def __set__(self, instance, value):
        element = instance.tree.find(self.source)
        if element is None:
            element = ElementTree.SubElement(instance.tree, self.source)
        element.text = value


class Project(Model):

    tag_name = 'project'

    status = Field(source='status')
    permalink = Field(source='permalink')
    group_id = Field(source='group-id')
    overview = Field(source='overview')
    start_page = Field(source='start-page')
    icon = Field(source='icon')
    name = Field(source='name')

    @property
    def url(self):
        return self.api.url / self.permalink

    def get_all_tickets(self):
        return self.get_many(Ticket)

    def search_tickets(self, query):
        return self.get_many(Ticket, query=query)

    def create_ticket(self):
        return Ticket.create(api=self.api, parent=self)

    def get_all_repositories(self):
        return self.get_many(Repository)

    def get_repository(self, permalink):
        url = self.url / permalink
        return self.get_one(Repository, url=url)

    def get_all_users(self):
        return self.get_many(User)


class Ticket(Model):

    tag_name = 'ticket'
    root_url = 'tickets'

    ticket_id = Field(source='ticket-id')
    summary = Field(source='summary')
    ticket_type = Field(source='ticket-type')
    reporter_id = Field(source='reporter-id')
    reporter = Field(source='reporter')
    assignee_id = Field(source='assignee-id')
    assignee = Field(source='assignee')
    category_id = Field(source='category-id')
    priority_id = Field(source='priority-id')
    status_id = Field(source='status-id')
    milestone_id = Field(source='milestone-id')


class Repository(Model):

    tag_name = 'repository'
    root_url = 'repositories'

    name = Field(source='name')
    permalink = Field(source='permalink')
    disk_usage = Field(source='disk-usage')
    last_commit_ref = Field(source='last-commit-ref')
    clone_url = Field(source='clone-url')

    @property
    def url(self):
        return self.parent.url / self.permalink


class User(Model):

    tag_name = 'user'
    root_url = 'assignments'

    company = Field(source='company')
    first_name = Field(source='first-name')
    id = Field(source='id')
    last_name = Field(source='last-name')
    username = Field(source='username')
    email_address = Field(source='email-address')
