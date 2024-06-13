from argparse import ArgumentParser


class Flag:

    def __init__(self, *names):
        self.names = names
        self.name = names[0]
        self.aliases = names[1:]
        self.default = None

    def argument_for(self, parser: ArgumentParser):
        parser.add_argument(*self.names, type=str)

    def is_in(self, collection):
        for name in self.names:
            if name in collection:
                return True
        return False

    def get_usage(self):
        return str(list(self.names)[::-1]).replace("\'", "")


class BoolFlag(Flag):

    def __init__(self, *names):
        super().__init__(*names)
        self.default = False

    def argument_for(self, parser: ArgumentParser):
        parser.add_argument(*self.names, action="store_true")
