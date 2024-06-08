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

from pluggy_sdk.api.category_api import CategoryApi


class TestCategoryApi(unittest.TestCase):
    """CategoryApi unit test stubs"""

    def setUp(self) -> None:
        self.api = CategoryApi()

    def tearDown(self) -> None:
        pass

    def test_categories_list(self) -> None:
        """Test case for categories_list

        List
        """
        pass

    def test_categories_retrieve(self) -> None:
        """Test case for categories_retrieve

        Retrieve
        """
        pass

    def test_client_category_rules_create(self) -> None:
        """Test case for client_category_rules_create

        Create Category Rule
        """
        pass

    def test_client_category_rules_list(self) -> None:
        """Test case for client_category_rules_list

        List Category Rules
        """
        pass


if __name__ == '__main__':
    unittest.main()
