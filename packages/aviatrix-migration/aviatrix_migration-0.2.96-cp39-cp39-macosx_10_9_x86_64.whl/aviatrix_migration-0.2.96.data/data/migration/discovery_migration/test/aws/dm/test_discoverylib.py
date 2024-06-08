import unittest
import json
import logging
from unittest.mock import patch
from unittest.mock import Mock
from dm.discoverylib import DiscoveryLib as dl
import pdb


class CheckAz(unittest.TestCase):

    def setUp(self):
        with open("test/fixtures/aws_az.json") as f:
            self.available_az = json.load(f)

    def test_find_az(self):
        ec2_client = Mock()
        ec2_client.describe_availability_zones.return_value = self.available_az
        azs = dl.checkAz(ec2_client, "us-east-1", ["a", "b"])
        self.assertListEqual(azs, ["us-east-1a", "us-east-1b"])

    def test_log_error(self):
        logger = logging.getLogger("dm.discoverylib")
        ec2_client = Mock()
        ec2_client.describe_availability_zones.return_value = self.available_az
        with patch.object(logger, "error") as mock_error:
            _ = dl.checkAz(ec2_client, "us-east-1", ["g"])
            mock_error.assert_called_with(
                "  **Alert** us-east-1g is not available in us-east-1"
            )

    def test_with_empty_zone(self):
        ec2_client = Mock()
        azs = dl.checkAz(ec2_client, "us-east-1", [])
        self.assertListEqual(azs, [])


class DiscoverAz(unittest.TestCase):

    def setUp(self):
        with open("test/fixtures/aws_subnet.json") as f:
            self.subnets = json.load(f)

    @patch('dm.discoverylib.exit')
    def test_exit(self, mock_exit):
        logger = logging.getLogger("dm.discoverylib")
        ec2_client = Mock()
        ec2_client.describe_subnets.return_value = {"Subnets": []}
        with patch.object(logger,"error") as mock_error:
            _ = dl.discoverAz(
                ec2_client,
                routeTables=None,
                vpc=Mock(),
                gw_zones=[],
                attachmentSubnet=[],
                az_needed=2,
            )
            mock_error.assert_called_with(
                "  **Error** number of AZs needed 2 > SUM(suggested AZs in gw_zones 0, other AZs found with private subnet 0)"
            )
            mock_exit.assert_called_once_with(1)        


if __name__ == "__main__":
    unittest.main()
