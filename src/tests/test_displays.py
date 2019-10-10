#!/usr/bin/env python3

from util.displays import Monitor


def test_monitor_attributes():
    monitor = Monitor()
    assert hasattr(monitor.geometry, 'x')
    assert hasattr(monitor.geometry, 'y')
    assert hasattr(monitor.geometry, 'height')
    assert hasattr(monitor.geometry, 'width')


def test_context_manager():
    with Monitor():
        pass


def test_monitor():
    with Monitor() as monitor:
        assert type(monitor.x) is int
        assert type(monitor.y) is int
        assert type(monitor.height) is int
        assert type(monitor.width) is int
        assert monitor.height > 0
        assert monitor.width > 0
