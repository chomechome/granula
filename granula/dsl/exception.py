import os


class DSLError(Exception):
    """
    DSL error at a given position in the source code
    """
    def __init__(self, message, position):
        """
        :type message: six.text_type
        :param int position: Position in DSL source where an error occurred
        """
        super(DSLError, self).__init__(message)

        self.position = position


class DSLResolveError(Exception):
    """
    Error during DSL resolving in a given file at a given position
    """
    def __init__(self, filename, line, position, source, exception):
        """
        :type filename: six.text_type
        :type line: int
        :type position: int
        :type source: six.text_type
        :type exception: Exception
        """
        # go no further than the rightmost non-whitespace character
        source = source.rstrip()
        position = min(position, len(source))

        super(DSLResolveError, self).__init__(
            u'{exception}'
            u'\n  in "{path}" at line {line}, position {position}.'
            u'\n    {source}'
            u'\n    {offset}^'
            .format(
                path=os.path.abspath(filename),
                line=line,
                position=position,
                source=source,
                exception=exception,
                offset=u' ' * position,
            )
        )
