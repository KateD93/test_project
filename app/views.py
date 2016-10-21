#!.test_project/bin/python
from flask import Response,abort
from flask import request
from app import app
from datetime import datetime
import commands
import json
import yaml
import os
import git
import glob


def clone_git_repo():
    err_code, output = commands.getstatusoutput('git clone git@github.com:KateD93/robbed_bank_account.git')
    if err_code != 0:
        print output
        raise ValueError("Git clone failed %s" %err_code)


@app.route('/', methods=['GET'])
def main():
    return Response('Hello world')


def update_yaml(content_json, content_yaml):
    num_var_val = 0
    for key in content_yaml:
        for item in content_yaml[key]:
            for i in range(len(content_json)):
                if item in content_json[i]:
                    num_var_val += num_var_val
                    content_yaml[key][item] = content_json[i][item]
    return num_var_val


def delete_yaml(content_json, content_yaml):
    """Deleted keys and values"""
    for key in content_yaml:
        for item in dict(content_yaml[key]):
            if item in content_json:
                content_yaml[key].pop(item)


@app.route('/posting_file', methods=['POST'])
def posting_file():
    commands.getstatusoutput('rm -r robbed_bank_account')
    x = request.files
    content_string = x['upload'].read()
    content_json = json.loads(content_string)
    clone_git_repo()
    content_yaml = yaml.load(open('robbed_bank_account'))
    update_yaml(content_json, content_yaml)
    write_file('robbed_bank_account/file1.yml', content_yaml)
    return commit_and_push() or Response("Elements update successfully", status = 200)


@app.route('/remove_elem', methods=['POST'])
def remove_elem():
    commands.getstatusoutput('rm -r robbed_bank_account')
    x = request.files
    content_string = x['upload'].read()
    content_json = json.loads(content_string)
    clone_git_repo()
    content_yaml = yaml.load(open('robbed_bank_account/file2.yml'))
    delete_yaml(content_json, content_yaml)
    write_file('robbed_bank_account/file2.yml', content_yaml)
    return commit_and_push() or Response('Elements delete successfully', status = 200)




def write_file(fn, content_yaml):
    with open(fn, 'w') as f:
       yaml.dump(content_yaml, f, default_flow_style = False)


def process_file(fn):
    content_yaml = yaml.load(open('robbed_bank_account/‘ + fn))
    update_yaml(content_json, content_yaml)
    write_file('robbed_bank_account/' + fn, content_yaml)

def read_file():
    dir = '/data/work/virtualenvs/test_project/test_project/robbed_bank_account'
    names = glob.glob('robbed_bank_account/*.yml')
    for root, dirs, files in os.walk(dir):
        for root, dirs, files in os.walk(dir):
            for name in names:
                process_file(name)



def commit_and_push():
    now = datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M:%S')
    name_branch = 'upload files' + now
    message = 'Doing some change'
    commands_git = {'git_add': "git add .",
                    'git branch': 'git checkout -b %s' %name_branch,
                    'git_commit': 'git commit -m %s' %message,
                    'git_push' : 'git push origin %s' %name_branch
    }
    err_code, output = commands.getstatusoutput('cd robbed_bank_account; git add .')
    if err_code != 0:
        return Response(output + '\n', status = 500)
    err_code, output = commands.getstatusoutput('cd robbed_bank_account; git commit -m "Doing some change"')
    if err_code != 0:
        return Response(output + '\n', status = 500)
    err_code, output = commands.getstatusoutput('cd robbed_bank_account; git push origin master')
    if err_code != 0:
        return Response(output + '\n', status = 500)






