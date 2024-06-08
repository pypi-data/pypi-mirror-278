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

from pluggy_sdk.models.update_payment_recipient import UpdatePaymentRecipient

class TestUpdatePaymentRecipient(unittest.TestCase):
    """UpdatePaymentRecipient unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UpdatePaymentRecipient:
        """Test UpdatePaymentRecipient
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UpdatePaymentRecipient`
        """
        model = UpdatePaymentRecipient()
        if include_optional:
            return UpdatePaymentRecipient(
                tax_number = '',
                name = '',
                payment_institution_id = '',
                account = {},
                is_default = True
            )
        else:
            return UpdatePaymentRecipient(
        )
        """

    def testUpdatePaymentRecipient(self):
        """Test UpdatePaymentRecipient"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
