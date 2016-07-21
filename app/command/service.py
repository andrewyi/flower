from flask.ext.script import Manager


ServiceCommand = Manager(usage="service command")

@ServiceCommand.command
def c(echo_str):
    print("echo_str: %s." % (echo_str,))
