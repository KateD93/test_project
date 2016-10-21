#!.test_project/bin/python
import os
from threading import Thread
import unittest
import commands
from flask import Response
from app import app
from app.views import run_command

TEMP_DIR = "temp/"

class TestAPI(unittest.TestCase):
    
    th = None
    
    def setUp(self):
        # starting API server in other thread
        self.th = Thread(target=app.run)
        self.th.daemon = True # to let it die after test is done
        self.th.start()
        # cloning repo
        run_command("cd '" + TEMP_DIR + "'; git clone '" + os.path.dirname(__file__) + "/test_git_repo.git'")
        CD_CMD = "cd '{}'; ".format(os.path.join(TEMP_DIR, "test_git_repo.git"))
        
    def tearDown(self):
        run_command("curl http://127.0.0.1:5000/shutdown -s")
    
    def test_update(self):
        # sending test js on data
        print os.getcwd()
        assert os.path.isfile(os.path.dirname(__file__) + '/test_data.json')
        err_code, output = commands.getstatusoutput('curl -F upload=@test_data.json -F press=OK \
                                                    http://127.0.0.1:5000/posting_file')
        # making sure curl executed fine
        if err_code != 0:
            print output
            assert False

    





if __name__=='__main__':
    unittest.main()
