import unittest
import json
import logging
from unittest.mock import patch
from dm.commonlib import Common as comm

class FilterVpcInConfig(unittest.TestCase):

    def setUp(self):
        with open("test/fixtures/yaml.json") as f:
            self.config = json.load(f)
    
    def test_pick_all_vpcs(self):
        # pick all VPCs with mix of account qualifier
        vpcs = [
            "205987878622:vpc-0173cdff453971939",
            "vpc-045608ad8e0521589",
            "205987878620:vpc-0173cdff453971930",
            "vpc-045608ad8e0521580",
        ]
        comm.filterVpcInConfig(self.config, vpcs)
        self.assertEqual(len(self.config["account_info"][0]["regions"][0]["vpcs"]), 2)
        self.assertEqual(len(self.config["account_info"][1]["regions"][0]["vpcs"]), 2)

    def test_pick_1_vpc_with_account_qualifier(self):
        """
        Pick 1 vpc with "205987878622:vpc-0173cdff453971939"
        """
        # pick VPC with account qualifier in 1st account
        vpcs = ["205987878622:vpc-0173cdff453971939"]
        comm.filterVpcInConfig(self.config, vpcs)
        self.assertDictEqual(
            self.config["account_info"][0]["regions"][0]["vpcs"][0],
            {"vpc_id": "vpc-0173cdff453971939"},
        )
        self.assertEqual(len(self.config["account_info"][1]["regions"][0]["vpcs"]), 0)

    def test_pick_1_vpc(self):
        """
        Pick 1 vpc with "vpc-045608ad8e0521589"
        """
        # pick a VPC in 2nd account
        vpcs = ["vpc-045608ad8e0521580"]
        comm.filterVpcInConfig(self.config, vpcs)
        self.assertEqual(len(self.config["account_info"][0]["regions"][0]["vpcs"]), 0)
        self.assertDictEqual(
            self.config["account_info"][1]["regions"][0]["vpcs"][0],
            {"vpc_id": "vpc-045608ad8e0521580"},
        )

    @patch('dm.commonlib.exit')
    def test_incorrect_vpc(self, mock_exit):
        """
        Pick 1 vpc with "vpc-045608ad8e0521589"
        """
        logger = logging.getLogger("dm.commonlib")
        # pick a VPC that does not exist in YAML
        vpcs = ["vpc-045608ad8e0521500"]
        with patch.object(logger,'error') as mock_error:
            comm.filterVpcInConfig(self.config, vpcs)
            mock_error.assert_called_with(
                "**Error** Cannot find the following VPC(s) in YAML: ['vpc-045608ad8e0521500']"
            )
            mock_exit.assert_called_once_with(1)

        #
        # Do NOT use the following assertion for SystemExit as
        # it will close stdio, resulting into
        #     ValueError: I/O operation on closed file
        # when running pdb:
        #
        # with self.assertRaises(SystemExit):
        #     comm.filterVpcInConfig(self.config, vpcs)
        #

if __name__ == "__main__":
    unittest.main()
