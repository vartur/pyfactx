from .FacturXMinimum import FacturXMinimum
from .InvoiceProfile import InvoiceProfile


class FacturXBasicWL(FacturXMinimum):
    profile = InvoiceProfile.BASICWL
