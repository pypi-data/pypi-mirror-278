from wizlib.parser import WizParser
from wizlib.command import CommandCancellation

from busy.command import QueueCommand
from busy.model.item import Item
from busy.util import date_util
from busy.util.date_util import relative_date


class DoneCommand(QueueCommand):
    """Combined the old defer and finish commands"""

    timed = True

    name = 'done'
    key = 'z'

    yes: bool = None
    iterate: str = ''

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--iterate', '-i')
        cls.add_yes_arg(parser)

    @property
    def plan_date(self):
        return relative_date(self.iterate) \
            if self.iterate else None

    def handle_vals(self):
        super().handle_vals()
        if self.selection:
            items = self.collection.items(self.selection)
            if not self.provided('iterate'):
                repeats = set(i.repeat for i in items)
                if len(repeats) > 1:
                    raise CommandCancellation(
                        'Items have different repeat values')
                self.iterate = next(iter(repeats)) if repeats else None
            if not self.provided('yes'):
                self.app.ui.send('\n'.join([str(i) for i in items]))

                def iterate_action():
                    self.iterate = self.app.ui.get_text(
                        "Iterate: ", [], (self.iterate or "tomorrow"))
                while not self.provided('yes'):
                    intro = "Done"
                    if self.plan_date:
                        intro += f" and iterate on {self.plan_date}"
                        iterate_action.name = 'other'
                        iterate_action.key = 'o'
                    else:
                        iterate_action.name = 'iterate'
                        iterate_action.key = 'i'
                    self.confirm(intro, iterate_action)

    @property
    def date(self):
        """Absolute date for iteration"""
        # Don't cache this!
        return date_util.relative_date(self.iteration)

    @QueueCommand.wrap
    def execute(self):
        if not self.selection:
            self.status = "Did nothing"
        elif self.yes is False:
            self.status = "Unconfirmed"  # TODO: Use cancelation
        else:
            date = date_util.today()
            dones = self.app.storage.get_collection(self.queue, 'done')
            plans = self.app.storage.get_collection(self.queue, 'plan')
            items = self.collection.delete(self.selection)
            nexts = [i.done(done_date=date_util.today(),
                            plan_date=self.plan_date) for i in items]
            nexts = [n for n in nexts if n]
            dones += items
            plans += nexts
            self.status = "Done"
