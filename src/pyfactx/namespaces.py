"""XML namespace definitions for Factur-X/EN16931 invoice standard.

This module contains the XML namespace definitions used in the Factur-X (EN16931)
electronic invoice standard. These namespaces are essential for creating valid
XML documents that conform to the Cross Industry Invoice (CII) specifications.

Constants:
    RAM: Namespace prefix for Reusable Aggregate Business Information Entities
    RSM: Namespace prefix for Reference Semantic Model
    UDT: Namespace prefix for Unqualified Data Types
    QDT: Namespace prefix for Qualified Data Types
    XSI: Namespace prefix for XML Schema Instance

    NAMESPACES: Dictionary mapping namespace prefixes to their URIs
    QUALIFIED: Dictionary mapping namespace prefixes to their qualified (bracketed) URIs

Example:
    >>> from namespaces import NAMESPACES, RAM
    >>> print(NAMESPACES[RAM])
    'urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100'
"""

# Namespace prefixes
RAM = "ram"  # Reusable Aggregate Business Information Entities
RSM = "rsm"  # Reference Semantic Model
UDT = "udt"  # Unqualified Data Types
QDT = "qdt"  # Qualified Data Types
XSI = "xsi"  # XML Schema Instance

# Mapping of namespace prefixes to their URIs
NAMESPACES = {
    RSM: "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
    RAM: "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
    QDT: "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
    UDT: "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
    XSI: "http://www.w3.org/2001/XMLSchema-instance"
}

# Qualified versions of namespaces (with brackets) for direct XML use
QUALIFIED = {prefix: f"{{{uri}}}" for prefix, uri in NAMESPACES.items()}


def get_qualified_name(prefix: str, local_name: str) -> str:
    """Creates a fully qualified XML name using namespace prefix and local name.

    Args:
        prefix: Namespace prefix (e.g., 'ram', 'rsm')
        local_name: Local part of the element name

    Returns:
        str: Fully qualified name in Clark notation

    Raises:
        KeyError: If the prefix is not found in NAMESPACES

    Examples:
        >>> get_qualified_name('ram', 'ID')
        '{urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100}ID'
    """
    if prefix not in NAMESPACES:
        raise KeyError(f"Unknown namespace prefix: {prefix}")
    return f"{QUALIFIED[prefix]}{local_name}"


def is_valid_namespace(uri: str) -> bool:
    """Checks if a URI is a valid Factur-X namespace.

    Args:
        uri: URI to validate

    Returns:
        bool: True if the URI is a valid Factur-X namespace

    Examples:
        >>> is_valid_namespace(NAMESPACES[RAM])
        True
        >>> is_valid_namespace('invalid:uri')
        False
    """
    return uri in NAMESPACES.values()


def get_prefix_for_uri(uri: str) -> str:
    """Gets the namespace prefix for a given URI.

    Args:
        uri: Namespace URI

    Returns:
        str: Corresponding namespace prefix

    Raises:
        ValueError: If the URI is not found in NAMESPACES

    Examples:
        >>> get_prefix_for_uri(NAMESPACES[RAM])
        'ram'
    """
    for prefix, namespace_uri in NAMESPACES.items():
        if namespace_uri == uri:
            return prefix
    raise ValueError(f"Unknown namespace URI: {uri}")