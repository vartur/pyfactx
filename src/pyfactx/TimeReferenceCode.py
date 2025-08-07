from enum import IntEnum


class TimeReferenceCode(IntEnum):
    """Time reference codes according to UN/EDIFACT code list 2005.
    
    These codes are used to specify the reference date context in business documents.
    The codes represent different types of dates that are relevant in business transactions,
    particularly in invoicing and delivery processes.

    References:
        UN/EDIFACT code list 2005: Date/time/period function code qualifier
        https://unece.org/trade/uncefact
    """

    INVOICE_DOCUMENT_ISSUE_DATE = 3
    ACTUAL_DELIVERY_DATE = 35
    PAID_TO_DATE = 432

    @property
    def description(self) -> str:
        """Gets the human-readable description of the time reference code.

        Returns:
            str: Description of the time reference code
        """
        return self._get_descriptions()[self]

    @classmethod
    def _get_descriptions(cls) -> dict['TimeReferenceCode', str]:
        """Internal method to get descriptions mapping.

        Returns:
            dict[TimeReferenceCode, str]: Mapping of time reference codes to their descriptions
        """
        return {
            cls.INVOICE_DOCUMENT_ISSUE_DATE: "Date when the invoice document was issued",
            cls.ACTUAL_DELIVERY_DATE: "Date when the goods or services were actually delivered",
            cls.PAID_TO_DATE: "Date up to which the payment has been made"
        }

    @classmethod
    def get_description(cls, code: int) -> str:
        """Gets the description for a given time reference code.

        Args:
            code: The time reference code to look up

        Returns:
            str: Description of the time reference code

        Raises:
            ValueError: If the code is not valid
        """
        try:
            return cls(code).description
        except ValueError:
            raise ValueError(f"Invalid time reference code: {code}")

    def is_invoice_related(self) -> bool:
        """Checks if the time reference is related to invoicing.

        Returns:
            bool: True if the reference is invoice-related
        """
        return self in (self.INVOICE_DOCUMENT_ISSUE_DATE,)

    def is_delivery_related(self) -> bool:
        """Checks if the time reference is related to delivery.

        Returns:
            bool: True if the reference is delivery-related
        """
        return self in (self.ACTUAL_DELIVERY_DATE,)

    def is_payment_related(self) -> bool:
        """Checks if the time reference is related to payment.

        Returns:
            bool: True if the reference is payment-related
        """
        return self in (self.PAID_TO_DATE,)

    @classmethod
    def from_code(cls, code: int) -> 'TimeReferenceCode':
        """Creates a TimeReferenceCode instance from an integer code.

        Args:
            code: The integer code to convert

        Returns:
            TimeReferenceCode: The corresponding enum instance

        Raises:
            ValueError: If the code is not valid
        """
        try:
            return cls(code)
        except ValueError:
            raise ValueError(f"Invalid time reference code: {code}")

    def __str__(self) -> str:
        """Returns a string representation of the time reference code.

        Returns:
            str: String representation including code and description
        """
        return f"{self.value} - {self.description}"