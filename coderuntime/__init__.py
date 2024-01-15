from flask import Flask
app = Flask(__name__)
from coderuntime.utils import get_projects
from coderuntime.constants import project_root

projects = []
r = None

def init():
    global projects, project_root
    projects = get_projects(project_root)
    from coderuntime import routes as r