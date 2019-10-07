# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import jinja2
import json
import sys

log = logging.getLogger(__name__)


# this function takes a path to a folder containing .rst files to be rendered
# and returns a generator for iterating through them
def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        # yield os.path.join(folder_path, name), base
        yield folder_path+'/'+name, base


# read_file takes a path to a certain file meant to be rendered,
# read its data and stores it in json format
def read_file(file_path):
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line.rstrip('\n')
    try:
        metadata = json.loads(raw_metadata)
        return metadata, content
    except ValueError:
        log.error('JSON object not found in {}'.format(file_path))


# takes the name of the document, the html generated
# creates the adequate static page
def write_output(name, html, *args):
    # TODO should not use sys.argv here, it breaks encapsulation
    if not os.path.exists(args[0]):
        os.mkdir(args[0])
    with open(os.path.join(args[0], name + '.html'), 'w') as f:
        f.write(html)


# generates the site from the layout of the page by creating a jinga environment
# and by rendering the data collected above
def generate_site(folder_path, *args):
    log.info("Generating site from %r", folder_path)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(folder_path, 'layout')))
    for file_path, name in list_files(folder_path):
        metadata, content = read_file(file_path)
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        html = template.render(**data)
        write_output(name, html, args[0])
        log.info("Writing %r with template %r", name, template_name)


def main():
    generate_site(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    logging.basicConfig()
    main()
