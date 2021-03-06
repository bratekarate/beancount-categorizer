# Beancount Categorizer

Decorator for beancount importers, providing automatic categorization of transactions. Greatly inspired by [smart_importer](https://github.com/beancount/smart_importer) and by [ledger-cli's payee subdirective for accounts](https://www.ledger-cli.org/3.0/doc/ledger3.html#Command-Directives).

Whilst the machine learning approach of smart_importer works great in most cases, one may miss ledger-cli's feature to apply categorization rules that are "set in stone". This importer does just that, categorizing payees of imported transactions to the appropriate accounts through user provided regular expressions.

## Installation

```sh
$ pip install git+https://github.com/bratekarate/beancount-categorizer.git
```
Currently there is only a development version. Releases and pip package are a work in progress.

## Usage

The categorizer allocates transactions to accounts according to user provided mappings. Any categorizer that implements the `ImporterHooks` interface can be applied through the `apply_hooks` decorator of smart_importer, which is a dependency of this categorizer.

The `PayeeCategorizer` is an `ImporterHook` implementation provided by this package. It is instantiated with a dictionary that configures what payee will be categorized to which account. Each account may have multiple payee regexes, where any transaction matched against one of the payee regexes will be categorized to the account.

The following example configuration uses the `PayeeCategorizer` to decorate the `ECImporter` of [beancount-dkb](https://github.com/siddhantgoel/beancount-dkb):

```python
from beancount_dkb import ECImporter
from beancount_categorizer import PayeeCategorizer
from smart_importer import apply_hooks

categorizer = PayeeCategorizer(
    {
        "Expenses:Foods:Groceries": ["^(SUPERMARKET XY|MY DELI)"],
    }
)

IBAN_NUMBER = "..."

CONFIG = [
    apply_hooks(
        ECImporter(
            IBAN_NUMBER,
            "Assets:Current:Checkings",
            file_encoding="iso-8859-1",
        ),
        [categorizer],
    ),
]
...
```

Matching CSV entries will produce transactions such as the following:

```beancount
2021-03-01 * "SUPERMARKET XY SAGT DANKE" "Shopping"
    Expenses:Food:Groceries
    Assets:DKB:EC                  -84.72 EUR

2021-03-01 * "MY DELI //LEIPZIG" "Shopping"
    Expenses:Food:Groceries
    Assets:DKB:EC                  -15.72 EUR
```

To get the best of both worlds, it is certainly possible (and encouraged) to use the categorizer in conjunction with smart_importer. Probably the most useful setup is to first use the categorizer to apply the predefined rules and then let the smart importer handle the uncategorized cases. This way the categorization rules are ensured to be applied, as the categorizer only adds a postings to the transaction if exactly one posting exists thus far.

The following configuration is an example of the combined use with smart_importer:

```python
from beancount_dkb import ECImporter, CreditImporter
from beancount_categorizer import PayeeCategorizer
from smart_importer import PredictPostings, apply_hooks

categorizer = PayeeCategorizer(
    {
        "Expenses:Foods:Groceries": ["^(SUPERMARKET XY|MY DELI)"],
    }
)

IBAN_NUMBER = "..."

CONFIG = [
    apply_hooks(
        ECImporter(
            IBAN_NUMBER,
            "Assets:Current:Checkings",
            file_encoding="iso-8859-1",
        ),
        [categorizer, PredictPostings()],
    ),
]
```
