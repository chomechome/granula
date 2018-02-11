from granula.pattern import IFilenamePattern


class NoMatch(IFilenamePattern):
    def matches(self, filename):
        return False
