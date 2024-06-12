import re
from dataclasses import KW_ONLY, dataclass
from datetime import date, datetime

from busy.util.date_util import absolute_date
from busy.util.date_util import relative_date
from busy.util import date_util


class ItemStateError(Exception):
    pass


START_TIME_FORMAT = '%Y%m%d%H%M'


@dataclass
class Item:

    description: str
    _: KW_ONLY
    state: str = 'todo'
    done_date: date = None
    plan_date: date = None

    def __str__(self):
        """Represent the item as its simple form"""
        return self.simple

    def restricted(*allowed_states):
        """Restrict a method to a specific set of states"""
        def wrapper(method):
            def replacement(self, *args, **kwargs):
                if self.state in allowed_states:
                    return method(self, *args, **kwargs)
                else:
                    raise ItemStateError
            return replacement
        return wrapper

    FOLLOW_SPLIT = re.compile(r'\s*\-*\>\s*')
    REPEAT = re.compile(r'^\s*repeat(?:\s+[io]n)?\s+(.+)\s*$', re.I)

    def __setattr__(self, name, value):
        if self.__annotations__[name] == date:
            value = absolute_date(value)
        super().__setattr__(name, value)

    @property
    def first(self):
        return self.FOLLOW_SPLIT.split(self.description, maxsplit=1)[0]

    @property
    def _words(self):
        return self.first.split()

    @property
    def tags(self):
        wins = [w for w in self._words if w.startswith("#")]
        return {w[1:].lower() for w in wins}

    @property
    def resource(self):
        wins = [w for w in self._words if w.startswith("@")]
        return wins.pop()[1:] if wins else ""

    @property
    def data(self):
        return {w[1]: w[2:] for w in self._words if w.startswith("!")}

    @property
    def start_time(self):
        if 's' in self.data:
            return datetime.strptime(self.data['s'], START_TIME_FORMAT)

    @property
    def elapsed_time(self):
        if 'e' in self.data:
            return int(self.data['e'])
        else:
            return 0

    @property
    def base(self):
        """Current description with no tags, resource, or data"""
        wins = [w for w in self._words if w[0] not in '#@!']
        return " ".join(wins)

    @property
    def simple(self):
        """Base plus tags"""
        wins = [w for w in self._words if w[0] not in '@!']
        return " ".join(wins)

    @property
    def next(self):
        """Second and successive segments, all but current"""
        split = self.FOLLOW_SPLIT.split(self.description, maxsplit=1)
        if len(split) > 1:
            return split[1]
        else:
            return ""

    @property
    def current(self):
        """The first segment, all but next"""
        split = self.FOLLOW_SPLIT.split(self.description, maxsplit=1)
        if split:
            return split[0]
        else:
            return ""

    @property
    def repeat(self):
        followon = self.next
        match = self.REPEAT.match(followon)
        if match:
            return match.group(1)
        else:
            return ""

    @property
    def repeat_date(self):
        repeat = self.repeat
        if repeat:
            return relative_date(repeat)

    @restricted('todo')
    def done(self, done_date: date, plan_date: date = None):
        """Updates the item to done and returns a copy as a plan for the
        plan_date if provided"""
        self.state = 'done'
        self.done_date = done_date
        description = self.description
        self.description = self.current
        if plan_date:
            return Item(description, state='plan', plan_date=plan_date)

    @restricted('done')
    def undone(self):
        self.state = 'todo'

    @restricted('todo')
    def skip(self):
        self.state = 'skip'

    @restricted('skip')
    def unskip(self):
        self.state = 'todo'

    @restricted('todo')
    def plan(self, plan_date: date):
        self.state = 'plan'
        self.plan_date = plan_date

    @restricted('plan')
    def unplan(self):
        self.state = 'todo'

    @restricted('todo')
    def update_time(self):
        """Update elapsed time based on start time"""
        if self.start_time and self.base:
            prev = self.elapsed_time
            new = (date_util.now() - self.start_time).seconds // 60
            elapsed = new + prev
            words = [w for w in self._words if not w.startswith("!")]
            changed = f"{' '.join(words)} !e{elapsed}"
            if self.next:
                changed += f" > {self.next}"
            self.description = changed

    @restricted('todo')
    def start_timer(self):
        if self.base and not self.start_time:
            start = date_util.now().strftime(START_TIME_FORMAT)
            elapsed = self.elapsed_time
            words = [w for w in self._words if not w.startswith("!")]
            changed = f"{' '.join(words)} !s{start}"
            if elapsed:
                changed += f" !e{elapsed}"
            if self.next:
                changed += f" > {self.next}"
            self.description = changed
