import requests
import re
import json
import csv
from LinkExtractor import LinkExtractor

verbose = True
include_artifact_versions = False

base_group = 'org.springframework'
base_group_path = base_group.replace('.', '/')
maven_base_url = 'https://repo1.maven.org/maven2/'
metadata_file = 'maven-metadata.xml'
jar_path_ext = '.jar'
sha1_path_ext ='.jar.sha1'
jar_name_format = '{}-{}.jar'   # artifact id, version

vers_path_pattern = re.compile(r"^(ivy\-)?\d+\.\d+\.\d+[.-a-zA-Z0-9]*/?")

GROUP_NODE = "sub-group"
ARTIFACT_NODE = "artifact"

download_dir = 'data'

def get_response_or_raise(url):
    response = requests.get(url)
    if response.status_code == 200:
        if verbose:
            print('GET ' + url + ' returns:')
            print(response)
        return response
    else:
        msg = 'GET ' + url + ' returns HTTP status: ' + str(response.status_code)
        if verbose:
            print(msg)
        raise Exception(msg)

def parse_maven_response(response):
    body = response.content.decode("utf-8")
    # print (body)
    return LinkExtractor().extract_hrefs(body)

def is_artifact(child_paths):
    if metadata_file in child_paths:
        return True
    for child_path in child_paths:
        if vers_path_pattern.match(child_path):
            return True
    return False

def retrieve_and_parse(node_name, url):
    response = get_response_or_raise(url)
    child_paths = parse_maven_response(response)
    if is_artifact(child_paths):
        if include_artifact_versions:
            return {"name": node_name, "type": ARTIFACT_NODE, "children": child_paths}
        elif metadata_file in child_paths:
            # return {"name": node_name, "type": ARTIFACT_NODE, "children": [metadata_file]}
            # for brevity in the normal case where an artifact has metadata omit children
            return {"name": node_name, "type": ARTIFACT_NODE}
        else:
            # for the aberrant case with missing metadata show children empty
            return {"name": node_name, "type": ARTIFACT_NODE, "children": []}
    else:
        return {"name": node_name, "type": GROUP_NODE, "children": child_paths}

def create_repo_tree(node_name, root_url):
    node_data = retrieve_and_parse(node_name, root_url)
    if node_data["type"] == GROUP_NODE:
        child_paths = node_data["children"]
        node_data["children"] = []
        for child_path in child_paths:
            if not child_path == '../':
                child_node = create_repo_tree(child_path.rstrip("/"), root_url + child_path)
                node_data["children"].append(child_node)
        return node_data
    else:
        # we can retrieve the metadata if we choose
        return node_data

def crawl_repo(groupid='org.springframework.session'):
    group_path = groupid.replace('.', '/')
    group_url = maven_base_url + group_path + "/"
    return create_repo_tree(groupid, group_url)

def write_repo_tree(repo_tree, filename="repo.json"):
    jsonStr = json.dumps(repo_tree, indent=2)
    print(jsonStr)
    with open(filename, "w") as outfile:
        outfile.write(jsonStr)
    return jsonStr

def read_repo_tree(filename="repo-session.json"):
    with open(filename, 'r') as infile:
        repo_tree = json.load(infile)
    return repo_tree

def flatten_repo_node(artifact_list, parent_group, node):
    if node['type'] == ARTIFACT_NODE:
        artifact = node['name']
        group = parent_group
        artifact_list.append([group, artifact])
    elif node['type'] == GROUP_NODE:
        group = node['name']
        if parent_group:
            group = parent_group + '.' + group
        for child_node in node['children']:
            flatten_repo_node(artifact_list, group, child_node)
    else:
        raise Exception("Unknown repo_tree node type: " + str(repo_tree[type]))

def flatten_repo_tree(repo_tree):
    artifact_list = []
    flatten_repo_node(artifact_list, "", repo_tree)
    return artifact_list

def write_artifact_csv(artifact_list, filename='artifacts.csv'):
    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['group', 'artifact'])
        writer.writerows(artifact_list)

def main():
    print(write_repo_tree(crawl_repo(groupid='org.springframework')))
    repo_tree = read_repo_tree()
    # print(json.dumps(repo_tree, indent=2))
    artifact_list = flatten_repo_tree(repo_tree)
    write_artifact_csv(artifact_list)
    # print(json.dumps(artifact_list, indent=2))

if __name__ == '__main__':
    # test = ['ivy-2.4.0.RELEASE.xml.asc']
    # print("is_artifact({}) = {}".format(test, str(is_artifact(test))))
    main()