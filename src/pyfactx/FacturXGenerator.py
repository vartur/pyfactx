import logging
import tempfile
from pathlib import Path
from typing import ClassVar

from lxml import etree as ET
from saxonche import PySaxonProcessor

from .FacturXData import FacturXData
from .InvoiceProfile import InvoiceProfile


class SchematronValidationError(Exception):
    """Exception raised when Schematron validation fails."""
    def __init__(self, failed_asserts: list[str], reports: list[str]):
        self.failed_asserts = failed_asserts
        self.reports = reports
        message = self._format_message()
        super().__init__(message)

    def _format_message(self) -> str:
        messages = []
        if self.failed_asserts:
            messages.append("Failed assertions:")
            messages.extend(f"  - {assertion}" for assertion in self.failed_asserts)
        if self.reports:
            messages.append("Validation reports:")
            messages.extend(f"  - {report}" for report in self.reports)
        return "\n".join(messages)


class FacturXGenerator:
    """Generator for Factur-X XML documents with Schematron validation.

    This class handles the generation and validation of Factur-X XML documents
    according to different profiles using XSLT-based Schematron validation.
    """

    # Base directory for resources
    BASE_DIR: ClassVar[Path] = Path(__file__).parent.resolve()

    # XSLT file locations for different profiles
    XSLT_LOCATIONS: ClassVar[dict[InvoiceProfile, str]] = {
        InvoiceProfile.MINIMUM: f"{BASE_DIR}/resources/0_minimum/_XSLT_MINIMUM/Factur-X_1.07.2_MINIMUM.xslt",
        InvoiceProfile.BASICWL: f"{BASE_DIR}/resources/1_basicwl/_XSLT_BASICWL/Factur-X_1.07.2_BASICWL.xslt",
        InvoiceProfile.BASIC: f"{BASE_DIR}/resources/2_basic/_XSLT_BASIC/Factur-X_1.07.2_BASIC.xslt",
        InvoiceProfile.EN16931: f"{BASE_DIR}/resources/3_en16931/_XSLT_EN16931/Factur-X_1.07.2_EN16931.xslt"
    }

    # XML namespaces
    SVRL_NS: ClassVar[dict[str, str]] = {'svrl': 'http://purl.oclc.org/dsdl/svrl'}

    @classmethod
    def generate(
        cls,
        factur_x_data: FacturXData,
        profile: InvoiceProfile,
        validate_xslt: bool = True
    ) -> ET.Element:
        """Generates and optionally validates a Factur-X XML document.

        Args:
            factur_x_data (FacturXData): The Factur-X data to generate XML from.
            profile (InvoiceProfile): The target profile for generation.
            validate_xslt (bool, optional): Whether to perform Schematron validation.
                Defaults to True.

        Returns:
            ET.Element: The generated XML document.

        Raises:
            NotImplementedError: If the EXTENDED profile is requested.
            FileNotFoundError: If the XSLT file for validation is not found.
            SchematronValidationError: If the generated XML fails validation.
            ValueError: If XML generation fails.
        """
        if profile == InvoiceProfile.EXTENDED:
            logging.error("The 'EXTENDED' profile is not implemented")
            raise NotImplementedError("The 'EXTENDED' profile is not supported yet")

        try:
            # Generate XML
            factur_x_xml = factur_x_data.to_xml("CrossIndustryInvoice", profile)

            # Perform validation if requested
            if validate_xslt:
                cls._validate_with_schematron(factur_x_xml, profile)

            return factur_x_xml

        except ET.XMLSyntaxError as e:
            raise ValueError(f"Failed to generate XML: {str(e)}")

    @classmethod
    def _validate_with_schematron(cls, xml: ET.Element, profile: InvoiceProfile) -> None:
        """Validates XML against Schematron rules using XSLT.

        Args:
            xml (ET.Element): The XML document to validate.
            profile (InvoiceProfile): The profile to use for validation.

        Raises:
            FileNotFoundError: If the XSLT file is not found.
            SchematronValidationError: If validation fails.
        """
        # Write XML to temporary file
        with tempfile.NamedTemporaryFile(
            mode="w+",
            encoding="utf-8",
            delete=False,
            suffix=".xml"
        ) as xml_file:
            xml_str = ET.tostring(
                xml,
                pretty_print=True,
                encoding="utf-8"
            ).decode('utf-8')
            xml_file.write(xml_str)
            xml_path = xml_file.name

        try:
            # Get XSLT path
            stylesheet_path = Path(cls.XSLT_LOCATIONS[profile]).resolve()
            if not stylesheet_path.exists():
                raise FileNotFoundError(
                    f"XSLT file not found: {stylesheet_path}"
                )

            # Perform XSLT transformation
            with PySaxonProcessor(license=False) as proc:
                xslt_proc = proc.new_xslt30_processor()
                xslt = xslt_proc.compile_stylesheet(
                    stylesheet_file=str(stylesheet_path)
                )
                result = xslt.transform_to_string(source_file=xml_path)

            # Parse validation results
            validation_result = cls._parse_svrl_result(result)
            if not validation_result.is_valid:
                raise SchematronValidationError(
                    validation_result.failed_asserts,
                    validation_result.reports
                )

            logging.info("XML validation successful")

        finally:
            # Clean up temporary file
            Path(xml_path).unlink(missing_ok=True)

    @classmethod
    def _parse_svrl_result(cls, svrl_xml: str) -> 'ValidationResult':
        """Parses SVRL validation results.

        Args:
            svrl_xml (str): The SVRL XML string to parse.

        Returns:
            ValidationResult: Object containing validation results.
        """
        tree = ET.fromstring(svrl_xml.encode('utf-8'))
        
        failed_asserts = [
            f"{el.attrib.get('location')}: "
            f"{el.findtext('svrl:text', namespaces=cls.SVRL_NS)}"
            for el in tree.findall('.//svrl:failed-assert', namespaces=cls.SVRL_NS)
        ]

        reports = [
            f"{el.attrib.get('location')}: "
            f"{el.findtext('svrl:text', namespaces=cls.SVRL_NS)}"
            for el in tree.findall('.//svrl:successful-report', namespaces=cls.SVRL_NS)
        ]

        return ValidationResult(
            is_valid=not (failed_asserts or reports),
            failed_asserts=failed_asserts,
            reports=reports
        )


class ValidationResult:
    """Container for Schematron validation results.

    Attributes:
        is_valid (bool): Whether validation passed.
        failed_asserts (list[str]): List of failed assertions.
        reports (list[str]): List of validation reports.
    """

    def __init__(
        self,
        is_valid: bool,
        failed_asserts: list[str],
        reports: list[str]
    ):
        self.is_valid = is_valid
        self.failed_asserts = failed_asserts
        self.reports = reports