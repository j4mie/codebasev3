from xml.etree import ElementTree


class Model(object):

    def __init__(self, tree, parent):
        self.parent = parent
        self.tree = tree

    def to_xml(self):
        return ElementTree.tostring(self.tree)


class Field(object):
    """Field descriptor"""

    def __init__(self, source):
        self.source = source

    def __get__(self, instance, owner):
        return instance.tree.find(self.source).text

    def __set__(self, instance, value):
        instance.tree.find(self.source).text = value


class Project(Model):

    status = Field(source='status')
    permalink = Field(source='permalink')
    group_id = Field(source='group-id')
    overview = Field(source='overview')
    start_page = Field(source='start-page')
    icon = Field(source='icon')
    name = Field(source='name')

    @property
    def url(self):
        return self.parent.url / self.permalink

    def get_all_tickets(self):
        return self.search_tickets({})

    def search_tickets(self, query):
        tree = self.parent.make_request(self.url / 'tickets' & query)
        return [Ticket(element, self) for element in tree]

    def get_all_repositories(self):
        tree = self.parent.make_request(self.url / 'repositories')
        return [Repository(element, self) for element in tree]


class Ticket(Model):

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

    name = Field(source='name')
    permalink = Field(source='permalink')
    disk_usage = Field(source='disk-usage')
    last_commit_ref = Field(source='last-commit-ref')
    clone_url = Field(source='clone-url')

    @property
    def url(self):
        return self.parent.url / self.permalink
