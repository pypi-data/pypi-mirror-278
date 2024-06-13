import glob
import os
import traceback

import click
import pandas as pd

from lib_holdings_simplified.api import ApiSession


@click.command()
@click.option("--start", default=0, type=int, help="Position of OCN to start with.")
@click.argument("infile_ocns", required=True, type=click.Path(exists=True))
@click.argument("infile_symb", required=True, type=click.Path(exists=True))
@click.argument("out_folder", required=True)
@click.option(
    "--key", prompt="Your OCLC API key", help="OCLC API key.", hide_input=True
)
@click.option(
    "--secret", prompt="Your OCLC API secret", help="OCLC API secret.", hide_input=True
)
def main(**kwargs):
    # create output folder (if it does not exist already)
    if not os.path.exists(kwargs.get("out_folder")):
        os.makedirs(kwargs.get("out_folder"), exist_ok=True)
    ocns = list(
        pd.read_csv(kwargs.get("infile_ocns"), header=None, dtype=object)
        .iloc[:, 0]
        .unique()
    )
    symbols = list(
        pd.read_csv(kwargs.get("infile_symb"), header=None, dtype=object)
        .iloc[:, 0]
        .unique()
    )
    scopes = [
        "wcapi:change_password",
        "wcapi:view_retained_holdings",
        "wcapi:view_summary_holdings",
        "wcapi:view_holdings",
        "wcapi:view_bib",
        "wcapi:view_my_holdings",
        "wcapi:view_brief_bib",
        "wcapi:view_institution_holdings",
    ]
    session = ApiSession(kwargs.get("key"), kwargs.get("secret"), scopes)
    # break up into smaller batches
    n = 100
    error = False
    # store temporary files here:
    if not os.path.exists(f'{kwargs.get("out_folder")}/temp'):
        os.makedirs(f'{kwargs.get("out_folder")}/temp')
    for i in range(kwargs.get("start"), len(ocns), n):
        try:
            click.echo(f"fetch data for batch {i}-{i+n}")
            ocns_sub = ocns[i : i + n]
            holdings = transform_holdings(session.extract_holdings(ocns_sub, symbols))
            print("holdings extracted")
            # record_types = transform_records(session.extract_record_type(ocns_sub))
            # print('record types extracted')
            # holdings = holdings.merge(record_types, how='left')
            # store temporary batch
            holdings.to_csv(
                f'{kwargs.get("out_folder")}/temp/{i}-{i+n}.csv', index=False
            )
        except Exception as e:
            click.echo(traceback.format_exc())
            click.echo(
                f"{e}\n{e.__class__}\nerror in batch {i}-{i+n}.\ntry again with start = {i}"
            )
            error = True
            break
    # merge the sub-batches
    if not error:
        table_big = pd.DataFrame()
        for file in glob.glob(f'{kwargs.get("out_folder")}/temp/*.csv'):
            table_big = pd.concat([table_big, pd.read_csv(file)])
            os.remove(file)  # then remove the temporary file
        table_big.to_csv(f'{kwargs.get("out_folder")}/holdings.csv', index=False)


def transform_holdings(data):
    ocns = []
    holdings = []
    for item in data:
        holding = item["briefRecords"][0]["institutionHolding"]
        ocns.append(item["briefRecords"][0]["oclcNumber"])
        holdings.append(holding["totalHoldingCount"])
    return pd.DataFrame({"ocn": ocns, "holdings": holdings}, dtype=object)


def transform_records(records):
    ocns = []
    record_types = []
    for ocn in records:
        if len(records[ocn]) > 0:
            ocns.append(ocn)
            record_types.append(records[ocn][0]["recordType"])
            # the multiple entries are holdings
    return pd.DataFrame({"ocn": ocns, "recordType": record_types}, dtype=object)


if __name__ == "__main__":
    main()
