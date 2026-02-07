"""
Rate Limiter Module - DAY 19

Implements human-like delays between actions to avoid detection.
Critical for scaling without triggering anti-bot measures.
"""

import time
import random
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def human_pause(min_s: float = 20, max_s: float = 45):
    """
    Wait a random amount of time to simulate human behavior.
    
    Args:
        min_s: Minimum seconds to wait
        max_s: Maximum seconds to wait
    """
    delay = random.uniform(min_s, max_s)
    print(f"⏳ Waiting {int(delay)} seconds (human-like delay)...")
    
    # Show countdown for longer waits
    if delay > 10:
        remaining = int(delay)
        while remaining > 0:
            print(f"   {remaining}s remaining...", end="\r")
            time.sleep(min(remaining, 5))
            remaining -= 5
        print(" " * 30, end="\r")  # Clear line
    else:
        time.sleep(delay)


def quick_pause(min_s: float = 2, max_s: float = 5):
    """
    Short pause between actions within an application.
    """
    delay = random.uniform(min_s, max_s)
    time.sleep(delay)


def typing_delay(text_length: int) -> float:
    """
    Calculate realistic typing delay based on text length.
    
    Args:
        text_length: Number of characters
    
    Returns:
        float: Seconds to wait
    """
    # Average typing speed: 40 words per minute = ~3.3 chars per second
    # Add some randomness
    base_time = text_length / 3.3
    variation = random.uniform(0.8, 1.2)
    return base_time * variation


def should_take_break(jobs_applied: int, break_every: int = 5) -> bool:
    """
    Check if we should take a longer break.
    
    Args:
        jobs_applied: Number of jobs applied so far
        break_every: Take break every N jobs
    
    Returns:
        bool: True if break is needed
    """
    return jobs_applied > 0 and jobs_applied % break_every == 0


def long_break(min_minutes: float = 5, max_minutes: float = 15):
    """
    Take a longer break to avoid detection.
    
    Args:
        min_minutes: Minimum minutes to wait
        max_minutes: Maximum minutes to wait
    """
    delay_minutes = random.uniform(min_minutes, max_minutes)
    delay_seconds = delay_minutes * 60
    
    print(f"\n☕ Taking a {int(delay_minutes)} minute break...")
    print("   This helps avoid detection and rate limits.")
    
    # Show countdown
    remaining = int(delay_seconds)
    while remaining > 0:
        mins, secs = divmod(remaining, 60)
        print(f"   {mins}m {secs}s remaining...", end="\r")
        time.sleep(10)
        remaining -= 10
    
    print(" " * 40, end="\r")
    print("   Break complete! Resuming...")


class SessionLimiter:
    """
    Tracks session limits and enforces safe application rates.
    """
    
    def __init__(self, max_per_session: int = 3, max_per_day: int = 10):
        self.max_per_session = max_per_session
        self.max_per_day = max_per_day
        self.session_count = 0
        self.daily_count = 0
    
    def can_apply(self) -> tuple:
        """
        Check if we can apply to another job.
        
        Returns:
            tuple: (can_apply: bool, reason: str)
        """
        if self.session_count >= self.max_per_session:
            return False, f"Session limit reached ({self.max_per_session})"
        
        if self.daily_count >= self.max_per_day:
            return False, f"Daily limit reached ({self.max_per_day})"
        
        return True, "OK"
    
    def record_application(self):
        """Record a successful application."""
        self.session_count += 1
        self.daily_count += 1
    
    def get_stats(self) -> dict:
        """Get current session statistics."""
        return {
            "session_applied": self.session_count,
            "session_limit": self.max_per_session,
            "daily_applied": self.daily_count,
            "daily_limit": self.max_per_day
        }
