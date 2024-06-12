
from wizlib.parser import WizParser

from busy.command import CollectionCommand


class DeleteCommand(CollectionCommand):

    yes: bool = None
    name = 'delete'
    key = 'd'
    default_filter = [1]

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--yes', action='store_true', default=None)

    def handle_vals(self):
        super().handle_vals()
        super().handle_vals()
        if self.selection:
            items = self.collection.items(self.selection)
            self.app.ui.send('\n'.join([str(i) for i in items]))
            self.confirm(f"Delete {self.count()}")

    # Assume the indices have been already set, before confirmation.

    @CollectionCommand.wrap
    def execute(self):
        if self.yes:
            deleted = self.collection.delete(self.selection)
            self.status = f"Deleted {self.count(deleted)}"
        else:
            self.status = "Delete command canceled"
