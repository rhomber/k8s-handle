import atexit
import logging
import os
import tempfile

import yaml, os
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from k8s_handle.exceptions import InvalidYamlError

# furiousassault RE: it's not a good practice to log from utility function
# maybe we should pass os.remove failure silently, it doesn't seem so important
log = logging.getLogger(__name__)

tenv = Environment(
  undefined=StrictUndefined,
  loader=FileSystemLoader(['.']))

def load_yaml(path):
    try:
        tmpl = tenv.get_template(path) 
        return yaml.safe_load(tmpl.render(env=os.environ))
    except Exception as e:
        raise InvalidYamlError("file '{}' doesn't contain valid yaml: {}".format(
            path, e))


def write_file_tmp(data):
    def remove_file(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            log.warning('Unable to remove "{}", due to "{}"'.format(file_path, e))

    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(data)
    f.flush()
    atexit.register(remove_file, f.name)
    return f.name
