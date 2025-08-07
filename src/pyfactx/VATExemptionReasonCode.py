from enum import StrEnum


class VATExemptionReasonCode(StrEnum):
    """VAT exemption reason codes based on EU VAT Directive articles.
    
    These codes identify specific legal bases for VAT exemptions according to
    EU VAT regulations and directives. The codes are structured as follows:
    
    - VATEX-EU-XXX: Main article number
    - VATEX-EU-XXX-YY: Specific paragraph or point within the article
    
    Main categories:
    - Article 79: Special provisions
    - Article 132: Exemptions for certain activities in public interest
    - Article 143: Exemptions on importation
    - Article 148: Exemptions for international transport
    - Article 151: Exemptions for diplomatic and international bodies
    - Article 159: Agricultural exemptions
    - Article 309: Special provisions
    - Special codes (AE, D, F, G, etc.): Other specific cases
    - Country-specific codes (e.g., FR for France)
    """

    # Article 79 - Special provisions
    VATEX_EU_79_C = "VATEX-EU-79-C"  # Reduction of taxable amount

    # Article 132 - Exemptions for certain activities in public interest
    VATEX_EU_132 = "VATEX-EU-132"      # General public interest exemption
    VATEX_EU_132_1A = "VATEX-EU-132-1A"  # Public postal services
    VATEX_EU_132_1B = "VATEX-EU-132-1B"  # Hospital and medical care
    VATEX_EU_132_1C = "VATEX-EU-132-1C"  # Medical treatment
    VATEX_EU_132_1D = "VATEX-EU-132-1D"  # Human blood and organs
    VATEX_EU_132_1E = "VATEX-EU-132-1E"  # Dental technicians
    VATEX_EU_132_1F = "VATEX-EU-132-1F"  # Cost-sharing groups
    VATEX_EU_132_1FA = "VATEX-EU-132-1FA"  # Additional cost-sharing provisions
    VATEX_EU_132_1G = "VATEX-EU-132-1G"  # Social security and welfare
    VATEX_EU_132_1H = "VATEX-EU-132-1H"  # Child and youth protection
    VATEX_EU_132_1I = "VATEX-EU-132-1I"  # Education
    VATEX_EU_132_1J = "VATEX-EU-132-1J"  # Private tuition
    VATEX_EU_132_1K = "VATEX-EU-132-1K"  # Religious services
    VATEX_EU_132_1L = "VATEX-EU-132-1L"  # Non-profit organizations
    VATEX_EU_132_1M = "VATEX-EU-132-1M"  # Sport services
    VATEX_EU_132_1N = "VATEX-EU-132-1N"  # Cultural services
    VATEX_EU_132_1O = "VATEX-EU-132-1O"  # Public broadcasting
    VATEX_EU_132_1P = "VATEX-EU-132-1P"  # Public authorities
    VATEX_EU_132_1Q = "VATEX-EU-132-1Q"  # Fundraising events

    # Article 143 - Exemptions on importation
    VATEX_EU_143 = "VATEX-EU-143"      # General import exemption
    VATEX_EU_143_1A = "VATEX-EU-143-1A"  # Final importation of goods
    VATEX_EU_143_1B = "VATEX-EU-143-1B"  # Reimportation of goods
    VATEX_EU_143_1C = "VATEX-EU-143-1C"  # Services related to imports
    VATEX_EU_143_1D = "VATEX-EU-143-1D"  # Transport services
    VATEX_EU_143_1E = "VATEX-EU-143-1E"  # Import of gas/electricity
    VATEX_EU_143_1F = "VATEX-EU-143-1F"  # Import of monetary gold
    VATEX_EU_143_1FA = "VATEX-EU-143-1FA"  # Additional import provisions
    VATEX_EU_143_1G = "VATEX-EU-143-1G"  # Import by diplomatic bodies
    VATEX_EU_143_1H = "VATEX-EU-143-1H"  # NATO imports
    VATEX_EU_143_1I = "VATEX-EU-143-1I"  # Import of caught fish
    VATEX_EU_143_1J = "VATEX-EU-143-1J"  # Port services
    VATEX_EU_143_1K = "VATEX-EU-143-1K"  # Import of investment gold
    VATEX_EU_143_1L = "VATEX-EU-143-1L"  # Special import arrangements

    # Article 144 - Special import provisions
    VATEX_EU_144 = "VATEX-EU-144"  # Special import arrangements

    # Article 146 - Export exemptions
    VATEX_EU_146_1E = "VATEX-EU-146-1E"  # Export-related services

    # Article 148 - International transport exemptions
    VATEX_EU_148 = "VATEX-EU-148"      # General transport exemption
    VATEX_EU_148_A = "VATEX-EU-148-A"  # Sea vessels
    VATEX_EU_148_B = "VATEX-EU-148-B"  # Aircraft
    VATEX_EU_148_C = "VATEX-EU-148-C"  # Supplies for vessels
    VATEX_EU_148_D = "VATEX-EU-148-D"  # Navigation services
    VATEX_EU_148_E = "VATEX-EU-148-E"  # War vessels
    VATEX_EU_148_F = "VATEX-EU-148-F"  # Vessel modifications
    VATEX_EU_148_G = "VATEX-EU-148-G"  # Fueling and provisioning

    # Article 151 - Diplomatic and international bodies
    VATEX_EU_151 = "VATEX-EU-151"        # General diplomatic exemption
    VATEX_EU_151_1A = "VATEX-EU-151-1A"  # Diplomatic missions
    VATEX_EU_151_1AA = "VATEX-EU-151-1AA"  # Additional diplomatic provisions
    VATEX_EU_151_1B = "VATEX-EU-151-1B"  # International organizations
    VATEX_EU_151_1C = "VATEX-EU-151-1C"  # NATO forces
    VATEX_EU_151_1D = "VATEX-EU-151-1D"  # UK forces in Cyprus
    VATEX_EU_151_1E = "VATEX-EU-151-1E"  # Other armed forces

    # Article 159 - Agricultural provisions
    VATEX_EU_159 = "VATEX-EU-159"  # Agricultural exemptions

    # Article 309 - Special schemes
    VATEX_EU_309 = "VATEX-EU-309"  # Special schemes

    # Special codes
    VATEX_EU_AE = "VATEX-EU-AE"  # Reverse charge
    VATEX_EU_D = "VATEX-EU-D"    # Distance sales
    VATEX_EU_F = "VATEX-EU-F"    # Farmers flat rate
    VATEX_EU_G = "VATEX-EU-G"    # Gold investment
    VATEX_EU_I = "VATEX-EU-I"    # Intra-Community supply
    VATEX_EU_IC = "VATEX-EU-IC"  # Intra-Community acquisition
    VATEX_EU_J = "VATEX-EU-J"    # Services article 44
    VATEX_EU_O = "VATEX-EU-O"    # Outside scope

    # Country-specific codes (France)
    VATEX_FR_FRANCHISE = "VATEX-FR-FRANCHISE"  # French VAT franchise
    VATEX_FR_CNWVAT = "VATEX-FR-CNWVAT"       # French VAT not within scope

    @classmethod
    def get_public_interest_codes(cls) -> set['VATExemptionReasonCode']:
        """Returns all exemption codes related to activities in public interest (Article 132)."""
        return {code for code in cls if code.name.startswith('VATEX_EU_132')}

    @classmethod
    def get_import_codes(cls) -> set['VATExemptionReasonCode']:
        """Returns all exemption codes related to imports (Article 143)."""
        return {code for code in cls if code.name.startswith('VATEX_EU_143')}

    @classmethod
    def get_transport_codes(cls) -> set['VATExemptionReasonCode']:
        """Returns all exemption codes related to international transport (Article 148)."""
        return {code for code in cls if code.name.startswith('VATEX_EU_148')}

    @classmethod
    def get_diplomatic_codes(cls) -> set['VATExemptionReasonCode']:
        """Returns all exemption codes related to diplomatic arrangements (Article 151)."""
        return {code for code in cls if code.name.startswith('VATEX_EU_151')}

    def get_article_number(self) -> str:
        """Returns the article number from the VAT exemption code.
        
        Returns:
            str: The article number or 'SPECIAL' for special codes
        """
        parts = self.value.split('-')
        if len(parts) < 3:
            return "SPECIAL"
        return parts[2].split('_')[0]

    def __str__(self) -> str:
        """Returns a human-readable string representation."""
        return self.value.replace('-', ' ')