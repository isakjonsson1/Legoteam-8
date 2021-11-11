"""Logging functionalities"""
import time
import sys


class Logger:
    """
    A class for logging functions
    
    params:
        stdout : bool - If stdout should be an output
        outputs : dict - Keys are writeable io buffer objects, values are logging level (0 - 50) 
        format : str - Logging format

    Note:
        The valid string format parameters are the same as in the logging standard python module found
        here: https://docs.python.org/3/library/logging.html#logrecord-attributes
        However, not all paramters are defined. As per 11 nov 2021 20:00 the implemented parameters are:
        %(name)s, %(asctime)s, %(time)d, %(levelname)s, %(levelno)d, %(message)s
    """
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    def __init__(self, 
                 name=__name__,
                 outputs={ sys.stdout: 10, open("latest.log", "a", encoding="UTF-8"): 20 },
                 log_format="%(asctime)s |:| %(name)s:%(levelname)-8s |:| %(message)s",
                 silent_log_errors=True):
        self.name = name
        self.outputs = outputs
        self.log_format = log_format
        self.silent_log_errors = silent_log_errors

    def debug(self, message):
        """Sends a debug logging message with logging level 10"""
        return self.log(message, self.DEBUG)

    def info(self, message):
        """Sends an info logging message with logging level 20"""
        return self.log(message, self.INFO)

    def warning(self, message):
        """Sends a warning logging message with logging level 30"""
        return self.log(message, self.WARNING)

    def error(self, message):
        """Sends a error logging message with logging level 40"""
        return self.log(message, self.ERROR)
        
    def critical(self, message):
        """Sends a critical logging message with logging level 50"""
        return self.log(message, self.CRITICAL)

    def log(self, message, level):
        """Sends a logging message with the given logging message"""
        return self.write_to_outputs({
            "message": message,
        }, level)
    
    def write_to_outputs(self, data, loglevel):
        """Writes to all the outputs with a loglevel lower than or equal to the given loglevel"""
        data["name"] = self.name
        data["time"] = time.time()
        time_struct = time.localtime()
        data["asctime"] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d},{:03d}".format(
            time_struct.tm_year,
            time_struct.tm_mon,
            time_struct.tm_mday,
            time_struct.tm_hour,
            time_struct.tm_min,
            time_struct.tm_sec,
            round(time.time() % 1 * 1000)
        )

        # Track errors, then display them later
        errors = []
        for output in self.outputs:
            data["levelno"] = self.outputs[output]
            data["levelname"] = self.level_num_to_name(loglevel)
            if self.outputs[output] <= loglevel:
                try:
                    output.write(self.log_format % data)
                    output.write("\n")
                    output.flush()
                except Exception as error:
                    if not self.silent_log_errors:
                        raise error
                    errors[(output, error)]

        for output, error in errors:
            print("Failed to log to {} ({}).\n\n".format(output, output.name) +
                  "{}\n{}".format(error.traceback, error))

    def time(self, loglevel=DEBUG, time_log_format="%(name)s() took %(time_ms).3fms to run"):
        """
        Returns a function that executes the given function, but logs the time taken as well.
        
        Intended to be used as a decorator. To run and time the function, see Logger.run_and_time
        instead.
        """
        def decorator(function):
            def decorated_function(*args, **kwargs):
                start = time.perf_counter()
                result = function(*args, **kwargs)
                end = time.perf_counter()
                self.log(time_log_format % {
                    "name": function.__name__,
                    "time": end-start,
                    "time_ms": (end-start)*1000,
                    "start_time": start,
                    "end_time": end
                }, loglevel)
                return result
            return decorated_function
        return decorator

    def run_and_time(self, function, *args, **kwargs):
        """Run and time the given function"""
        return self.time()(function)(*args, **kwargs)

    def level_num_to_name(self, num):
        """Returns the name of the given level"""
        if num >= 50:
            return "CRITICAL"
        if num >= 40:
            return "ERROR"
        if num >= 30:
            return "WARNING"
        if num >= 20:
            return "INFO"
        if num >= 10:
            return "DEBUG"
        return "NOTSET"

    def __del__(self):
        """Close all output streams when the object is destructured"""
        for output in self.outputs.keys():
            if output == sys.stdout: continue
            output.close()