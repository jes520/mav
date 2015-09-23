# .. -*- coding: utf-8 -*-
#
# ***********************************************************
# mav_recharging.py - Simulate a multi-MAV recharging station
# ***********************************************************
# A group of *n* MAVs each carry out a mission by taking off, flying along a directed path, then landing when the mission is complete. They land at a charging station, which is a circle with a series of electrodes evenly distributed around it. The MAVs then connect to two electrodes, charge, then take off to complete their next mission.
#
# Your task is to simulate the charging station's operation. When an MAV lands, it will reqest two electrodes from the charging station; when both are given, it charges, releases the electrodes, then takes off again. You must insure that a given electrode is only granted to one MAV at a time.
#
# Each MAV should be simulated by a class which runs in a unique thread, making charging requests of the station..
#
# Library imports
# ===============
# For the core code.
from threading import Thread, Lock
# For testing.
from time import sleep
from Queue import Queue
from threading import ThreadError
import pytest
#
# A simple enumerate I like, taken from one of the snippet on `stackoverflow
# <http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python>`_.
# What I want: a set of unique identifiers that will be named nicely,
# rather than printed as a number. Really, just a way to create a class whose
# members contain a string representation of their name. Perhaps the best
# solution is `enum34 <https://pypi.python.org/pypi/enum34>`_, based on `PEP
# 0435 <https://www.python.org/dev/peps/pep-0435/>`_, but I don't want an extra
# dependency just for this.
class Enum(frozenset):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

_MAV_STATES = Enum( ('Flying', 'Waiting', 'Charging') )

# MAV class
# =========
class MAV(Thread):
    def __init__(self,
      # The left electrode for this MAV.
      left_electrode,
      # The right electrode for this MAV.
      right_electrode,
      # Time spent flying on a mission, in seconds.
      fly_time_sec=0.5,
      # Time spent charging, in seconds.
      charge_time_sec=1.5,
      # Any extra args.
      **kwargs):

        # Before flying:
        self._state = None

        # Your code here.

    def run(self):
        # Your code here.
        #
        # Fly while ``self.running`` is True. Update your state:
        self._state = _MAV_STATES.Flying
        self._state = _MAV_STATES.Waiting
        self._state = _MAV_STATES.Charging
        # When done flying:
        self._state = None
#
# Testing
# =======
# A testable electrode: waits until True is placed in its queue before allowing code to proceed.
class MockElectrode(object):
    def __init__(self):
        self.q = Queue()
        self.is_locked = False

    # Context manager
    # ---------------
    # Defining these methods allows use of the ``MockElectrode`` class in a `context manager <https://docs.python.org/2/reference/datamodel.html#context-managers>`_ (the `with <https://docs.python.org/2/reference/compound_stmts.html#with>`_ statement).
    #
    # To acquire a (mock) electrode, wait until the test grants permission to use this electrode by plaing a True value in its queue. See `__enter__ <https://docs.python.org/2/reference/datamodel.html#object.__enter__>`_.
    def __enter__(self):
        # For testing purposes, show that this electrode is currently locked.
        self.is_locked = True
        assert self.q.get()

    # When exiting the context manager, simply note that this electode isn't locked. See `__exit__ <https://docs.python.org/2/reference/datamodel.html#object.__exit__>`_.
    def __exit__(self, exc_type, exc_value, traceback):
        self.is_locked = False
        return False

class TestMav(object):
    def test_1(self):
        e_left = MockElectrode()
        e_right = MockElectrode()
        fly_time_sec = 0.05
        charge_time_sec = 0.15
        thread_start_time_sec = 0.01
        m = MAV(e_left, e_right, fly_time_sec, charge_time_sec)
        assert m._state == None

        # Wait to make sure the MAV isn't flying until we start it.
        sleep(thread_start_time_sec)
        assert m._state == None
        m.start()

        # Use a ``finally`` clause to guarentee that the ``m`` thread will be shut down properly.
        try:
            # Wait for the thread to start, then check that it's flying.
            sleep(thread_start_time_sec)
            assert m._state == _MAV_STATES.Flying

            # Wait for the fly time to end, then check that it's waiting.
            sleep(fly_time_sec)
            assert m._state == _MAV_STATES.Waiting

            # Wait a while to make sure it's waiting for an electrode.
            sleep(charge_time_sec*2)
            assert m._state == _MAV_STATES.Waiting
            e_left.q.put(True)

            # Wait some more to make sure it's waiting for the other electrode.
            sleep(charge_time_sec*2)
            assert m._state == _MAV_STATES.Waiting
            e_right.q.put(True)

            # Wait a bit to let it start charging.
            sleep(thread_start_time_sec)
            m.running = False
            assert m._state == _MAV_STATES.Charging

            # Wait for the charge cycle to finish. The MAV should be done.
            sleep(charge_time_sec)
            assert m._state == None

        finally:
            # Tell the MAV to stop operations.
            m.running = False
            # Wait for the thread to terminate.
            m.join(thread_start_time_sec)
            # Verify that it exited correctly -- the thread should be dead.
            assert not m.isAlive()

class TestElectrode(object):
    # Releasing an electrode not in use should raise an exception.
    def test_1(self):
        e = Electrode()
        # Releasing an electrode that's unlocked should raise a ThreadError, just as `releasing a Lock <https://docs.python.org/2/library/threading.html#threading.Lock.release>`_ does. See `pytest.raises <https://pytest.org/latest/assert.html#assertions-about-expected-exceptions>`_.
        with pytest.raises(ThreadError):
            e.release()

    # An electrode should be able to be acquired only once.
    def test_2(self):
        e = Electrode()
        assert e.acquire()
        assert not e.acquire(False)

        # After releasing the lock, it should be able to be acquired again.
        e.release()
        assert e.acquire()

    # An electrode should work with context managers.
    def test_3(self):
        e = Electrode()
        with e:
            assert not e.acquire(False)
        assert e.acquire()
#
# main code
# =========
def main():
    pass

if __name__ == '__main__':
    main()
