# mbank-csv-export

Many projects successfully attempt to parse the crappy mBank CSV operations, but few reliably automate the extraction process. 

This library does only one thing - exports transaction CSV files from mBank as a string.
 - Uses Playwright for automated browser interactions.
 - Saves browser state to maintain session continuity, minimizing the need for repeated mobile authentication.

# Usage

## Library
```python
from datetime import date

from mbank_csv_export import MBank

mbank = MBank(headless=False)
mbank.login(username="1111222233334444", password="***")
csv_content: str = mbank.export_operations_csv(
    date_from=date(2023, 6, 1), 
    date_to=date(2024, 6, 1)
)
print(csv_content)
```

## CLI
```sh
> mbank --help
usage: mbank [-h] [--headless] [--username USERNAME] [--password PASSWORD] [--log-level {ERROR,WARN,INFO,DEBUG}] [--date-from DATE_FROM] [--date-to DATE_TO] [--verbose]

options:
  -h, --help            show this help message and exit
  --headless
  --username USERNAME   or set MBANK_USERNAME env variable
  --password PASSWORD   or set MBANK_PASSWORD env variable
  --log-level {ERROR,WARN,INFO,DEBUG}
                        or set MBANK_LOG_LEVEL env variable
  --date-from DATE_FROM
                        format YYYY-MM-DD, defaults to date 1 month ago.
  --date-to DATE_TO     format YYYY-MM-DD, defaults to date today.
  --verbose
```

## Contribute
Pull requests and issues are highly appreciated. To add your changes:
  1) Fork the repository.
  2) Create a new branch for your feature or bugfix (git checkout -b feature-name).
  3) Commit your changes (git commit -m 'Add some feature').
  4) Push to the branch (git push origin feature-name).
  5) Open a pull request on GitHub.
