# -*- coding: utf-8 -*-
"""
Created on Fri May 26 12:44:29 JST 2023

@author: okada

"""

import unittest
import subprocess
import yaml

class ConfigureTest(unittest.TestCase):
    

    # init class
    @classmethod
    def setUpClass(self):
        pass

    # terminated class
    @classmethod
    def tearDownClass(self):
        pass

    # init method
    def setUp(self):
        pass

    # terminated method
    def tearDown(self):
        pass

    def test1_02_version(self):
        subprocess.check_call(['python', 'gcat_runner', '--version'])
    
    def test2_01_bash(self):
        conf = {
            "runner": "bash",
            "qsub_option": "",
            "log_dir": "./tests",
            "max_task": 0,
            "retry_count": 1,
        }
        bash_file = './tests/test_bash_runner.sh'
        conf_file = "./tests/conf_bash_runner.yml"
        with open(conf_file, "w") as f:
            yaml.dump(conf, f, default_flow_style=False)

        subprocess.check_call(['gcat_runner', bash_file, conf_file, '--interval', '10'])

if __name__ == '__main__':
    unittest.main()
