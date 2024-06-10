import csv
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def convert(input_file, output_file):
    """Converts AIB transactions CSV to YNAB import format."""
    reader = csv.DictReader(input_file, skipinitialspace=True)
    reader.fieldnames = (
        "Posted Account",
        "Posted Transactions Date",
        "Description1",
        "Description2",
        "Description3",
        "Debit Amount",
        "Credit Amount",
        "Balance",
        "Posted Currency",
        "Transaction Type",
        "Local Currency Amount",
        "Local Currency",
    )
    writer = csv.DictWriter(
        output_file, fieldnames=["Date", "Payee", "Memo", "Outflow", "Inflow"]
    )
    writer.writeheader()
    next(reader)  # skip headers
    for row in reader:
        writer.writerow(
            {
                "Date": row["Posted Transactions Date"],
                "Payee": row["Description1"],
                "Memo": row["Description2"],
                "Outflow": row["Debit Amount"],
                "Inflow": row["Credit Amount"],
            }
        )
    click.echo("Successfully converted file.")
