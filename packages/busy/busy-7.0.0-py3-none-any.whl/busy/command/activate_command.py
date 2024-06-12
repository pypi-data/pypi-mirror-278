from wizlib.parser import WizParser

from busy.command import QueueCommand
from busy.util import date_util


def is_today_or_earlier(plan):
    return plan.plan_date <= date_util.today()


class ActivateCommand(QueueCommand):

    timed = True

    timing: str = ""
    yes: bool = None
    collection_state: str = 'plan'
    name = 'activate'
    key = 'c'
    default_filter = [is_today_or_earlier]

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        # parser.add_argument('--timing', '-t', default='today')
        cls.add_yes_arg(parser)

    def handle_vals(self):
        super().handle_vals()
        # def update_timing():
        #     self.timing = self.app.ui.get_text("Timing", "today")
        super().handle_vals()
        # For now, handling filter as normal
        if self.selection:
            if not self.provided('yes'):
                items = self.collection.items(self.selection)
                self.app.ui.send('\n'.join([str(i) for i in items]))
                intro = f"Activate {self.count()}"
                # self.confirm(intro, update_timing)
                self.confirm(intro)

    @QueueCommand.wrap
    def execute(self):
        if not self.selection:
            self.status = "Activated nothing"
        elif self.yes is False:
            self.status = "Activate command canceled"
        else:
            todos = self.app.storage.get_collection(self.queue)
            activated = self.collection.delete(self.selection)
            for item in activated:
                item.state = 'todo'
            todos.extend(activated)
            self.status = f"Activated {self.count()}"
