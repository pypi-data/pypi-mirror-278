# Copyright 2022-2023 Georges Racinet <georges.racinet@octobus.net>
# Copyright 2024 Georges Racinet <georges.racinet@cloudcrane.io>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import argparse
from collections import defaultdict
import json
import statistics


def stats():  # pragma no cover
    parser = argparse.ArgumentParser(
        description="Analyse HGitaly logs and output statistics by method",
    )
    parser.add_argument('log_path', help="Path to the log file to analyse")
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--sort-by', choices=('calls',
                                              'incomplete',
                                              'timing:mean',
                                              'timing:median',
                                              'timing:worst_decile',
                                              'timing:worst_centile',
                                              ),
                        default='calls')

    cl_args = parser.parse_args()
    log_path = cl_args.log_path

    called = defaultdict(lambda: 0)
    succeeded = defaultdict(list)

    first_timestamp = None
    with open(log_path) as logf:
        for line in logf:
            try:
                log = json.loads(line)
            except json.JSONDecodeError:
                # ignoring log lines dating from before the transition to JSON
                continue

            if first_timestamp is None:
                first_timestamp = log['asctime']

            req = log.get('request')
            if req is None:
                continue

            req = req.split(' ', 1)[0]
            msg = log.get('message')
            if msg.startswith("Starting"):
                called[req] += 1
            elif msg.startswith("Finished"):
                # milliseconds for readability of most frequent cases
                succeeded[req].append(log["elapsed_seconds"] * 1000)

    total_requests = sum(called.values())
    incomplete = total_requests - sum(len(succ) for succ in succeeded.values())

    stats = []
    for req, count in called.items():
        percent = round(count * 100 / total_requests)
        succ = succeeded[req]
        nb_succ = len(succ)
        req_stats = dict(percent=percent,
                         calls=count,
                         complete=nb_succ,
                         incomplete=count - nb_succ,
                         )
        stats.append((req, req_stats))
        if nb_succ > 0:
            timing = req_stats['completion_stats_ms'] = dict(
                mean=statistics.mean(succ),
                median=statistics.median(succ),
            )
            if nb_succ > 1:
                timing['standard_deviation'] = statistics.pstdev(succ)
                deciles = statistics.quantiles(succ, method='inclusive', n=10)
                centiles = statistics.quantiles(succ, method='inclusive',
                                                n=100)
                timing['best_centile'] = centiles[0]
                timing['best_decile'] = deciles[0]
                timing['worst_decile'] = deciles[-1]
                timing['worst_centile'] = centiles[-1]

    sort_key = cl_args.sort_by
    if sort_key.startswith('timing:'):
        sort_key = ('completion_stats_ms', sort_key.split(':', 1)[-1])

    def sort_key_function(req_stats):
        stats = req_stats[1]
        if isinstance(sort_key, str):
            return -stats.get(sort_key, 0)

        stats = stats.get(sort_key[0])
        if stats is None:
            return 0
        return -stats.get(sort_key[1], 0)

    stats.sort(key=sort_key_function)
    stats = dict(stats)

    if cl_args.json:
        print(json.dumps(stats))
        return

    print(f"TOTAL Requests since {first_timestamp}: {total_requests} \n"
          f"      {incomplete} incomplete (cancelled or failed)")
    print("Breakdown:")
    for req, details in stats.items():
        percent = '%4.1f' % details['percent']
        time_stats = details['completion_stats_ms']
        mean = time_stats['mean']
        avg_ms_str = '%.1f' % mean
        worst_decile_str = '%.1f' % time_stats.get('worst_decile', mean)
        print(f"  {percent}% {req} "
              f"(called={details['calls']}, "
              f"incomplete={details['incomplete']}, "
              f"average_time={avg_ms_str}ms, "
              f"worst_decile={worst_decile_str}ms)")
