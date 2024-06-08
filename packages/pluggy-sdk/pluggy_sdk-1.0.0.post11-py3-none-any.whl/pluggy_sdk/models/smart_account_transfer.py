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
from pluggy_sdk.models.payment_recipient import PaymentRecipient
from pluggy_sdk.models.smart_account import SmartAccount
from typing import Optional, Set
from typing_extensions import Self

class SmartAccountTransfer(BaseModel):
    """
    Transfer made with money from a smart account
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Primary identifier of the transfer")
    client_id: Optional[StrictStr] = Field(default=None, description="Primary identifier of the client associated to the transfer", alias="clientId")
    client_payment_id: Optional[StrictStr] = Field(default=None, description="Primary identifier of the client payment associated to the transfer", alias="clientPaymentId")
    amount: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Transfer amount")
    status: Optional[StrictStr] = Field(default=None, description="Transfer status")
    created_at: Optional[datetime] = Field(default=None, description="Transfer creation date", alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, description="Transfer last update date", alias="updatedAt")
    smart_account: Optional[SmartAccount] = Field(default=None, alias="smartAccount")
    payment_recipient: Optional[PaymentRecipient] = Field(default=None, alias="paymentRecipient")
    __properties: ClassVar[List[str]] = ["id", "clientId", "clientPaymentId", "amount", "status", "createdAt", "updatedAt", "smartAccount", "paymentRecipient"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['IN_PROGRESS', 'COMPLETED', 'ERROR']):
            raise ValueError("must be one of enum values ('IN_PROGRESS', 'COMPLETED', 'ERROR')")
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
        """Create an instance of SmartAccountTransfer from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of smart_account
        if self.smart_account:
            _dict['smartAccount'] = self.smart_account.to_dict()
        # override the default output from pydantic by calling `to_dict()` of payment_recipient
        if self.payment_recipient:
            _dict['paymentRecipient'] = self.payment_recipient.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SmartAccountTransfer from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "clientId": obj.get("clientId"),
            "clientPaymentId": obj.get("clientPaymentId"),
            "amount": obj.get("amount"),
            "status": obj.get("status"),
            "createdAt": obj.get("createdAt"),
            "updatedAt": obj.get("updatedAt"),
            "smartAccount": SmartAccount.from_dict(obj["smartAccount"]) if obj.get("smartAccount") is not None else None,
            "paymentRecipient": PaymentRecipient.from_dict(obj["paymentRecipient"]) if obj.get("paymentRecipient") is not None else None
        })
        return _obj


