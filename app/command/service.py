from flask_script import Manager


ServiceCommand = Manager(usage="service command")


@ServiceCommand.command
def c(echo_str):
    print("echo_str: %s." % (echo_str,))


# @ServiceCommand.command
@ServiceCommand.option('-n', '--name', help='name str', dest='name')
@ServiceCommand.option('-i', '--mobile', help='mobile str', dest='mobile', default='132')
def opt(name, mobile):
    print("name: %s, mobile: %s." % (name, mobile))
