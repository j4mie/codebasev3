from codebase.api import Codebase

username = 'company/username'
key = 'xxxx' # API key from https://yourcompany.codebasehq.com/settings/profile

codebase = Codebase(username, key)

for project in codebase.get_all_projects():
    print project.permalink


project = codebase.get_project('carsiteexternal')
for ticket in project.get_all_tickets():
    print ticket.ticket_id, ticket.summary

for repo in project.get_all_repositories():
    print repo.name, repo.url
