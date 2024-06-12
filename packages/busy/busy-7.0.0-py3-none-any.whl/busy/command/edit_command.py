

from busy.command import CollectionCommand
from busy.util.edit import edit_items


class EditorCommandBase(CollectionCommand):

    timed = True

    @CollectionCommand.wrap
    def execute(self):
        if not self.selection:
            self.status = "Edited nothing"
        else:
            command = self.app.config.get('editor') or 'emacs'
            edited = edit_items(self.collection,
                                self.selection, command)
            self.status = f"Edited {self.count(edited)}"


class EditOneItemCommand(EditorCommandBase):
    """Edit items; default to just one"""

    name = "edit"
    key = "e"


class EditManyCommand(EditorCommandBase):
    """Edit items; default to all"""

    name = 'manage'
    # key = 'm'
    default_filter = ["1-"]
