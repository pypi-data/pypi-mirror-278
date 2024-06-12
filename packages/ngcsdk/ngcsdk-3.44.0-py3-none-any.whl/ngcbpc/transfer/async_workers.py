#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import asyncio
import time
from typing import Any, Callable, Optional

from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor

from ngcbpc.environ import NGC_CLI_PROGRESS_UPDATE_FREQUENCY

# contractral constant, cannot be modified without agreement
PARTITION_SIZE = 500000000

# This line instruments aiohttp client sessions and requests, enabling tracing functionality.
# It adds default trace configuration options to all aiohttp requests
AioHttpClientInstrumentor().instrument()

# This line instruments all asyncio functions, enabling tracing without the need to pass a tracer explicitly.
# In asyncio workers, where different contexts may exist for the overall execution and individual worker tasks,
# this instrumentation ensures that tracing captures and respects the distinct contexts of each worker's execution.
AsyncioInstrumentor().instrument()


class AsyncTransferProgress:
    """
    Track overall transfer progress for a transfer,
    and calls provided callback with a specified maximum update rate,
    including completed, failed, and total bytes and counts.

    Args:
        completed_bytes (int): The number of completed bytes.
        failed_bytes (int): The number of failed bytes.
        total_bytes (int): The total number of bytes.
        completed_count (int): The number of completed items.
        failed_count (int): The number of failed items.
        total_count (int): The total number of items.
        callback_func (Optional[Callable[[int, int, int, int, int, int], Any]]):
            A callback function that accepts six integers representing
            completed_bytes, failed_bytes, total_bytes, completed_count,
            failed_count, and total_count respectively. If provided,
            this function will be called to report progress.
            If set to None, progress updates will not be reported.
        update_rate (float): The maximum update rate for the callback function,
            in seconds. Progress updates will be reported at most once per
            this duration. Ignored if callback_func is None.

    """

    def __init__(
        self,
        completed_bytes: int = 0,
        failed_bytes: int = 0,
        total_bytes: int = 0,
        completed_count: int = 0,
        failed_count: int = 0,
        total_count: int = 0,
        callback_func: Optional[  # pylint: disable=unsubscriptable-object
            Callable[[int, int, int, int, int, int], Any]
        ] = None,
        update_rate=NGC_CLI_PROGRESS_UPDATE_FREQUENCY,
    ):
        self.lock = asyncio.Lock()
        self.completed_bytes = completed_bytes
        self.failed_bytes = failed_bytes
        self.total_bytes = total_bytes
        self.completed_count = completed_count
        self.failed_count = failed_count
        self.total_count = total_count
        self.callback_func = callback_func

        self.update_rate = update_rate if callback_func else -1
        self.next_update = time.time() + update_rate if callback_func else -1

    async def debounced_update_progress(self):
        """
        Call the update progress callback function if the specified update rate interval has passed.

        'callback_func' is a user provided function with limited capability during lots of concurrent updates.

        Be sure to call update_progress at the end to finalize progress update
        """

        now = time.time()  # tiny bit less expensive than lock check, thus do it first
        if self.callback_func and now > self.next_update and (not self.lock.locked()):
            async with self.lock:
                self.next_update = now + self.update_rate
                self.update_progress()

    def update_progress(self):
        """
        Call the update progress callback function with the current progress metrics.
        """

        if self.callback_func:
            self.callback_func(
                self.completed_bytes,
                self.failed_bytes,
                self.total_bytes,
                self.completed_count,
                self.failed_count,
                self.total_count,
            )

    async def advance(self, size_in_bytes: int, count: int):
        """
        Advance the progress by adding completed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.completed_bytes += size_in_bytes
            self.completed_count += count
        await self.debounced_update_progress()

    async def fail(self, size_in_bytes: int, count: int):
        """
        Update the progress by adding failed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.failed_bytes += size_in_bytes
            self.failed_count += count
        await self.debounced_update_progress()

    def read_progress(self):
        """
        Read the current progress metrics.
        """
        return (
            self.completed_bytes,
            self.failed_bytes,
            self.total_bytes,
            self.completed_count,
            self.failed_count,
            self.total_count,
        )
