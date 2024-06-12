from wizlib.parser import WizParser

from busy.command import QueueCommand
from busy.model.item import Item


class AddCommand(QueueCommand):

    timed = True

    description: str = ""
    name = 'add'
    key = 'a'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--description', '-d', nargs='?')

    def handle_vals(self):
        super().handle_vals()
        if not self.provided('description'):
            self.description = self.app.ui.get_text('Description: ')
            # edited = self.ui.edit_items(self.collection, self.selection)

    @QueueCommand.wrap
    def execute(self):
        if self.description:
            item = Item(self.description)
            self.collection.append(item)
            self.status = "Added: " + self.description
        else:
            self.status = "Nothing added"

    # @CollectionCommand.wrap
    # def execute(self):
    #     if not self.selection:
    #         self.status = "Edited nothing"
    #     else:
    #         edited = self.ui.edit_items(self.collection, self.selection)
    #         self.status = f"Edited {self.count(edited)}"
