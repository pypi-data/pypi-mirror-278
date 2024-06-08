# coding: utf-8

"""
    Pluggy API

    Pluggy's main API to review data and execute connectors

    The version of the OpenAPI document: 1.0.0
    Contact: hello@pluggy.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pluggy_sdk.models.smart_account_balance import SmartAccountBalance

class TestSmartAccountBalance(unittest.TestCase):
    """SmartAccountBalance unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SmartAccountBalance:
        """Test SmartAccountBalance
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SmartAccountBalance`
        """
        model = SmartAccountBalance()
        if include_optional:
            return SmartAccountBalance(
                last_updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                balance = 1.337,
                blocked_balance = 1.337,
                scheduled_balance = 1.337
            )
        else:
            return SmartAccountBalance(
                last_updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                balance = 1.337,
                blocked_balance = 1.337,
                scheduled_balance = 1.337,
        )
        """

    def testSmartAccountBalance(self):
        """Test SmartAccountBalance"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
