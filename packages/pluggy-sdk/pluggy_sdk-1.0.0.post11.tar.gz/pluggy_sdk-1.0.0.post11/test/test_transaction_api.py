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

from pluggy_sdk.api.transaction_api import TransactionApi


class TestTransactionApi(unittest.TestCase):
    """TransactionApi unit test stubs"""

    def setUp(self) -> None:
        self.api = TransactionApi()

    def tearDown(self) -> None:
        pass

    def test_transactions_list(self) -> None:
        """Test case for transactions_list

        List
        """
        pass

    def test_transactions_retrieve(self) -> None:
        """Test case for transactions_retrieve

        Retrieve
        """
        pass

    def test_transactions_update(self) -> None:
        """Test case for transactions_update

        Update
        """
        pass


if __name__ == '__main__':
    unittest.main()
