

from wizlib.parser import WizParser

from busy.command import CollectionCommand
from busy.util.checklist import Checklist


class PrintCommand(CollectionCommand):
    """Generate a Checklist PDF"""

    full: bool = False
    default_filter = ["1-"]
    name = "print"

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--long', '-l', action='store_true')

    @CollectionCommand.wrap
    def execute(self):
        checklist = Checklist()
        collection = self.app.storage.get_collection(
            self.queue, self.collection_state)
        indices = collection.select(*self.filter)
        if indices:
            if self.long:
                items = [collection[i].description for i in indices]
            else:
                items = [collection[i].base for i in indices]
        else:
            self.status = f"Queue '{self.queue}' has " + \
                f"no {self.collection_state} items that meet the filter"
        queue = self.queue.capitalize()
        state = self.collection_state.capitalize()
        filter = (": "+",".join(self.filter)) \
            if (self.filter != self.default_filter) else ""
        title = f"{queue} ({state}{filter})"
        checklist.generate(title, items)
