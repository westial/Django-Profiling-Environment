#!/usr/bin/env python

__author__ = "Jaume Mila"
__email__ = "jaume@westial.com"
__license__ = "GPL-v.3 <http://www.gnu.org/licenses/gpl-3.0.txt>"
__version__ = "0.5.0"
__file__ = "BasicBenchmarker.py"

import datetime
import time
import psutil
from threading import Thread
import Queue


class BasicBenchmarker(object):
    """
    Class to benchmark pieces of code by timer and CPU and memory usage
    performance. The usage is not delimited to the piece of code but usage of
    whole operating system.

    The start method is required to start the timer and usage recording.

    The usage recording is optional and starts in a different thread at the same
    time that timer.

    Based on a Timer Class created by Frank Sebastia.
    """

    def __init__(self, usage=False, memory_kb=False):
        """
        Constructor
        :param usage: bool
        :param memory_kb: bool returns memory usage in KB instead of
        MB by default.
        """
        self._started_timestamp = None
        self._stopped_timestamp = None

        self._time = 0  # Processing time (cpu time)
        self._elapsed = 0  # Wall clock time (person time)

        self._sTime = 0  # Start time (cpu)
        self._sElapse = 0  # Start time (person)

        self._running = False      # Running control flag

        self._usage = usage    # Flag option for adding usage profiling

        self._cpu_usage = 0      # CPU usage result
        self._memory_usage = 0   # Memory usage result

        if memory_kb:           # Flag for usage memory in KB.
            self._memory_divider = 1024
            self._memory_unit = 'KB'

        else:
            self._memory_divider = 1024 * 1024
            self._memory_unit = 'MB'

        # Queue are thread-safe data structure
        self._max_cpu_usage = Queue.Queue(maxsize=1)        # cpu usage
        self._max_memory_usage = Queue.Queue(maxsize=1)     # memory usage

        self._usage_thread = Thread(target=self._usage_worker)
        self._usage_thread_stop = False         # stop control for usage thread

    def start(self):
        """
        (re)starts the timer
        """
        self._started_timestamp = datetime.datetime.now().isoformat()

        self._sTime = time.clock()
        self._sElapse = time.time()

        if self._usage:
            self._usage_thread.start()

        self._running = True

        return

    def stop(self):
        """
        stops the timer
        """
        if self._running:

            self._stopped_timestamp = datetime.datetime.now().isoformat()

            self._time = time.clock() - self._sTime
            self._elapsed = time.time() - self._sElapse

            if self._usage:
                self._stop_usage_worker()

            self._running = False

        return

    def current(self):
        """
        Return tuple with current elapsed times, cpu & person
        """
        return self.cur_cpu_time(), self.cur_elapsed()

    def cur_cpu_time(self):
        """
        Return current cpu time
        """
        return time.clock() - self._sTime

    def cur_elapsed(self):
        """
        Return current user time
        """
        return time.time() - self._sElapse

    def started_timestamp(self):
        """
        Timestamp on start
        """
        return self._started_timestamp

    def stopped_timestamp(self):
        """
        Timestamp on stop
        """
        return self._stopped_timestamp

    def time(self):
        """
        CPU time
        NOTE execute only when timer is stopped
        :raise Exception if capture is running
        """
        self.stop()
        
        return self._time

    def elapsed(self):
        """
        Stops capture and returns elapsed time - clock time (real time).
        """
        self.stop()
        
        return self._elapsed

    def cpu_usage(self):
        """
        Stops capture and returns cpu usage %
        :return: int
        """
        self.stop()

        if not self._max_cpu_usage.empty():
            self._cpu_usage = self._max_cpu_usage.get()

        return self._cpu_usage

    def memory_usage(self):
        """
        Stops capture and returns memory usage
        :return: int
        """
        self.stop()

        if not self._max_memory_usage.empty():
            self._memory_usage = int(
                self._max_memory_usage.get() / self._memory_divider)

        return self._memory_usage

    def time_to_str(self, prepend=""):
        """
        Returns string representing elapsed times of stopped timer
        :param prepend: string to prepend
        :return: string
        """
        return self._out_str(self.time(), self.elapsed(), prepend)

    def report_to_str(self, prepend=""):
        """
        Stops capture and returns string representing elapsed times of stopped
        timer and usage records if option is enabled.
        :param prepend: string to prepend
        :return: string
        """
        self.stop()

        return self._out_str(self.time(), self.elapsed(), prepend,
                             self._usage, self.cpu_usage(),
                             self.memory_usage(), self._memory_unit)

    def cur_time_str(self, prepend=""):
        """
        Returns string representing elapsed times until now
        :param prepend: string to prepend
        :return: string
        """
        cpu_time, elapsed_time = self.current()
        return self._out_str(cpu_time, elapsed_time, prepend)

    def report(self):
        """
        Stops profiler and returns a dictionary with the key pairs:

            started_time
            stopped_time
            elapsed_seconds
            cpu_seconds
            cpu_usage (if enabled)
            memory_usage (if enabled)

        :return: dict
        """
        self.stop()

        results = {
            'started_time': self.started_timestamp(),
            'stopped_time': self.stopped_timestamp(),
            'elapsed_seconds': round(self.elapsed(), 3),
            'cpu_seconds': round(self.time(), 5),
        }

        if self._usage:
            results['cpu_usage'] = self.cpu_usage()
            results['memory_usage'] = self.memory_usage()

        return results

    def _usage_worker(self):
        """
        Sets used cpu and memory usage in their respective Queue objects.
        """
        cached_max_cpu = 0
        cached_max_memory = 0

        self._max_cpu_usage.put(cached_max_cpu)
        self._max_memory_usage.put(cached_max_memory)

        changes_cpu = 0
        changes_memory = 0

        while not self._usage_thread_stop:
            cpu_percent = psutil.cpu_percent(1)
            memory = psutil.virtual_memory().active

            if cpu_percent > cached_max_cpu:
                cached_max_cpu = cpu_percent
                self._max_cpu_usage.get()
                self._max_cpu_usage.put(cpu_percent)
                changes_cpu += 1

            if memory > cached_max_memory:
                cached_max_memory = memory
                self._max_memory_usage.get()
                self._max_memory_usage.put(memory)
                changes_memory += 1

        print "changes cpu:", changes_cpu, "; changes memory:", changes_memory

        pass

    def _stop_usage_worker(self):
        """
        Public flag control to stop async thread for usage checking.
        Waits until thread is alive and after resets the stop flag.
        """
        self._usage_thread_stop = True

        self._usage_thread.join()

        self._usage_thread_stop = False

        pass

    @classmethod
    def _out_str(cls, cpu, person, prepend,
                 usage=False, cpu_usage=0, memory_usage=0, memory_unit='MB'):
        """
        Helper function to return times
        :param cpu: CPU time
        :param person: clock time
        :param prepend: string to prepend
        :return: string
        """

        txt = ''
        txt += prepend + "Processing time {0:.2f} seconds".format(cpu)
        txt += "\n"
        txt += prepend + "Elapsed time {0:.2f} seconds".format(person)

        if usage:
            txt += "\n"
            txt += prepend + "CPU Usage {!s} %".format(cpu_usage)
            txt += "\n"
            txt += prepend + "Memory Usage {!s} {!s}".format(memory_usage,
                                                             memory_unit)

        return txt

    @classmethod
    def now(cls, fmt="%Y-%m-%d %H:%M:%S"):
        """
        Returns current time
        :param fmt: format of the time
        :return: string representing current time
        """
        return time.strftime(fmt)

    @classmethod
    def _put_if_larger(cls, queue, cached_value, value):

        if queue.empty():
            queue.put(value)

        else:

            if value > cached_value:
                queue.put(value)

        return queue


# Testing

if __name__ == '__main__':

    profiler = BasicBenchmarker(usage=True, memory_kb=True)

    profiler.start()

    time.sleep(10)      # replace by your piece of code

    profiler.stop()

    print profiler.report()

    print profiler.report_to_str()