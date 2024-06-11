from ingestion.nextgen.util.alteration_table import extract_hyperdiploidy_row

from logging import Logger
import re


def parse_pattern(pattern: str, line: str, name: str) -> str:
    regex = re.compile(pattern)
    match = regex.match(line)

    if not match:
        raise ValueError(f"Could not parse {name} from line")

    return match.group(1).strip()


def parse_indication(line: str) -> str:
    return parse_pattern(r"^.*Reason for Referral:(.*?)(Patient|<).*$", line, "indication")


def parse_ordering_md(line: str) -> str:
    return parse_pattern(r"^.*Physician Name:(.*?)(Reason|<).*$", line, "ordering MD")


def parse_patient_name(line: str) -> str:
    return parse_pattern(r"^.*Patient Name: (.*?)(Accession|<).*$", line, "patient name")


def parse_sample_number(line: str) -> str:
    return parse_pattern(r"^.*Specimen #: (\d*) .*$", line, "sample number")


def parse_body_site(line: str) -> str:
    return parse_pattern(r"^.*Specimen:(.*?)(Age|Birthdate|<).*$", line, "body site")


def parse_report_id(line: str) -> str:
    return parse_pattern(r"^.*Accession #: (.*?) .*$", line, "report ID")


def parse_report_date(line: str) -> str:
    return parse_pattern(
        r"^.*Diagnostic Genomics Laboratory.*(\d{2}\/\d{2}\/\d{4}).*$", line, "report date"
    )


def extract_hyperdiploidy_chromosomes(xml_in_file: str, log: Logger) -> list[str] | None:
    hyperdiploidy_row_dict = extract_hyperdiploidy_row(xml_in_file, log)

    if not hyperdiploidy_row_dict:
        return None

    return re.findall(r"\d+", hyperdiploidy_row_dict["gene"])
