# aib2ynab

[![PyPI](https://img.shields.io/pypi/v/aib2ynab.svg)](https://pypi.org/project/aib2ynab/)

[YNAB](https://www.ynab.com/) supports linking directly to an [AIB personal bank account](https://aib.ie/) via [TrueLayer](https://truelayer.com/). This command makes it a little easier to import transactions manually without linking your account.

It is possible to export a list of historical transactions from [AIB Personal Online Banking](https://aib.ie/) to a CSV file. You can use this command to then convert the CSV file from AIB into [a format required by YNAB](https://support.ynab.com/en_us/formatting-a-csv-file-an-overview-BJvczkuRq).



## Installation

Install this tool using `pipx`:
```bash
pipx install aib2ynab
```
## Usage

### Importing historical transactions

1. [Export](https://aib.ie/business/help-centre/manage-my-accounts/how-do-i-export-my-statements-transactions) a list of historical transactions from your AIB Personal Online Banking account to a CSV file.
2. Run `aib2ynab`, specifying the path to the transaction file that you downloaded from AIB & the path where you want the YNAB import file to be created.
3. Follow [the YNAB file-based import guide](https://support.ynab.com/en_us/file-based-import-a-guide-Bkj4Sszyo#import).
```bash
aib2ynab /path/to/transactions.csv ./path/to/ynab_import_file.csv
```

### Help
You can run the following command for help with the command's syntax.

```bash
aib2ynab --help
```

## Development
This project uses [Poetry](https://python-poetry.org/) for dependency and package management.

```bash
poetry install --with=dev
```
To run the tests:
```bash
poetry run pytest
```
To format using [Black](https://black.readthedocs.io/en/stable/):
```bash
poetry run black aib2ynab/ tests/
```

To run the command using Poetry:
```bash
poetry run aib2ynab /path/to/transactions.csv ./path/to/ynab_import_file.csv
```
