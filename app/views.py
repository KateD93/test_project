#!.test_project/bin/python
from flask import Response
from flask import request
from app import app
import commands
import json
import yaml
import os
import git


def clone_git_repo():
    err_code, output = commands.getstatusoutput('git clone git@github.com:KateD93/robbed_bank_account.git')
    if err_code != 0:
        print output
        raise ValueError("Git clone failed %s" %err_code)


@app.route('/', methods=['GET'])
def main():
    return Response('Hello world')


def update_yaml(content_json, content_yaml):
    """Update values"""
    for key in content_yaml:
        for item in content_yaml[key]:
            for i in range(len(content_json)):
                if item in content_json[i]:
                    content_yaml[key][item] = content_json[i][item]


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
    content_yaml = yaml.load(open('robbed_bank_account/file1.yml'))
    update_yaml(content_json, content_yaml)
    write_file('robbed_bank_account/file1.yml', content_yaml)
    commit_and_push()
    return Response("Elements update successfully")


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
    commit_and_push()
    return Response('Elements delete successfully')


def write_file(fn, content_yaml):
    with open(fn, 'w') as f:
       yaml.dump(content_yaml, f, default_flow_style = False)


def commit_and_push():
    err_code, output = commands.getstatusoutput('cd robbed_bank_account; git add .')
    if err_code != 0:
        print output
        raise ValueError("Git add failed %s" % err_code)
    err_code, output = commands.getstatusoutput('cd robbed_bank_account; git commit -m "Doing some change"')
    if err_code != 0:
        print output
        raise ValueError("Git commit failed %s" % err_code)
    err_code, output = commands.getstatusoutput('cd robbed_bank_account; git push origin master')
    if err_code != 0:
        print output
        raise ValueError("Git push on github failed %s" % err_code)






