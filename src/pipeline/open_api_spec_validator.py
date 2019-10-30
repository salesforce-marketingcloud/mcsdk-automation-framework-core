from mcsdk.integration.os.process import Command
from mcsdk.bootstrap import cfg


def validate_spec():
    cmd = ' '.join([
        'java',
        '-jar',
        '{swagger_exec}'.format(swagger_exec=cfg['repos']['core']['swagger_cli']),
        'validate',
        '-i',
        '{spec_file}'.format(spec_file=cfg['repos']['core']['swagger_spec'])
    ])

    command = Command(cmd)
    command.run()

    print(command.get_output())

    if not command.returned_errors():
        return 0
    return 255
