import csv
import json
import re

import requests

from LinkExtractor import LinkExtractor

SPRINGFRAMEWORK = 'org.springframework'
SPRINGWEBFLOW = 'org.springframework.webflow'
SPRINGBOOT = 'org.springframework.boot'

VERBOSE = False
INCLUDE_VERSIONS = False
CRAWL_MAVEN = True
CRAWL_GROUP = SPRINGFRAMEWORK

JSON_FILE = 'repo.json'
CSV_FILE = 'artifacts.csv'

maven_base_url = 'https://repo1.maven.org/maven2/'
metadata_file = 'maven-metadata.xml'
jar_path_ext = '.jar'
sha1_path_ext ='.jar.sha1'
jar_name_format = '{}-{}.jar'   # artifact id, version

vers_path_pattern = re.compile(r"^(ivy\-)?\d+\.\d+(\.\d+)?[.-a-zA-Z0-9]*/?")

ABERRANT_ARTIFACT_NAMES = ['spring-session-bom', 'spring-obj']

GROUP_NODE = 'sub-group'
ARTIFACT_NODE = 'artifact'
UNPARSABLE_NODE = 'unparseable'

NODE_TYPE = 'type'
NODE_NAME = 'name'
CHILDREN = 'children'

def get_response_or_raise(url):
    response = requests.get(url)
    if response.status_code == 200:
        if VERBOSE:
            print('GET ' + url + ' returns:')
            print(response)
        else:
            print('.', end='')
        return response
    else:
        msg = 'GET ' + url + ' returns HTTP status: ' + str(response.status_code)
        if VERBOSE:
            print(msg)
        raise Exception(msg)

def parse_maven_response(response):
    body = response.content.decode('utf-8')
    return LinkExtractor().extract_hrefs(body)

def is_artifact(child_paths, node_name):
    if node_name in ABERRANT_ARTIFACT_NAMES:
        return True

    # org.springframework.boot and .cloud both have stray metadata_files
    # if metadata_file in child_paths:
    #     return True

    for child_path in child_paths:
        if vers_path_pattern.match(child_path):
            return True
    return False

last_node_type = GROUP_NODE

def progress_indicator(node_type):
    global last_node_type
    if not VERBOSE and last_node_type != node_type:
        last_node_type = node_type
        print()

def retrieve_and_parse(node_name, url):
    try:
        response = get_response_or_raise(url)
        child_paths = parse_maven_response(response)
    except Exception as e:
        print("Exception processing url " + url)
        print(str(e))
        return {NODE_NAME: node_name, NODE_TYPE: UNPARSABLE_NODE, CHILDREN: []}

    if is_artifact(child_paths, node_name):
        progress_indicator(ARTIFACT_NODE)
        if INCLUDE_VERSIONS:
            return {NODE_NAME: node_name, NODE_TYPE: ARTIFACT_NODE, CHILDREN: child_paths}
        elif metadata_file in child_paths:
            # return {NODE_NAME: node_name, NODE_TYPE: ARTIFACT_NODE, CHILDREN: [metadata_file]}
            # for brevity in the normal case where an artifact has metadata omit children
            return {NODE_NAME: node_name, NODE_TYPE: ARTIFACT_NODE}
        else:
            # for the aberrant case with missing metadata show empty children
            return {NODE_NAME: node_name, NODE_TYPE: ARTIFACT_NODE, CHILDREN: []}
    else:
        progress_indicator(GROUP_NODE)
        return {NODE_NAME: node_name, NODE_TYPE: GROUP_NODE, CHILDREN: child_paths}

def create_repo_tree(node_name, root_url):
    node_data = retrieve_and_parse(node_name, root_url)
    if node_data[NODE_TYPE] == GROUP_NODE:
        child_paths = node_data[CHILDREN]
        node_data[CHILDREN] = []
        for child_path in child_paths:
            if not child_path == '../':
                child_node = create_repo_tree(child_path.rstrip('/'), root_url + child_path)
                node_data[CHILDREN].append(child_node)
        return node_data
    elif node_data[NODE_TYPE] == ARTIFACT_NODE:
        # we can retrieve the metadata if we choose
        return node_data
    elif node_data[NODE_TYPE] == UNPARSABLE_NODE:
        return node_data
    else:
        raise Exception('Unknown node type: ' + str(node_data[NODE_TYPE]))

def crawl_repo(groupid):
    group_path = groupid.replace('.', '/')
    group_url = maven_base_url + group_path + '/'
    return create_repo_tree(groupid, group_url)

def write_repo_tree(repo_tree, filename=JSON_FILE):
    jsonStr = json.dumps(repo_tree, indent=2)
    with open(filename, 'w') as outfile:
        outfile.write(jsonStr)
    return jsonStr

def read_repo_tree(filename=JSON_FILE):
    with open(filename, 'r') as infile:
        repo_tree = json.load(infile)
    return repo_tree

def flatten_repo_node(artifact_list, parent_group, node):
    if node[NODE_TYPE] == ARTIFACT_NODE:
        artifact = node[NODE_NAME]
        group = parent_group
        artifact_list.append([group, artifact])
    elif node[NODE_TYPE] == GROUP_NODE:
        group = node[NODE_NAME]
        if parent_group:
            group = parent_group + '.' + group
        for child_node in node[CHILDREN]:
            flatten_repo_node(artifact_list, group, child_node)
    elif node[NODE_TYPE] == UNPARSABLE_NODE:
        name = node[NODE_NAME]
        group = parent_group
        artifact_list.append([group, name + '(UNPARSABLE)'])
    else:
        raise Exception('Unknown node type: ' + str(node[NODE_TYPE]))

def flatten_repo_tree(repo_tree):
    artifact_list = []
    flatten_repo_node(artifact_list, '', repo_tree)
    return artifact_list

def write_artifact_csv(artifact_list, filename=CSV_FILE):
    with open(filename, 'w', newline='') as outfile:
        writer = csv.writer(outfile, )
        writer.writerow(['group', 'artifact'])
        writer.writerows(artifact_list)

def main():
    if CRAWL_MAVEN:
        repo_tree = crawl_repo(CRAWL_GROUP)
        repo_json = write_repo_tree(repo_tree)
        if VERBOSE:
            print(repo_json)
    else:
        repo_tree = read_repo_tree()
        if VERBOSE:
            print(json.dumps(repo_tree, indent=2))
    artifact_list = flatten_repo_tree(repo_tree)
    write_artifact_csv(artifact_list)
    if VERBOSE:
        with open(CSV_FILE, 'r') as file:
            lines = file.readlines()
        for line in lines:
            print(line, end='')

if __name__ == '__main__':
    # test = ['ivy-2.4.0.RELEASE.xml.asc']
    # print('is_artifact({}) = {}'.format(test, str(is_artifact(test))))
    main()