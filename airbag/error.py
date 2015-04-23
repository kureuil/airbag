from sys import stderr


def write(msg):
    stderr.write('airbag: {0}\n'.format(msg))
