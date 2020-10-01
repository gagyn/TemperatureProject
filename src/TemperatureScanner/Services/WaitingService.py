from time import sleep
from datetime import datetime
from Common.Configuration.ConfigurationService import ConfigurationService

class WaitingService:

    def __init__(self, configurationService: ConfigurationService):
        self.isCancelled = True
        self.configurationService = configurationService
        self.secondsBetween = self.configurationService.get_records_seconds_between()
        self._wait() # run in new thread

    def start(self, action):
        self.isCancelled = False
        self.action = action

    def cancel(self):
        self.isCancelled = True

    def update_seconds_between(self):
        self.secondsBetween = self.configurationService.get_records_seconds_between()

    def _wait(self):
        while True:
            while self.isCancelled:
                sleep(0.5)
            secondsLeft = self._how_many_seconds_should_wait()
            waitedFullTime = self._wait_this_time(secondsLeft)
            if waitedFullTime:
                self.action()

    def _how_many_seconds_should_wait(self) -> int:
        timeInSeconds = (datetime.now() - datetime.now().date()).total_seconds
        howLongShouldWait = self.secondsBetween - timeInSeconds % self.secondsBetween
        return howLongShouldWait

    def _wait_this_time(self, secondsLeft: int) -> bool:
        secondsBetweenSettingWhenStarted = self.secondsBetween
        while secondsLeft > 0:
            sleep(1)
            if self.isCancelled or self.secondsBetween != secondsBetweenSettingWhenStarted:
                return False
            secondsLeft -= 1
        return True
