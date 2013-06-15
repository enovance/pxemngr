#---------------------------------------------------------------
# Project         : pxe
# File            : test_pxeparse.py
# Copyright       : (C) 2013 by 
# Author          : Frederic Lepied
# Created On      : Sat Jun 15 22:21:49 2013
# Purpose         : 
#---------------------------------------------------------------

import unittest

import pxeparse

class TestPxeparseTest(unittest.TestCase):
    
    def test_parse(self):
        r = pxeparse.parse('''DEFAULT eDeploy
  
LABEL eDeploy
KERNEL vmlinuz
APPEND initrd=initrd.pxe SERV=10.66.6.10
''')
        return self.assertEqual(
            r, {'DEFAULT': 'eDeploy',
                'eDeploy':
                    {'KERNEL': 'vmlinuz',
                     'APPEND': 'initrd=initrd.pxe SERV=10.66.6.10'
                     }})

    def test_parse_complete(self):
        r = pxeparse.parse('''DEFAULT eDeploy

prompt 0
timeout 0

  
LABEL eDeploy
KERNEL vmlinuz
APPEND initrd=initrd.pxe SERV=10.66.6.10
''')
        return self.assertEqual(
            r, {'DEFAULT': 'eDeploy',
                'prompt': '0',
                'timeout': '0',
                'eDeploy':
                    {'KERNEL': 'vmlinuz',
                     'APPEND': 'initrd=initrd.pxe SERV=10.66.6.10'
                     }})

if __name__ == "__main__":
    unittest.main()
                                        
# test_pxeparse.py ends here
