from jinja2 import Environment
import pickle


def toid(s):
    valid_chars = ''.join(c for c in s if c.isalnum() or c.isspace())
    return '-'.join(valid_chars.split())


env = Environment()
env.filters['toid'] = toid
with open('teammates.pickle', 'rb') as f:
    teammates = pickle.load(f)
with open('output.jinja') as f:
    tmpl = env.from_string(f.read())
print(tmpl.render(teammates=teammates))

