from decimal import Decimal
from typing import Optional, override
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Annotated

from .namespaces import NAMESPACES, RAM
from .InvoiceProfile import InvoiceProfile
from .TradeAllowanceCharge import TradeAllowanceCharge
from .UnitCode import UnitCode
from .XMLBaseModel import XMLBaseModel


class TradePrice(XMLBaseModel):
    """Represents a trade price according to UN/CEFACT standards.
    
    This class models pricing information including the base amount,
    quantity, unit of measure, and any applied allowances or charges.
    
    Attributes:
        charge_amount: The monetary amount for the price
        quantity: The basis quantity for the price (e.g., price per unit)
        unit: The unit of measure for the quantity
        applied_trade_allowance_charge: Any allowance or charge applied to this price
    """

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True
    )

    charge_amount: Annotated[
        float,
        Field(
            description="Price amount",
            gt=0,
            examples=["100.00", "1234.5678"]
        )
    ]

    quantity: Optional[Annotated[
        float,
        Field(
            description="Basis quantity for the price",
            gt=0,
            examples=["1.000", "12.500"]
        )
    ]] = None

    unit: Optional[UnitCode] = Field(
        default=None,
        description="Unit of measure for the quantity"
    )

    applied_trade_allowance_charge: Optional[TradeAllowanceCharge] = Field(
        default=None,
        description="Allowance or charge applied to this price"
    )

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade price to XML representation.

        Creates an XML element representing the price according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing the price

        Example:
            ```xml
            <ram:GrossPriceProductTradePrice>
                <ram:ChargeAmount>100.00</ram:ChargeAmount>
                <ram:BasisQuantity unitCode="C62">1.000</ram:BasisQuantity>
                <ram:AppliedTradeAllowanceCharge>...</ram:AppliedTradeAllowanceCharge>
            </ram:GrossPriceProductTradePrice>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ChargeAmount
        amount_str = f"{self.charge_amount:.4f}"
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ChargeAmount").text = amount_str

        # BasisQuantity
        if self.quantity is not None:
            attrib = {"unitCode": str(self.unit)} if self.unit else {}
            quantity_str = f"{self.quantity:.3f}"
            ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}BasisQuantity",
                attrib=attrib
            ).text = quantity_str

        # AppliedTradeAllowanceCharge
        if self.applied_trade_allowance_charge:
            root.append(
                self.applied_trade_allowance_charge.to_xml(
                    "AppliedTradeAllowanceCharge",
                    profile
                )
            )

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the trade price
        """
        parts = [f"Amount: {self.charge_amount:.4f}"]
        if self.quantity is not None:
            parts.append(f"Quantity: {self.quantity:.3f}")
            if self.unit:
                parts.append(f"Unit: {self.unit}")
        if self.applied_trade_allowance_charge:
            parts.append(f"Allowance/Charge: {self.applied_trade_allowance_charge}")
        return " | ".join(parts)
