import ConfigParser


def readconfig():
    config = ConfigParser.RawConfigParser()
    config.read('solomatic.cfg')
    return config
