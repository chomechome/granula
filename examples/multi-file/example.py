import granula


if __name__ == '__main__':
    # gather multi-file configuration from the directory
    config = granula.Config.from_directory('settings')

    print(config)
    print(config.name)
    print(config.occupation)
