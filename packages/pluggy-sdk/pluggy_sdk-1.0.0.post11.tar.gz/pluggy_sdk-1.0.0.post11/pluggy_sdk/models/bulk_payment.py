# coding: utf-8

"""
    Pluggy API

    Pluggy's main API to review data and execute connectors

    The version of the OpenAPI document: 1.0.0
    Contact: hello@pluggy.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from pluggy_sdk.models.payment_request import PaymentRequest
from pluggy_sdk.models.payment_request_callback_urls import PaymentRequestCallbackUrls
from pluggy_sdk.models.smart_account import SmartAccount
from typing import Optional, Set
from typing_extensions import Self

class BulkPayment(BaseModel):
    """
    Response with information related to a bulk payment
    """ # noqa: E501
    id: StrictStr = Field(description="Primary identifier")
    total_amount: Union[StrictFloat, StrictInt] = Field(description="Total amount of all requests associated with the bulk payment", alias="totalAmount")
    status: StrictStr = Field(description="Bulk payment status")
    created_at: datetime = Field(description="Date when the payment request was created", alias="createdAt")
    updated_at: datetime = Field(description="Date when the payment request was updated", alias="updatedAt")
    callback_urls: Optional[PaymentRequestCallbackUrls] = Field(default=None, alias="callbackUrls")
    payment_url: StrictStr = Field(description="URL to begin the payment intent creation flow for this payment request", alias="paymentUrl")
    payment_requests: List[PaymentRequest] = Field(description="List of payment requests associated with the bulk payment", alias="paymentRequests")
    smart_account: SmartAccount = Field(description="Smart account associated with the bulk payment", alias="smartAccount")
    __properties: ClassVar[List[str]] = ["id", "totalAmount", "status", "createdAt", "updatedAt", "callbackUrls", "paymentUrl", "paymentRequests", "smartAccount"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['CREATED', 'PAYMENT_IN_PROGRESS', 'TOP_UP_IN_PROGRESS', 'COMPLETED', 'PARTIALLY_COMPLETED', 'ERROR']):
            raise ValueError("must be one of enum values ('CREATED', 'PAYMENT_IN_PROGRESS', 'TOP_UP_IN_PROGRESS', 'COMPLETED', 'PARTIALLY_COMPLETED', 'ERROR')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of BulkPayment from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of callback_urls
        if self.callback_urls:
            _dict['callbackUrls'] = self.callback_urls.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in payment_requests (list)
        _items = []
        if self.payment_requests:
            for _item in self.payment_requests:
                if _item:
                    _items.append(_item.to_dict())
            _dict['paymentRequests'] = _items
        # override the default output from pydantic by calling `to_dict()` of smart_account
        if self.smart_account:
            _dict['smartAccount'] = self.smart_account.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BulkPayment from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "totalAmount": obj.get("totalAmount"),
            "status": obj.get("status"),
            "createdAt": obj.get("createdAt"),
            "updatedAt": obj.get("updatedAt"),
            "callbackUrls": PaymentRequestCallbackUrls.from_dict(obj["callbackUrls"]) if obj.get("callbackUrls") is not None else None,
            "paymentUrl": obj.get("paymentUrl"),
            "paymentRequests": [PaymentRequest.from_dict(_item) for _item in obj["paymentRequests"]] if obj.get("paymentRequests") is not None else None,
            "smartAccount": SmartAccount.from_dict(obj["smartAccount"]) if obj.get("smartAccount") is not None else None
        })
        return _obj


