import logging
import time
from functools import wraps
from typing import Any, Callable, List, Optional

import config

logger = logging.getLogger("health")


class ProviderHealth:
    """Tracker for provider health metrics."""

    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.response_times: List[float] = []

        # Track failures directly
        self.connection_failures = 0
        self.block_failures = 0
        self.network_failures = 0

        # Block timing data
        self.last_block_time: Optional[int] = None

        # Recovery tracking
        self.unhealthy_since: Optional[float] = None
        self.last_recovery_check: float = time.time()

    def record_response_time(self, duration: float) -> None:
        """Record response time."""
        self.response_times.append(duration)

        # Keep only the most recent measurements
        while len(self.response_times) > config.RESPONSE_TIME_WINDOW:
            self.response_times.pop(0)

    def mark_unhealthy(self) -> None:
        """Mark provider as unhealthy and record the time."""
        if self.unhealthy_since is None:
            self.unhealthy_since = time.time()
            logger.info(
                f"{self.provider_name} marked unhealthy, will recover after {config.PROVIDER_RECOVERY_TIME} seconds"
            )

    def _check_recovery(self) -> bool:
        """Check if enough time has passed to recover health."""
        current_time = time.time()
        if current_time - self.last_recovery_check < config.HEALTH_CHECK_MIN_INTERVAL:
            return False

        self.last_recovery_check = current_time
        elapsed = current_time - self.unhealthy_since

        if elapsed >= config.PROVIDER_RECOVERY_TIME:
            logger.info(f"{self.provider_name} recovered after {elapsed:.1f} seconds")
            self.reset_health()
            return True

        return False

    def reset_health(self) -> None:
        """Reset health metrics."""
        self.connection_failures = 0
        self.block_failures = 0
        self.network_failures = 0
        self.unhealthy_since = None
        logger.info(f"Health metrics reset for {self.provider_name}")

    @property
    def avg_response_time(self) -> float:
        """Get average response time."""
        if not self.response_times:
            return 0
        return sum(self.response_times) / len(self.response_times)

    @property
    def is_healthy(self) -> bool:
        """Check if the provider is healthy based on metrics."""
        # Always check recovery first if unhealthy
        if self.unhealthy_since is not None:
            self._check_recovery()

        # Check connection failures
        if self.connection_failures >= config.CONNECTION_FAILURE_THRESHOLD:
            logger.warning(
                f"{self.provider_name} marked unhealthy: connection failures ({self.connection_failures})"
            )
            self.mark_unhealthy()
            return False

        # Check block failures
        if self.block_failures >= config.BLOCK_FAILURE_THRESHOLD:
            logger.warning(
                f"{self.provider_name} marked unhealthy: block failures ({self.block_failures})"
            )
            self.mark_unhealthy()
            return False

        # Check network failures
        if self.network_failures >= config.NETWORK_FAILURE_THRESHOLD:
            logger.warning(
                f"{self.provider_name} marked unhealthy: network failures ({self.network_failures})"
            )
            self.mark_unhealthy()
            return False

        # Response time too slow
        if (
            self.response_times
            and self.avg_response_time > config.PROVIDER_TIMEOUT * 0.8
        ):
            logger.warning(
                f"{self.provider_name} marked unhealthy: slow response time ({self.avg_response_time:.2f}s)"
            )
            self.mark_unhealthy()
            return False

        return True


def measure_time(fn: Callable) -> Callable:
    """Decorator to measure operation time."""

    @wraps(fn)
    def wrapper(client, *args, **kwargs) -> Any:
        start_time = time.time()
        result = fn(client, *args, **kwargs)
        duration = time.time() - start_time

        client.health.record_response_time(duration)
        return result

    return wrapper
