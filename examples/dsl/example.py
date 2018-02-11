import os

import granula


if __name__ == '__main__':
    # use default value here, specified using 'val' operator
    default = granula.Config.from_directory('settings')

    # add SECRET variable to the environment and parse again
    os.environ['SECRET'] = 'secret'
    secret = granula.Config.from_directory('settings')

    print(default)
    print(secret)
