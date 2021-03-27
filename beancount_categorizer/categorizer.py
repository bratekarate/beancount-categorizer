import re
from beancount.core import data
from smart_importer.hooks import ImporterHook


class PayeeCategorizer(ImporterHook):
    def __init__(self, categories):
        self.categories = categories

    def __call__(self, importer, file, imported_entries, existing_entries):
        return [
            self._process(entry) or entry for entry in imported_entries
        ]

    def _process(self, entry):
        if type(entry) != data.Transaction or len(entry.postings) != 1:
            return

        for category in self.categories:
            for payee in self.categories[category]:
                if re.match(payee, (entry.payee or entry.narration)):
                    posting = data.Posting(
                        category,
                        None,
                        None,
                        None,
                        None,
                        None,
                    )

                    if entry.postings[0].units.number > 0:
                        entry.postings.append(posting)
                    else:
                        entry.postings.insert(0, posting)

                    return entry
