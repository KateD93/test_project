#!.test_project/bin/python
import unittest
import os
from app.views import update_yaml, delete_yaml
import yaml

class TestCase(unittest.TestCase):
    
    def test_update(self):
        # example data
        with open(os.path.dirname(__file__) + '/sample.yaml', 'r') as f:
            e_data = f.read()
        e_p = yaml.load(e_data)
        # function test
        n_updates = update_yaml({ "Bono": "Beer",
                                  "Harrison": "Rum",
                                  "Martin McFly": "Cola" }, e_p)
        # checks
        self.assertEquals(n_updates, 2)
        self.assertEqual(e_p["Musicians"]["Bono"], "Beer")
        self.assertEqual(e_p["Musicians"]["Beatles"]["Harrison"], "Rum")

    def test_delete(self):
        # example data
        with open(os.path.dirname(__file__) + '/sample.yaml', 'r') as f:
            e_data = f.read()
        e_p = yaml.load(e_data)
        # function test
        n_updates = delete_yaml([ "Lady Gaga", "Harrison", "Monte Cristo" ], e_p)
        # checks
        self.assertEquals(n_updates, 2)
        self.assertEqual(e_p["Musicians"].get("Lady Gaga"), None)
        self.assertEqual(e_p["Musicians"]["Beatles"].get("Harrison"), None)

if __name__=='__main__':
    unittest.main()
