from enum import StrEnum


class UnitCode(StrEnum):
    """Unit codes based on UN/ECE Recommendation 20 and UN/CEFACT.
    
    This enumeration defines standardized codes for units of measurement
    used in international trade and business documents.
    
    The codes are organized into the following categories:
    - Length units (e.g., metre, kilometre)
    - Area units (e.g., square metre)
    - Volume units (e.g., litre, cubic metre)
    - Weight/Mass units (e.g., kilogram, tonne)
    - Time units (e.g., hour, day)
    - Energy units (e.g., kilowatt hour)
    - Information units (e.g., gigabyte)
    - Count units (e.g., piece, each)
    - Special concepts (e.g., batch, set)
    - Package types (e.g., box, pallet)
    """

    # region Length Units
    KILOMETRE = "KMT"  # kilometre
    METRE = "MTR"      # metre
    DECIMETRE = "DMT"  # decimetre
    CENTIMETRE = "CMT" # centimetre
    MILLIMETRE = "MMT" # millimetre
    # endregion

    # region Area Units
    SQUARE_METRE = "MTK"      # square metre
    SQUARE_DECIMETRE = "DMK"  # square decimetre
    SQUARE_CENTIMETRE = "CMK" # square centimetre
    # endregion

    # region Volume Units
    CUBIC_METRE = "MTQ"       # cubic metre
    CUBIC_DECIMETRE = "DMQ"   # cubic decimetre
    CUBIC_CENTIMETRE = "CMQ"  # cubic centimetre
    LITRE = "LTR"            # litre
    DECILITRE = "DLT"        # decilitre
    CENTILITRE = "CLT"       # centilitre
    MILLILITRE = "MLT"       # millilitre
    # endregion

    # region Weight/Mass Units
    TONNE = "TNE"      # metric ton (1000 kg)
    KILOGRAM = "KGM"   # kilogram
    HECTOGRAM = "HGM"  # hectogram (100 g)
    GRAM = "GRM"       # gram
    MILLIGRAM = "MGM"  # milligram
    # endregion

    # region Time Units
    YEAR = "ANN"     # year
    QUARTER = "QAN"  # quarter (of a year)
    MONTH = "MON"    # month
    WEEK = "WEE"     # week
    DAY = "DAY"      # day
    HOUR = "HUR"     # hour
    MINUTE = "MIN"   # minute
    SECOND = "SEC"   # second
    # endregion

    # region Energy Units
    MEGAWATT_HOUR = "MWH"  # megawatt hour
    KILOWATT_HOUR = "KWH"  # kilowatt hour
    # endregion

    # region Information Units
    GIGABYTE = "E34"  # gigabyte
    MEGABYTE = "4L"   # megabyte
    # endregion

    # region Count Units
    ONE = "C62"                  # one (unit)
    EACH = "EA"                  # each
    PIECE = "H87"                # piece
    NUMBER_OF_ARTICLES = "NAR"   # number of articles
    # endregion

    # region Special Concepts
    BATCH = "5B"       # batch
    DOZEN = "DZN"      # dozen (12)
    KIT = "KT"         # kit
    LUMP_SUM = "LS"    # lump sum
    PAIR = "PR"        # pair
    SET = "SET"        # set
    UNPACKAGED = "XNE" # unpackaged/bulk
    # endregion

    # region Package Types
    AEROSOL = "XAE"         # aerosol
    AMPOULE = "XAM"         # ampoule
    CAPSULE = "XAV"         # capsule
    BARREL = "XBA"          # barrel
    BOARD = "XBD"           # board
    BUNDLE = "XBE"          # bundle
    BAG = "XBG"            # bag
    BUCKET = "XBJ"         # bucket
    BASKET = "XBK"         # basket
    BALE = "XBL"           # bale
    BOTTLE = "XBO"         # bottle
    BOX = "XBX"            # box
    CAN = "XCA"            # can
    CAGE = "XCG"           # cage
    CARD = "XCM"           # card
    CRATE = "XCR"          # crate
    CASE = "XCS"           # case
    CARTON = "XCT"         # carton
    CUP = "XCU"            # cup
    CAGE_ROLL = "XCW"      # cage roll
    CYLINDER = "XCY"       # cylinder
    ENVELOPE = "XEN"       # envelope
    JUG = "XJG"            # jug
    JAR = "XJR"            # jar
    NET = "XNT"            # net
    PALLET_BOX = "XPB"     # pallet box
    PACKAGE = "XPK"        # package
    TRAY = "XPU"           # tray
    PALLET = "XPX"         # pallet
    RACK = "XRK"           # rack
    REEL = "XRL"           # reel
    ROLL = "XRO"           # roll
    SACK = "XSA"           # sack
    SKELETON_CASE = "XSK"  # skeleton case
    SHEET = "XST"          # sheet
    SHRINK_WRAPPED = "XSW" # shrink wrapped
    SLEEVE = "XSY"         # sleeve
    TUBE = "XTU"           # tube
    TANK = "XTY"           # tank
    VACUUM_PACKED = "XVP"  # vacuum packed
    WRAP = "XWR"           # wrap
    # endregion

    @classmethod
    def get_si_units(cls) -> set['UnitCode']:
        """Returns a set of SI (International System of Units) unit codes.

        Returns:
            set[UnitCode]: Set of SI unit codes
        """
        return {
            cls.METRE, cls.KILOGRAM, cls.SECOND,
            cls.SQUARE_METRE, cls.CUBIC_METRE,
            cls.LITRE, cls.GRAM
        }

    @classmethod
    def get_volume_units(cls) -> set['UnitCode']:
        """Returns a set of volume unit codes.

        Returns:
            set[UnitCode]: Set of volume unit codes
        """
        return {
            cls.CUBIC_METRE, cls.CUBIC_DECIMETRE,
            cls.CUBIC_CENTIMETRE, cls.LITRE,
            cls.DECILITRE, cls.CENTILITRE,
            cls.MILLILITRE
        }

    @classmethod
    def get_weight_units(cls) -> set['UnitCode']:
        """Returns a set of weight unit codes.

        Returns:
            set[UnitCode]: Set of weight unit codes
        """
        return {
            cls.TONNE, cls.KILOGRAM, cls.HECTOGRAM,
            cls.GRAM, cls.MILLIGRAM
        }

    def is_packaging(self) -> bool:
        """Checks if the unit code represents a packaging type.

        Returns:
            bool: True if the unit is a packaging type
        """
        return self.value.startswith('X') and len(str(self.value)) == 3

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: The name of the unit in lowercase with underscores replaced by spaces
        """
        return self.name.lower().replace('_', ' ')