from wizlib.parser import WizParser

from busy.command import QueueCommand
from busy.util import date_util


class DeferCommand(QueueCommand):

    timing: str = ""
    yes: bool = None
    name = 'defer'
    key = 'f'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--timing', '-t', default='tomorrow')
        cls.add_yes_arg(parser)

    def handle_vals(self):
        super().handle_vals()

        def update_deferral():
            self.timing = self.app.ui.get_text("Timing: ", [], "tomorrow")
        if self.selection:
            items = self.collection.items(self.selection)
            self.app.ui.send('\n'.join([str(i) for i in items]))
            if not self.provided('timing'):
                self.timing = 'tomorrow'
            while not self.provided('yes'):
                intro = f"Defer {self.count()} to {self.date}"
                self.confirm(intro, update_deferral)

    @property
    def date(self):
        """Absolute date for deferral"""
        # Don't cache this!
        return date_util.relative_date(self.timing)

    @QueueCommand.wrap
    def execute(self):
        if not self.selection:
            self.status = "Deferred nothing"
        elif self.yes is False:
            self.status = "Defer operation unconfirmed"
        else:
            plans = self.app.storage.get_collection(self.queue, 'plan')
            deferred = self.collection.delete(self.selection)
            for item in deferred:
                item.plan_date = self.date
                item.state = 'plan'
            plans.extend(deferred)
            self.status = f"Deferred {self.count(deferred)} to {self.date}"
