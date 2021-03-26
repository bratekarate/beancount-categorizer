class ImporterHook:
    """Interface for an importer hook."""

    def __call__(self, importer, file, imported_entries, existing_entries):
        """Apply the hook and modify the imported entries.

        Args:
            importer: The importer that this hooks is being applied to.
            file: The file that is being imported.
            imported_entries: The current list of imported entries.
            existing_entries: The existing entries, as passed to the extract
                function.

        Returns:
            The updated imported entries.
        """
        raise NotImplementedError
