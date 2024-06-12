

from wizlib.parser import WizParser

from busy.command import QueueCommand
from busy.model.item import Item
from busy.util import date_util
from busy.util.date_util import relative_date


class FinishCommand(QueueCommand):
    """Mark a task as finished by moving it to the done queue"""

    yes: bool = None
    name = 'finish'
    key = 'n'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        cls.add_yes_arg(parser)

    def handle_vals(self):
        super().handle_vals()
        super().handle_vals()
        if self.selection:
            if not self.provided('yes'):
                items = self.collection.items(self.selection)
                self.app.ui.send('\n'.join([str(i) for i in items]))
                intro = f"Finish {self.count()}"
                self.confirm(intro)

    @QueueCommand.wrap
    def execute(self):
        if not self.selection:
            self.status = "Finished nothing"
        elif self.yes is False:
            self.status = "Finish operation unconfirmed"
        else:
            date = date_util.today()
            dones = self.app.storage.get_collection(self.queue, 'done')
            plans = self.app.storage.get_collection(self.queue, 'plan')
            items = self.collection.delete(self.selection)
            finished = [Item(i.current, state='done',
                             done_date=date_util.today()) for i in items]
            nexts = [Item(i.next, state='todo') for i in items
                     if (i.next and not i.repeat)]
            repeats = [Item(i.description, state='plan',
                            plan_date=i.repeat_date)
                       for i in items if i.repeat]
            dones += finished
            self.collection[0:0] = nexts
            plans += repeats
            self.status = f"Finished {self.count(finished)}"
            self.status += f" / Added {self.count(nexts)}"
            self.status += f" / Planned {self.count(repeats)}"
