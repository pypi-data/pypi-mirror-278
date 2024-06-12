from busy.command import QueueCommand


class DropCommand(QueueCommand):
    """Move an item to the end of the todo collection of a queue"""

    timed = True
    name = 'drop'
    key = 'r'
    default_filter = [1]

    @QueueCommand.wrap
    def execute(self):
        collection = self.app.storage.get_collection(self.queue)
        lolist, hilist = self.collection.split(self.selection)
        self.collection.data = hilist + lolist
        if len(lolist) == 1:
            self.status = f"Dropped: {str(lolist[0])}"
        elif lolist:
            self.status = f"Dropped {str(len(lolist))} Items"
        else:
            self.status = "Dropped nothing"


class PopCommand(QueueCommand):
    """Move an item to the beginning of the collection"""

    timed = True
    name = 'pop'
    key = 'o'
    default_filter = ['-']

    @QueueCommand.wrap
    def execute(self):
        collection = self.app.storage.get_collection(self.queue)
        hilist, lolist = self.collection.split(self.selection)
        self.collection.data = hilist + lolist
        if len(hilist) == 1:
            self.status = f"Popped: {str(hilist[0])}"
        elif hilist:
            self.status = f"Popped {str(len(hilist))} Items"
        else:
            self.status = "Popped nothing"
