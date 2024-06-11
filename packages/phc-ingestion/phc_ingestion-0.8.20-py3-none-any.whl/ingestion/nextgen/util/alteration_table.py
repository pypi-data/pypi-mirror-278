from logging import Logger
import pandas as pd
import re
from typing import cast, Literal, TypedDict


short_variant_types: list[str] = [
    "Missense",
    "Frameshift",
    "Stop gained",
    "Stop lost",
    "Inframe deletion",
    "Inframe insertion",
    "Inframe",
    "Splice site",
    "Splice region",
    "Nonsense",
]


def extract_all_table_lines(xml_in_file: str) -> list[str]:
    with open(xml_in_file, "r") as f:
        xml_lines = f.readlines()

    in_range_trigger = False
    table_lines = []
    for line in xml_lines:
        if "Gene (Chr. Position, hg38)" in line:
            in_range_trigger = True
        if in_range_trigger:
            if "</Table>" in line:
                break
            table_lines.append(line)

    return table_lines


def extract_alteration_table(xml_in_file: str, log: Logger) -> pd.DataFrame:
    table_lines = extract_all_table_lines(xml_in_file)
    # Remove completely empty lines
    table_lines = [line for line in table_lines if line.strip() != ""]

    table_row_lines: list[list[str]] = []
    current_row: list[str] = []
    for line in table_lines:
        if line.strip() == "</TR>":
            if current_row:
                table_row_lines.append(current_row)
                current_row = []
        line = re.sub(r"<T.>", "", line)
        line = re.sub(r"</T.>", "", line)
        line = re.sub(r"<T./>", "", line)
        if line.strip() not in ["", "p."]:
            current_row.append(line.strip())

    gene_column = []
    type_column = []
    description_column = []
    vaf_column = []
    info_column = []

    for row in table_row_lines:
        gene_column.append(row[0])
        type_column.append(row[1])
        description_column.append(row[2])
        vaf_column.append(row[3])
        # Sometimes the info column is empty, so we need to check if it actually exists
        # So far, it seems like rows with empty "info" columns are generally not useful for us
        # and the data in them will not be used anywhere, so we just fill in an empty string
        if len(row) > 4:
            info_column.append(row[4])
        else:
            info_column.append("")

    # If the test is negative we will have a type column with only NA values
    # We return an empty df which we check for later when scraping annotations
    # Ignore the first row which is the header
    if set(type_column[1:]) == {"NA"}:
        log.info("Alteration table is empty")
        return pd.DataFrame()

    alteration_df = pd.DataFrame(
        {
            "gene": gene_column,
            "type": type_column,
            "description": description_column,
            "vaf": vaf_column,
            "info": info_column,
        }
    )

    return alteration_df


def extract_variant_table(
    xml_in_file: str, variant_type: Literal["copy number", "structural", "short"], log: Logger
) -> pd.DataFrame:
    alteration_table = extract_alteration_table(xml_in_file, log)
    if alteration_table.empty:
        return alteration_table

    # Drop by variant type
    if variant_type == "copy number":
        variant_df = alteration_table[alteration_table["type"] == "CNV"]
    elif variant_type == "structural":
        variant_df = alteration_table[alteration_table["type"] == "Translocation"]
    elif variant_type == "short":
        variant_df = alteration_table[alteration_table["type"].isin(short_variant_types)]

    return variant_df


class AlterationTableRow(TypedDict):
    gene: str
    type: str
    description: str
    vaf: str
    info: str


def extract_hyperdiploidy_row(xml_in_file: str, log: Logger) -> None | AlterationTableRow:
    alteration_table = extract_alteration_table(xml_in_file, log)
    if alteration_table.empty:
        return None

    hyperdiploidy_df = alteration_table[alteration_table["type"] == "Hyperdiploidy"]

    if hyperdiploidy_df.empty:
        return None
    # We only expect one hyperdiploidy row. If we get more than 1, just fail the ingestion so we can investigate
    if hyperdiploidy_df.shape[0] > 1:
        raise ValueError("More than one hyperdiploidy row found")

    hyperdiploidy_row = cast(AlterationTableRow, hyperdiploidy_df.iloc[0].to_dict())

    return hyperdiploidy_row
