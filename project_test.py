#!.test_project/bin/python
import os
from threading import Thread
import unittest
import commands
from flask import Response
from app import app



class TestCase(unittest.TestCase):
    def test(self):
        #starting API server
        thread = Thread(target=app.run)
        thread.daemon = True
        thread.start()
        #sending test js on data
        print os.getcwd()
        assert os.path.isfile('test_data.json')
        err_code, output = commands.getstatusoutput('curl -F upload=@test_data.json -F press=OK \
                                                    http://127.0.0.1:5000/posting_file')
        # making sure curl executed fine
        if err_code != 0:
            print output
            assert False






if __name__=='__main__':
    unittest.main()