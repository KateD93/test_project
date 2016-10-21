#!.test_project/bin/python
from flask import Response,abort
from flask import request
from app import app
from datetime import datetime
import commands
import json
import yaml
import os


TEMP_DIR = "temp/"
REPO_NAME = "robbed_bank_account"
REPO_URL = "git@github.com:KateD93/{}.git".format(REPO_NAME)

# ------ api endpoints ----------

@app.route("/", methods=["GET"])
def main():
    return Response("HTML todo")


@app.errorhandler(500)
def internal_error(error):
    return "Error: %s" % error


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown", methods=["GET"])
def shutdown():
    shutdown_server()
    return Response("Server shutting down... Goodbye", status = 200)


@app.route("/posting_file", methods=["POST"])
def posting_file():
    content_string = request.files["upload"].read()
    content_json = json.loads(content_string)
    # now we use content_json dict to posting data
    commit, n_updates = process_repo("update", content_json)
    return Response("Elements update successfully; num_updates: {}, commit_sha: {}\n".format(n_updates, commit), status = 200)


@app.route("/remove_elem", methods=["POST"])
def remove_elem():
    content_string = request.files["upload"].read()
    content_json = json.loads(content_string)
    # now we use content_json dict to delete data
    commit, n_updates = process_repo("delete", content_json)
    return Response("Elements deleted successfully; \
                    num_updates: {}, commit_sha: {}\n".format(n_updates, commit), status = 200)


# --------
def process_repo(op, content_json):
    """ Changes data in repository"""
    name_branch = "change_v_" + datetime.strftime(datetime.now(), "%Y%m%d_%H_%M_%S")
    message = "Doing some change"
    # clone git repo
    run_command("mkdir -p {}".format(TEMP_DIR))
    rm_dir = os.path.join(TEMP_DIR, REPO_NAME)
    if rm_dir != "/":
        run_command("rm -r '{}'".format(rm_dir), ignore_fails = True)
    run_command("cd '{}'; git clone '{}'".format(TEMP_DIR, REPO_URL))
    # create new branch
    cmd_pref = "cd '" + os.path.join(TEMP_DIR, REPO_NAME) + "'; "
    run_command(cmd_pref + "git branch {}".format(name_branch))
    run_command(cmd_pref + "git checkout {}".format(name_branch))
    # doing changes
    num_changes = find_dirs(TEMP_DIR + REPO_NAME, op, content_json)
    if num_changes > 0:
        # do commit
        run_command(cmd_pref + "git add .")
        run_command(cmd_pref + "git commit -m '{}'".format(message))
        commit_sha = run_command(cmd_pref + "git log --format='%H' -n 1")
        run_command(cmd_pref + "git push origin {}".format(name_branch))
        return (commit_sha, num_changes)
    # no changes
    return (0, None)


def run_command(command, ignore_fails = False):
    """ Runs command in os system"""
    err_code, output = commands.getstatusoutput(command)
    if err_code != 0 and not ignore_fails:
        raise ValueError("command failed with %i: %s\noutput:\n%s" % (err_code, command, output))
    return output


def find_dirs(repo_dir, op, content_json):
    """ Finds files by recursion"""
    total_changes = 0
    for path,dirs,files in os.walk(repo_dir):
        for fn in dirs:
            # got directory: process it recursive
            cc = find_dirs(os.path.join(repo_dir, fn), op, content_json)
            total_changes += cc
        for fname in files:
            # got file: process it if it's yaml
            if fname.endswith(".yaml") or fname.endswith(".yml"):
                cc = process_file(os.path.join(repo_dir, fname), op, content_json)
                total_changes += cc
    return total_changes


def process_file(fn, op, content_json):
    """ Op is operation: 'update' or 'delete' """
    # load file
    with open(fn, "r") as f:
        f_data = f.read()
    # parsing
    content_yaml = yaml.load(f_data)
    # processing
    if op == "update":
        num_changes = update_yaml(content_json, content_yaml)
    elif op == "delete":
        num_changes = delete_yaml(content_json, content_yaml)
    else:
        print "Bad operation"
    # if changes made to file
    if num_changes > 0:
        # saving
        saved_str = yaml.dump(content_yaml, default_flow_style = False)
        # writing to file
        with open(fn, "w") as f:
            f.write(saved_str)
    return num_changes


# ---------- yaml update and delete ------
def update_yaml(content_json, content_yaml):
    """ Applies change to given yaml dict lists. Content json is just a dict"""
    num_var_val = 0
    for key in content_yaml:
        v = content_yaml[key]
        if type(v) == dict:
            # for dicts, processing it again
            num_var_val += update_yaml(content_json, v)
        elif key in content_json:
            # not dict: replacing it
            repl_v = content_json[key]
            if repl_v != v:
                content_yaml[key] = repl_v
                num_var_val += 1
    return num_var_val


def delete_yaml(content_json, content_yaml):
    """ Applies change to given yaml dict lists. Content json is just a dict"""
    keys_to_del = []
    num_var_val = 0
    for key in content_yaml:
        v = content_yaml[key]
        if type(v) == dict:
            # for dicts, processing it again
            num_var_val += delete_yaml(content_json, v)
        elif key in content_json:
            keys_to_del.append(key)
            num_var_val += 1
    # actual deleting keys
    for k in keys_to_del:
        content_yaml.pop(k)
    return num_var_val

