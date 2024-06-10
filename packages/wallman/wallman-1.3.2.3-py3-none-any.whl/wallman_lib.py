#!/usr/bin/env python3
from sys import exit
from os import chdir, getenv, system
import logging
import tomllib
from datetime import datetime, time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# setup logging
chdir(str(getenv("HOME")) + "/.local/share/wallman/")
logger = logging.getLogger(__name__)
logging.basicConfig(filename="wallman.log", encoding="utf-8", level=logging.WARNING)

# read config
        # a = list(data["changing_times"].values())
        # print(a[0])

class ConfigError(Exception):
    pass

class _ConfigLib:
    def _initialize_config(self) -> dict:
        chdir(str(getenv("HOME")) + "/.config/wallman/")
        with open("wallman.toml", "rb") as config_file:
            data = tomllib.load(config_file)
            return data
            # a = list(data["changing_times"].values())
            # print(a[0])

    def __init__(self):
        self.config_file: dict = self._initialize_config() # Full config
        # Dictionaries
        self.config_general: dict = self.config_file["general"]
        self.config_changing_times: dict = self.config_file["changing_times"]
        # Values in Dicts
        self.config_wallpaper_sets_enabled: bool = self.config_general["enable_wallpaper_sets"]
        self.config_used_sets: list = self.config_general["used_sets"]
        self.config_wallpapers_per_set: int = self.config_general["wallpapers_per_set"]
        self.config_total_changing_times: int = len(self.config_changing_times)
        try:
            self.config_notify = self.config_general["notify"]
        except KeyError:
            self.config_notify = False
            logger.warning("'notify' is not set in dictionary general in the config file, defaulting to 'false'.")

    def _set_fallback_wallpaper(self):
        if self.config_general["fallback_wallpaper"]:
            system(f"feh --bg-fill --no-fehbg {self.config_general['fallback_wallpaper']}")
            logger.info("The fallback Wallpaper has been set.")
        else:
            logger.critical("An Error occured and no fallback wallpaper was provided, exiting...")
            raise ConfigError("An error occured and no fallback wallpaper has been set, exiting...")

class ConfigValidity(_ConfigLib):
    def __init__(self):
        super().__init__()

    def _check_fallback_wallpaper(self):
        if self.config_general["fallback_wallpaper"]:
            logger.debug("A fallback wallpaper has been defined.")
            return True
        else:
            logger.warning("No fallback wallpaper has been provided. If the config is written incorrectly, the program will not be able to be executed.")
            return False

    def _check_wallpapers_per_set_and_changing_times(self) -> bool:
        # Check if the amount of wallpapers_per_set and given changing times match
        if self.config_total_changing_times == self.config_wallpapers_per_set:
            logger.debug("The amount of changing times and wallpapers per set is set correctly")
            return True
        else:
            try:
                self._set_fallback_wallpaper()
                logger.error("The amount of changing_times and the amount of wallpapers_per_set does not much, the fallback wallpaper has been set.")
                print("ERROR: The amount of changing_times and the amount of wallpapers_per_set does not much, the fallback wallpaper has been set.")
                return False
            except ConfigError:
                logger.critical("The amount of changing times and the amount of wallpapers per set does not match, exiting...")
                raise ConfigError("Please provide an amount of changing_times equal to wallpapers_per_set, exiting...")

    def _check_general_validity(self) -> bool:
        if len(self.config_general) < 3:
            try:
                self._set_fallback_wallpaper()
                logger.error("An insufficient amount of elements has been provided for general, the fallback wallpaper has been set.")
                print("ERROR: An insufficient amount of wallpapers has been provided for general, the fallback wallpaper has been set.")
                return False
            except ConfigError:
                logger.critical("An insufficient amount of elements for general has been provided, exiting...")
                raise ConfigError("general should have at least 3 elements, exiting...")

        else:
            logger.debug("A valid amount of options has been provided in general")
            return True

    def _check_wallpaper_dicts(self) -> bool:
        # This block checks if a dictionary for each wallpaper set exists
        for wallpaper_set in self.config_used_sets:
            if wallpaper_set in self.config_file:
                logger.debug(f"The dictionary {wallpaper_set} has been found in config.")
                return True
            else:
                try:
                    self._set_fallback_wallpaper()
                    logger.error(f"The dictionary {wallpaper_set} has not been found in the config, the fallback wallpaper has been set.")
                    print(f"ERROR: The dictionary {wallpaper_set} has not been found in the config, the fallback wallpaper has been set.")
                    return False
                except ConfigError:
                    logger.critical(f"No dictionary {wallpaper_set} has been found in the config exiting...")
                    raise ConfigError(f"The dictionary {wallpaper_set} has not been found in the config, exiting...")

    def _check_wallpaper_amount(self) -> bool:
        # This block checks if if each wallpaper set dictionary provides enough wallpapers to satisfy wallpapers_per_set
        for wallpaper_set in self.config_used_sets:
            if len(self.config_file[wallpaper_set]) == self.config_wallpapers_per_set:
                logger.debug(f"Dictionary {wallpaper_set} has sufficient values.")
                return True
            else:
                try:
                    self._set_fallback_wallpaper()
                    logger.error(f"The Dictionary {wallpaper_set} does not have sufficient entries, the fallback wallpaper has been set.")
                    print(f"ERROR: The Dictionaty {wallpaper_set} does not have sufficient entries, the fallback wallpaper has been set.")
                    return False
                except ConfigError:
                    logger.critical(f"Dictionary {wallpaper_set} does not have sufficient entries, exciting...")
                    raise ConfigError(f"Dictionary {wallpaper_set} does not have the correct amount of entries, exciting...")

    def validate_config(self) -> bool:
        if not self._check_fallback_wallpaper():
            pass
        if not self._check_wallpapers_per_set_and_changing_times():
            exit(1)
        if not self._check_general_validity():
            exit(1)
        if not self._check_wallpaper_dicts():
            exit(1)
        if not self._check_wallpaper_amount():
            exit(1)
        logger.debug("The config file has been validated successfully (No Errors)")
        return True

class WallpaperLogic(_ConfigLib):
    def __init__(self):
        super().__init__()
        self.chosen_wallpaper_set = False

    # Returns a list of a split string that contains a changing time from the config file
    def _clean_times(self, desired_time) -> list:
        unclean_times = list(self.config_changing_times.values())[desired_time]
        return unclean_times.split(":")

    def _choose_wallpaper_set(self) -> None:
        from random import choice as choose_from
        self.chosen_wallpaper_set = choose_from(self.config_used_sets)
        self.wallpaper_list = list(self.config_file[self.chosen_wallpaper_set].values())
        logger.debug(f"Chose wallpaper set {self.chosen_wallpaper_set}")

    # Verify if a given time is in a given range
    def _time_in_range(self, start, end, x) -> bool:
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x < end

    def _check_system_exitcode(self, code) -> bool:
        if code != 0:
            try:
                self._set_fallback_wallpaper()
                logger.error(f"The wallpaper {self.wallpaper_list[self.current_time_range]} has not been found, the fallback wallpaper has been set. Future wallpapers will still attempted to be set.")
                print(f"ERROR: The wallpaper {self.wallpaper_list[self.current_time_range]} has not been found, the fallback wallpaper has been set. Future wallpapers will still attempted to be set.")
                return False
            except ConfigError:
                logger.error(f"The wallpaper {self.wallpaper_list[self.current_time_range]} has not been found and no fallback wallpaper has been set. Future wallpapers will still attempted to be set.")
                print(f"ERROR: The wallpaper {self.wallpaper_list[self.current_time_range]} has not been found and no fallback wallpaper has been set. Future wallpapers will still attempted to be set.")
                return False
        else:
            logger.debug(f"The wallpaper {self.wallpaper_list[self.current_time_range]} has been set.")
            return True


    def _notify_user(self):
        system("notify-send 'Wallman' 'A new Wallpaper has been set.'")
        logger.debug("Sent desktop notification.")

    def set_wallpaper_by_time(self) -> bool:
        # Ensure use of a consistent wallpaper set
        if self.chosen_wallpaper_set is False:
            self._choose_wallpaper_set()
        for time_range in range(self.config_total_changing_times - 1):
            self.current_time_range = time_range # Store current time for better debugging output
            clean_time = self._clean_times(time_range)
            clean_time_two = self._clean_times(time_range + 1)
            # Check if the current time is between a given and the following changing time and if so, set that wallpaper. If not, keep trying.
            if self._time_in_range(time(int(clean_time[0]), int(clean_time[1]), int(clean_time[2])), time(int(clean_time_two[0]), int(clean_time_two[1]), int(clean_time_two[2])), datetime.now().time()):
                system(f"feh --bg-scale --no-fehbg --quiet {self.wallpaper_list[time_range]}")
                exitcode = system(f"feh --bg-scale --no-fehbg --quiet {self.wallpaper_list[time_range]}")
                has_wallpaper_been_set = self._check_system_exitcode(exitcode)
                if self.config_notify:
                    self._notify_user()
                return has_wallpaper_been_set
            else:
                continue

        system(f"feh --bg-scale --no-fehbg {self.wallpaper_list[-1]}")
        exitcode = system(f"feh --bg-scale --no-fehbg {self.wallpaper_list[-1]}")
        has_wallpaper_been_set = self._check_system_exitcode(exitcode)
        if self.config_notify:
            self._notify_user()
        return has_wallpaper_been_set

    def schedule_wallpapers(self):
        scheduler = BlockingScheduler()
        # Create a scheduled job for every changing time
        for changing_time in range(len(self.config_changing_times)):
            clean_time = self._clean_times(changing_time)
            scheduler.add_job(self.set_wallpaper_by_time, trigger=CronTrigger(hour=clean_time[0], minute=clean_time[1], second=clean_time[2]))
        scheduler.start()
        logger.info("The scheduler has been started.")
