from time import sleep
from Common.Configuration.ConfigurationService import ConfigurationService

class WaitingService:

    def __init__(self, action, configurationService: ConfigurationService):
        self.isCancelled = True
        self.action = action
        self.configurationService = configurationService

    def restart(self):
        self.isCancelled = False

    def cancel(self):
        self.isCancelled = True

    def _wait(self):
        while True:
            while self.isCancelled:
                sleep(0.5)
            action()

    def _get_next_execute_time(self):
        pass