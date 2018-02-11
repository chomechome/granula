import granula


if __name__ == '__main__':
    # match files without environment and 'testing' configurations
    testing = granula.Config.from_directory(
        directory='settings',
        pattern=granula.Environment('testing'),
    )

    # match files without environment and 'production' configurations
    production = granula.Config.from_directory(
        directory='settings',
        pattern=granula.Environment('production'),
    )

    print(testing)
    print(production)
