import unittest
import json
from unittest.mock import patch
from unittest.mock import Mock
from dm.arm.core.config import VNetConfig as vc
from dm.arm.core.config import SubnetGroupConfig as sgc
from dm.arm.core.config import ERROR_NO_SUBNET_GROUPS_DEF
from dm.arm.core.config import ERROR_UNDEFINED_SUBNET_GROUPS
from dm.arm.core.config import ERROR_DUPLICATE_SUBNET_NAME
from dm.arm.core.config import ERROR_DUPLICATE_SUBNET_GROUP_NAME
from dm.arm.core.config import ERROR_DUPLICATE_SUBNET_GROUP_NAME_INSPECTED

class ValidateSubnetGroups(unittest.TestCase):

    def setUp(self):
        with open("test/fixtures/arm_config_subnet_groups.json") as f:
            data = json.load(f)
            self.input = data["ValidateSubnetGroups"]

    def test_subnet_group(self):
        val_lst = self.input["val"]
        val = [ sgc(**x["SubnetGroupConfig"]) for x in val_lst ] 
        values = self.input["values"]
        self.assertEqual(val, vc.validate_subnet_groups(val, values))

    def test_duplicate_group_name(self):
        val_lst = self.input["val"]
        val_lst[0]["SubnetGroupConfig"]["group_name"] = "mgmt"
        val = [ sgc(**x["SubnetGroupConfig"]) for x in val_lst ] 
        values = self.input["values"]
        with self.assertRaises(ValueError) as e:
            vc.validate_subnet_groups(val, values)
        self.assertEqual(str(e.exception),ERROR_DUPLICATE_SUBNET_GROUP_NAME)

    def test_duplicate_subnet_name(self):
        val_lst = self.input["val"]
        val_lst[0]["SubnetGroupConfig"]["subnet_name"] = "private"
        val = [ sgc(**x["SubnetGroupConfig"]) for x in val_lst ] 
        values = self.input["values"]
        with self.assertRaises(ValueError) as e:
            vc.validate_subnet_groups(val, values)
        self.assertEqual(str(e.exception),ERROR_DUPLICATE_SUBNET_NAME)


class ValidateSubnetGroupsInspected(unittest.TestCase):

    def setUp(self):
        with open("test/fixtures/arm_config_subnet_groups.json") as f:
            data = json.load(f)
            self.input = data["ValidateSubnetGroupsInspected"]

    def test_group_inspected(self):
        val = self.input["val"]
        values = self.input["values"]
        values["subnet_groups"] = [ sgc(**x["SubnetGroupConfig"]) for x in values["subnet_groups"] ]
        self.assertEqual(val, vc.validate_subnet_groups_inspected(val, values))

    def test_no_subnet_groups_def(self):
        val = self.input["val"]

        # convert SubnetGroupConfig dict into SubnetGroupConfig object
        values = self.input["values"]
        values["subnet_groups"] = None
        
        with self.assertRaises(ValueError) as e:
            vc.validate_subnet_groups_inspected(val, values)
        self.assertEqual(str(e.exception), ERROR_NO_SUBNET_GROUPS_DEF)

    def test_undefined_group(self):
        val = self.input["val"]
        # add a undefined group
        val.append("external")

        errors = ["external"]

        # convert SubnetGroupConfig dict into SubnetGroupConfig object
        values = self.input["values"]
        values["subnet_groups"] = [ sgc(**x["SubnetGroupConfig"]) for x in values["subnet_groups"] ]
        
        with self.assertRaises(ValueError) as e:
            vc.validate_subnet_groups_inspected(val, values)
        self.assertEqual(str(e.exception), ERROR_UNDEFINED_SUBNET_GROUPS.format(errors=errors))

    def test_duplicate_group_name(self):
        val = self.input["val"]
        val.append("internal")
        values = self.input["values"]
        values["subnet_groups"] = [ sgc(**x["SubnetGroupConfig"]) for x in values["subnet_groups"] ]
        with self.assertRaises(ValueError) as e:
            vc.validate_subnet_groups_inspected(val, values)
        self.assertEqual(str(e.exception),ERROR_DUPLICATE_SUBNET_GROUP_NAME_INSPECTED)
        
