RAM = "ram"
RSM = "rsm"
UDT = "udt"
QDT = "qdt"
XSI = "xsi"

NAMESPACES = {
    RSM: "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
    RAM: "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
    QDT: "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
    UDT: "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
    XSI: "http://www.w3.org/2001/XMLSchema-instance"
}

QUALIFIED = {prefix: f"{{{uri}}}" for prefix, uri in NAMESPACES.items()}
