from mcsdk.integration.os.process import Command
import os

TRAVIS_BUILD_DIR = os.environ.get('TRAVIS_BUILD_DIR')


def validate_spec():
    open_api_spec_path = os.path.join(TRAVIS_BUILD_DIR, 'resources', 'sfmc-openapi-v2.json')
    swagger_codegen_cli_path = os.path.join(TRAVIS_BUILD_DIR, 'bin', 'swagger-codegen-cli.jar')

    cmd = ' '.join([
        'java',
        '-jar',
        '{swagger_exec}'.format(swagger_exec=swagger_codegen_cli_path),
        'validate',
        '-i',
        '{spec_file}'.format(spec_file=open_api_spec_path)
    ])

    command = Command(cmd)
    command.run()

    print(command.get_output())

    if not command.returned_errors():
        return 0
    return 255
