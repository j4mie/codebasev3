from dictshield import document, fields
from .utils import etree_to_dict


class CodebaseDocument(document.Document):

    def __init__(self, data, parent):
        self.parent = parent
        kwargs = {key.replace('-', '_'): value for key, value in data.items()}
        super(CodebaseDocument, self).__init__(**kwargs)


class Project(CodebaseDocument):

    status = fields.StringField()
    permalink = fields.StringField()
    group_id = fields.IntField()
    overview = fields.StringField()
    start_page = fields.StringField()
    icon = fields.IntField()
    name = fields.StringField()

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

    ticket_id = fields.IntField()
    summary = fields.StringField()
    ticket_type = fields.StringField()
    reporter_id = fields.IntField()
    reporter = fields.StringField()
    assignee_id = fields.IntField()
    assignee = fields.StringField()
    category_id = fields.IntField()
    priority_id = fields.IntField()
    status_id = fields.IntField()
    milestone_id = fields.IntField()


class Repository(CodebaseDocument):

    name = fields.StringField()
    permalink = fields.StringField()
    disk_usage = fields.IntField()
    last_commit_ref = fields.StringField()
    clone_url = fields.StringField()

    @property
    def url(self):
        return self.parent.url / self.permalink
