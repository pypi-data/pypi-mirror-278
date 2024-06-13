from dataclasses import dataclass, field
from typing import List, Optional

from sgrspecification.generic.data_point import DataPointBase
from sgrspecification.generic.functional_profile import FunctionalProfileBase
from sgrspecification.product.messaging_types import (
    MessagingDataPointConfiguration,
    MessagingInterfaceDescription,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class MessagingDataPoint(DataPointBase):
    messaging_data_point_configuration: Optional[
        MessagingDataPointConfiguration
    ] = field(
        default=None,
        metadata={
            "name": "messagingDataPointConfiguration",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        },
    )


@dataclass
class MessageDataPointList:
    """
    List of data points.
    """

    data_point_list_element: List[MessagingDataPoint] = field(
        default_factory=list,
        metadata={
            "name": "dataPointListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        },
    )


@dataclass
class MessagingFunctionalProfile(FunctionalProfileBase):
    data_point_list: Optional[MessageDataPointList] = field(
        default=None,
        metadata={
            "name": "dataPointList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        },
    )


@dataclass
class MessagingFunctionalProfileList:
    """
    List of functional profiles.
    """

    functional_profile_list_element: List[MessagingFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "name": "functionalProfileListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        },
    )


@dataclass
class MessagingInterface:
    """
    Container for a modbus device.
    """

    messaging_interface_description: Optional[
        MessagingInterfaceDescription
    ] = field(
        default=None,
        metadata={
            "name": "messagingInterfaceDescription",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        },
    )
    functional_profile_list: Optional[MessagingFunctionalProfileList] = field(
        default=None,
        metadata={
            "name": "functionalProfileList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        },
    )
