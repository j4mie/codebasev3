from .utils import etree_to_dict


class CodebaseDocument(object):

    def __init__(self, data, parent):
        self.parent = parent
        self.data = data


class Field(object):
    """Field descriptor"""

    def __init__(self, source):
        self.source = source

    def __get__(self, instance, owner):
        return instance.data[self.source]

    def __set__(self, instance, value):
        instance.data[self.source] = value


class Project(CodebaseDocument):

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
        tickets = self.parent.make_request(self.url / 'tickets' & query)
        return [Ticket(etree_to_dict(ticket), self) for ticket in tickets]

    def get_all_repositories(self):
        repos = self.parent.make_request(self.url / 'repositories')
        return [Repository(etree_to_dict(repo), self) for repo in repos]


class Ticket(CodebaseDocument):

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


class Repository(CodebaseDocument):

    name = Field(source='name')
    permalink = Field(source='permalink')
    disk_usage = Field(source='disk-usage')
    last_commit_ref = Field(source='last-commit-ref')
    clone_url = Field(source='clone-url')

    @property
    def url(self):
        return self.parent.url / self.permalink
