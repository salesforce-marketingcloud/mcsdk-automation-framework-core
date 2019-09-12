import subprocess


class Command:
    """ Command runner class """

    def __init__(self, command):
        if not isinstance(command, list):
            command = command.split(" ")

        """ Class constructor """
        self.__command = command
        self.__output = b''

    def run(self):
        """ Runs the command and returns the status code """
        print("Running command: " + self.get_command())

        result = subprocess.run(self.__command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        self.__output = result.stdout

        return result.returncode

    def returned_errors(self):
        """ Checks if the output contains errors """
        output = self.get_output()
        if output.find("error:") != -1 \
                or output.find("fatal:") != -1 \
                or output.find('FAILURES!') != -1 \
                or output.find('ERRORS!') != -1:
            return True
        return False

    def get_command(self):
        """ Returns the string representation of the command """
        return " ".join(self.__command)

    def get_output(self):
        """
            Returns the output of the command that has been run.

            :returns: str
        """
        return self.__output.decode("utf-8")
