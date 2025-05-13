from enum import StrEnum


class UnitCode(StrEnum):
    # Length
    KILOMETRE = "KMT"
    METRE = "MTR"
    DECIMETRE = "DMT"
    CENTIMETRE = "CMT"
    MILLIMETRE = "MMT"

    # Area
    SQUARE_METRE = "MTK"
    SQUARE_DECIMETRE = "DMK"
    SQUARE_CENTIMETRE = "CMK"

    # Volume
    CUBIC_METRE = "MTQ"
    CUBIC_DECIMETRE = "DMQ"
    LITRE = "LTR"
    DECILITRE = "DLT"
    CENTILITRE = "CLT"
    CUBIC_CENTIMETRE = "CMQ"
    MILLILITRE = "MLT"

    # Weight
    TONNE = "TNE"
    KILOGRAM = "KGM"
    HECTOGRAM = "HGM"
    GRAM = "GRM"
    MILLIGRAM = "MGM"

    # Time
    YEAR = "ANN"
    QUARTER = "QAN"
    MONTH = "MON"
    WEEK = "WEE"
    DAY = "DAY"
    HOUR = "HUR"
    MINUTE = "MIN"
    SECOND = "SEC"

    # Energy
    MEGAWATT_HOUR = "MWH"
    KILOWATT_HOUR = "KWH"

    # Information
    GIGABYTE = "E34"
    MEGABYTE = "4L"

    # Unit/piece
    ONE = "C62"
    EACH = "EA"
    PIECE = "H87"
    NUMBER_OF_ARTICLES = "NAR"

    # Special concept
    BATCH = "5B"
    DOZEN = "DZN"
    KIT = "KT"
    LUMP_SUM = "LS"
    PAIR = "PR"
    SET = "SET"
    UNPACKAGED = "XNE"

    # Package type
    AEROSOL = "XAE"
    AMPOULE = "XAM"
    CAPSULE = "XAV"
    BARREL = "XBA"
    BOARD = "XBD"
    BUNDLE = "XBE"
    BAG = "XBG"
    BUCKET = "XBJ"
    BASKET = "XBK"
    BALE = "XBL"
    BOTTLE = "XBO"
    BOX = "XBX"
    CAN = "XCA"
    CAGE = "XCG"
    CARD = "XCM"
    CRATE = "XCR"
    CASE = "XCS"
    CARTON = "XCT"
    CUP = "XCU"
    CAGE_ROLL = "XCW"
    CYLINDER = "XCY"
    ENVELOPE = "XEN"
    JUG = "XJG"
    JAR = "XJR"
    NET = "XNT"
    PALLET_BOX = "XPB"
    PACKAGE = "XPK"
    TRAY = "XPU"
    PALLET = "XPX"
    RACK = "XRK"
    REEL = "XRL"
    ROLL = "XRO"
    SACK = "XSA"
    SKELETON_CASE = "XSK"
    SHEET = "XST"
    SHRINK_WRAPPED = "XSW"
    SLEEVE = "XSY"
    TUBE = "XTU"
    TANK = "XTY"
    VACUUM_PACKED = "XVP"
    WRAP = "XWR"
