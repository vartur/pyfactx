import logging
import tempfile
from .FacturXData import FacturXData
from .InvoiceProfile import InvoiceProfile
from lxml import etree as ET
from typing import ClassVar
from saxonche import PySaxonProcessor
from pathlib import Path


class FacturXGenerator:
    BASE_DIR = Path(__file__).parent.resolve()
    XSLT_LOCATIONS: ClassVar[dict[InvoiceProfile, str]] = {
        InvoiceProfile.MINIMUM: f"{BASE_DIR}/resources/0_minimum/_XSLT_MINIMUM/Factur-X_1.07.2_MINIMUM.xslt",
        InvoiceProfile.BASICWL: f"{BASE_DIR}/resources/1_basicwl/_XSLT_BASICWL/Factur-X_1.07.2_BASICWL.xslt",
        InvoiceProfile.BASIC: f"{BASE_DIR}/resources/2_basic/_XSLT_BASIC/Factur-X_1.07.2_BASIC.xslt",
        InvoiceProfile.EN16931: f"{BASE_DIR}/resources/3_en16931/_XSLT_EN16931/Factur-X_1.07.2_EN16931.xslt"
    }

    @classmethod
    def generate(cls, factur_x_data: FacturXData, profile: InvoiceProfile, validate_xslt: bool = True) -> ET.Element:
        if profile == InvoiceProfile.EXTENDED:
            logging.warning("The 'EXTENDED' profile has not been implemented yet")
            raise NotImplemented

        root_element_name = "CrossIndustryInvoice"
        factur_x_xml = factur_x_data.to_xml(root_element_name, profile)

        if validate_xslt:
            def is_svrl_valid(svrl_xml: str):
                svrl_ns = {'svrl': 'http://purl.oclc.org/dsdl/svrl'}
                tree = ET.fromstring(svrl_xml.encode('utf-8'))
                failed_asserts = tree.findall('.//svrl:failed-assert', namespaces=svrl_ns)
                reports = tree.findall(".//svrl:successful-report", namespaces=svrl_ns)
                for el in failed_asserts:
                    print(f"[FAILED ASSERT] {el.attrib.get('location')}: {el.findtext('svrl:text', namespaces=svrl_ns)}")

                for el in reports:
                    print(f"[REPORT] {el.attrib.get('location')}: {el.findtext('svrl:text', namespaces=svrl_ns)}")

                return len(failed_asserts) == 0 and len(reports) == 0

            with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".xml") as xml_file:
                xml_str = ET.tostring(factur_x_xml, pretty_print=True, encoding="utf-8").decode('utf-8')
                xml_file.write(xml_str)
                xml_path = xml_file.name

            with PySaxonProcessor(license=False) as proc:
                xslt_proc = proc.new_xslt30_processor()
                stylesheet_path = Path(cls.XSLT_LOCATIONS[profile]).resolve()
                if not stylesheet_path.exists():
                    raise FileNotFoundError(f"XSLT not found at: {stylesheet_path}")
                xslt = xslt_proc.compile_stylesheet(stylesheet_file=str(stylesheet_path))
                result = xslt.transform_to_string(source_file=xml_path)
                if is_svrl_valid(result):
                    print(f"✅ XML is valid according to Schematron")
                else:
                    print(f"❌ XML is NOT valid according to Schematron")

        return factur_x_xml
