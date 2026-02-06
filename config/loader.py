"""
Config Loader - Loads settings from YAML configuration file.
This separates behavior from code, making the agent configurable.
"""

import yaml
from pathlib import Path


def load_settings() -> dict:
    """
    Load settings from config/settings.yaml.
    
    Returns:
        Dictionary containing all configuration settings
    """
    config_path = Path("config/settings.yaml")
    
    if not config_path.exists():
        raise FileNotFoundError(
            "Config file not found. Please create config/settings.yaml"
        )
    
    return yaml.safe_load(config_path.read_text(encoding="utf-8"))


def get_job_settings() -> dict:
    """
    Get job-specific settings.
    
    Returns:
        Dictionary with job preferences
    """
    settings = load_settings()
    return settings.get("job", {})


def get_experience_settings() -> dict:
    """
    Get experience-related settings.
    
    Returns:
        Dictionary with experience filters
    """
    settings = load_settings()
    return settings.get("experience", {})


def get_filter_settings() -> dict:
    """
    Get matching filter settings.
    
    Returns:
        Dictionary with filter thresholds
    """
    settings = load_settings()
    return settings.get("filters", {})


def get_behavior_settings() -> dict:
    """
    Get behavior settings (delays, slow mode, etc.).
    
    Returns:
        Dictionary with behavior configuration
    """
    settings = load_settings()
    return settings.get("behavior", {})
