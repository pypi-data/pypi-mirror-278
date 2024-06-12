from datetime import datetime

from wizlib.command import WizCommand
from wizlib.parser import WizParser
from wizlib.ui import Choice, Chooser
from wizlib.command import CommandCancellation

from busy.model.collection import Collection


class BusyCommand(WizCommand):

    default = 'simple'
    timed = False

    # TODO: Move to wizlib
    @staticmethod
    def add_yes_arg(parser: WizParser):
        parser.add_argument('--yes', '-y', action='store_true', default=None)

    # TODO: Move to wizlib
    def confirm(self, verb, *other_actions):
        """Ensure that a command is confirmed by the user"""
        if self.provided('yes'):
            return self.yes
        else:
            def cancel():
                raise CommandCancellation('Cancelled')
            chooser = Chooser(f"{verb}?", 'OK', [
                Choice('OK', '\n', True),
                Choice('cancel', 'c', cancel)
            ])
            for action in other_actions:
                name = action.name if hasattr(action, 'name') else 'other'
                key = action.key if hasattr(action, 'key') else 'o'
                chooser.add_choice(name, key, action)
            choice = self.app.ui.get_option(chooser)
            if type(choice) is bool:
                self.yes = choice
            return choice


class QueueCommand(BusyCommand):
    """Base for commands that work on the default collection of one queue"""

    queue: str = 'tasks'
    collection_state: str = 'todo'
    filter: list = None
    default_filter = [1]

    @property
    def collection(self):
        """Return the collection object being queried, usually todo"""
        if not hasattr(self, '_collection'):
            self._collection = self.app.storage.get_collection(
                self.queue, self.collection_state)
        return self._collection

    @property
    def selection(self):
        """Indices of objects within the query collection that match the
        filter"""
        if not hasattr(self, '_selection'):
            self._selection = self.collection.select(*self.filter)
        return self._selection

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('queue', default='tasks', nargs='?')
        parser.add_argument('--filter', '-f', action='store', nargs="*")

    def handle_vals(self):
        """Apply default filter"""
        super().handle_vals()
        if not self.provided('filter'):
            self.filter = self.default_filter

    @BusyCommand.wrap
    def execute(self, method, *args, **kwargs):
        """Execute the command then save the collection(s)"""
        if self.timed and self.queue == 'tasks':
            todos = self.app.storage.get_collection('tasks', 'todo')
            if len(todos) > 0:
                todos[0].update_time()
        result = method(self, *args, **kwargs)
        if self.timed and self.queue == 'tasks':
            todos = self.app.storage.get_collection('tasks', 'todo')
            if len(todos) > 0:
                todos[0].start_timer()
        self.app.storage.save()
        return result

    def count(self, items=None):
        """Return a friendly string count of some items"""
        if items is None:
            items = self.selection
        if len(items) == 1:
            return "1 item"
        if len(items) > 1:
            return str(len(items)) + " items"
        return "nothing"


class CollectionCommand(QueueCommand):
    """Base for commands that work on a user-specified collection"""

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        states = Collection.family_attrs('state')
        parser.add_argument(
            '--state', '-s', action='store', default='todo',
            dest='collection_state', choices=states)

    def output_items(self, func, with_index=False):
        """Return some attribute of all the items in the collection"""
        collection = self.app.storage.get_collection(
            self.queue, self.collection_state)
        indices = collection.select(*self.filter)
        if indices:
            if with_index:
                return '\n'.join([func(collection[i], i) for i in indices])
            else:
                return '\n'.join([func(collection[i]) for i in indices])
        else:
            self.status = f"Queue '{self.queue}' has " + \
                f"no {self.collection_state} items"
