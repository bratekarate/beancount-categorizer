import re
from beancount.core import data
from .hooks import ImporterHook


class PayeeCategorizer(ImporterHook):
    def __init__(self, categories):
        self.categories = categories

    def __call__(self, importer, file, imported_entries, existing_entries):
        return [self.process_entry(entry) for entry in imported_entries]

    def process_entry(self, entry):
        for category in self.categories:
            for payee in self.categories[category]:
                if re.match(payee, (entry.payee or entry.narration)):
                    entry.postings.append(
                        data.Posting(
                            category,
                            None,
                            None,
                            None,
                            None,
                            None,
                        )
                    )
                    return entry
        return entry
