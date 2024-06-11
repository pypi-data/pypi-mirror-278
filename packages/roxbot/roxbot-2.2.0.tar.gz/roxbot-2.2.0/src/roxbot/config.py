#!/usr/bin/env python3
"""
common configuration

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class MqttConfig(BaseSettings):
    """MQTT related settings"""

    model_config = SettingsConfigDict(env_prefix="mqtt_")

    host: str = "localhost"
    port: int = 1883
    log_topic: str = "/log"
