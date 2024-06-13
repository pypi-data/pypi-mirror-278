from logging import Logger
from typing import Optional


def filter_caris_liquid_line(line: Optional[str], log: Logger) -> Optional[str]:
    # Parse INFO column and filter by TLOD >= 4, MBQ >= 30, MMQ >= 20, MPOS >= 9
    # Extract AF and filter by AF >= 0.001
    # Assume we won't know if gene is lineage-relevant and use more permissive filters
    if not line:
        return None

    working_line = line.split("\t")
    # Confirm that the line has the expected number of columns
    if len(working_line) != 10:
        raise RuntimeError(f"Line in CarisLiquid VCF has {len(working_line)} columns, expected 10")

    # Split INFO column into dictionary
    info_dict = {}
    items = working_line[7].split(";")
    for item in items:
        # Skip synonymous mutations which have protein changes coded like this: PC=C172=
        if item.count("=") == 1:
            key, value = item.split("=")
            key = key.strip()
            info_dict[key] = value
    # Filter by TLOD >= 4 (Caris uses 6.3 for not-lineage-relevant genes)
    if "TLOD" in info_dict:
        try:
            if float(info_dict["TLOD"]) < 4:
                return None
        except ValueError:
            log.error(f"Could not convert TLOD value to type float: TLOD={info_dict['TLOD']}")
            return None

    # Filter by MBQ >= 30 (MBQ has two values, check both)
    if "MBQ" in info_dict:
        nums = info_dict["MBQ"].split(",")
        try:
            if float(nums[0]) < 30 and float(nums[1]) < 30:
                return None
        except ValueError:
            log.error(f"Could not convert MBQ values to type float: MBQ={info_dict['MBQ']}")
            return None
    # Filter by MMQ >= 20 (MMQ has two values, check both)
    if "MMQ" in info_dict:
        nums = info_dict["MMQ"].split(",")
        try:
            if float(nums[0]) < 20 and float(nums[1]) < 20:
                return None
        except ValueError:
            log.error(f"Could not convert MMQ values to type float: MMQ={info_dict['MMQ']}")
            return None
    # Filter by MPOS >= 9
    if "MPOS" in info_dict:
        try:
            if float(info_dict["MPOS"]) < 9:
                return None
        except ValueError:
            log.error(f"Could not convert MPOS value to type float: MPOS={info_dict['MPOS']}")
            return None

    # Extract AF and filter by AF >= 0.001 (Caris uses 0.005 for not-lineage-relevant genes)
    format_col = working_line[8].split(":")
    vals = working_line[9].split(":")
    vals_dict = dict(zip(format_col, vals))
    if "AF" in vals_dict:
        try:
            if float(vals_dict["AF"]) < 0.001:
                return None
        except ValueError:
            log.error(f"Could not convert AF value to type float: AF={vals_dict['AF']}")
            return None
    return line
