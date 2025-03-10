# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import unittest

from streamlit.runtime.stats import (
    CacheStat,
    CacheStatsProvider,
    StatsManager,
    group_stats,
)


class MockStatsProvider(CacheStatsProvider):
    def __init__(self):
        self.stats: list[CacheStat] = []

    def get_stats(self) -> list[CacheStat]:
        return self.stats


class StatsManagerTest(unittest.TestCase):
    def test_get_stats(self):
        """StatsManager.get_stats should return all providers' stats."""
        manager = StatsManager()
        provider1 = MockStatsProvider()
        provider2 = MockStatsProvider()
        manager.register_provider(provider1)
        manager.register_provider(provider2)

        # No stats
        self.assertEqual([], manager.get_stats())

        # Some stats
        provider1.stats = [
            CacheStat("provider1", "foo", 1),
            CacheStat("provider1", "bar", 2),
        ]

        provider2.stats = [
            CacheStat("provider2", "baz", 3),
            CacheStat("provider2", "qux", 4),
        ]

        self.assertEqual(provider1.stats + provider2.stats, manager.get_stats())

    def test_group_stats(self):
        """Should return stats grouped by category_name and cache_name.
        byte_length should be summed."""

        # Similar stats sequential
        stats1 = [
            CacheStat("provider1", "foo", 1),
            CacheStat("provider1", "bar", 2),
            CacheStat("provider1", "bar", 5),
        ]

        # Similar stats not sequential
        stats2 = [
            CacheStat("provider2", "baz", 3),
            CacheStat("provider2", "qux", 4),
            CacheStat("provider2", "baz", 28),
        ]

        # All the same stats
        stats3 = [
            CacheStat("provider3", "boo", 1),
            CacheStat("provider3", "boo", 1),
            CacheStat("provider3", "boo", 1),
            CacheStat("provider3", "boo", 1),
            CacheStat("provider3", "boo", 1),
            CacheStat("provider3", "boo", 1),
            CacheStat("provider3", "boo", 1),
        ]

        self.assertEqual(
            set(group_stats(stats1)),
            {
                CacheStat("provider1", "foo", 1),
                CacheStat("provider1", "bar", 7),
            },
        )

        self.assertEqual(
            set(group_stats(stats2)),
            {
                CacheStat("provider2", "baz", 31),
                CacheStat("provider2", "qux", 4),
            },
        )

        self.assertEqual(
            set(group_stats(stats3)),
            {
                CacheStat("provider3", "boo", 7),
            },
        )
