"""Candle Data Servide address"""
from os import environ
CANDLE_DATA_SERVICE = environ.get("CANDLE_DATA_SERVICE_URL", "http://localhost:5000")
EP_CANDLES = '/candles'
EP_SETTINGS = '/settings'
