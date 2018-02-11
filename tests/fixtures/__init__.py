import os


def get_fixture_path(filename):
    """
    :type filename: six.text_type
    :rtype: six.text_type
    """
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, filename)
