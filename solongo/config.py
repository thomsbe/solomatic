import ConfigParser


def ReadConfig():
    config = ConfigParser.RawConfigParser()
    config.read('solomatic.cfg')
    return config
