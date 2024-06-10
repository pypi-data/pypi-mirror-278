"""This file stores the function that can be used to quickly benchmark the performance of the PrecisionTimer() class
on different host systems.

Successful installation of the library exposes a shorthand 'benchmark_timer' command that can be used to trigger the
benchmark() function stored inside this file with CLI support via click.
"""

import sys
import time as tm

import click  # type: ignore
import numpy as np  # type: ignore
from high_precision_timer.precision_timer import PrecisionTimer  # type: ignore
from tqdm import tqdm


@click.command()
@click.option(
    "--interval-cycles",
    "-ic",
    type=int,
    default=60,
    help="Number of times to repeat interval benchmark for each precision. Default: 10.",
)
@click.option("--interval-delay", "-id", type=float, default=1, help="Interval delay in seconds. " "Default: 1")
@click.option(
    "--delay-cycles",
    "-dc",
    type=str,
    default="1000,1000,1000,60",
    help="Number of times to repeat each delay test for each precision (comma-separated list in the order "
    "of ns, us, ms, s). Default: '1000, 1000, 1000, 60'.",
)
@click.option(
    "--delay-durations",
    "-dd",
    type=str,
    default="250,5,2,1",
    help="Delay durations for each precision (comma-separated list in the order of ns, us, ms, s). Default: "
    "'250, 5, 2, 1'.",
)
def benchmark(interval_cycles: int, interval_delay: float, delay_cycles: str, delay_durations: str) -> None:
    """This function is used to benchmark the PrecisionTimer performance for the caller host system.

    Notes:
        Generally, it is highly advised to use this script to evaluate the particular precision and performance
        capabilities of the timer as they vary for each tested OS and Platform combination (and also depend on the
        overall system utilization in some cases).

        Successful library installation exposes 'benchmark_timer' command that calls this function, which simplifies
        initiating benchmark script runtimes.

        The function comes with click-facilitated CLI support that allows specifying benchmark parameters.
    """
    precisions = ["ns", "us", "ms", "s"]  # Supported precisions to be benchmarked

    # Conversion factors to convert from nanosecond to desired precision.
    divisors = [1, 1_000, 1_000_000, 1_000_000_000]

    # Parses delay cycles and durations from comma-separated strings
    delay_cycles_list: list = [int(x) for x in delay_cycles.split(",")]
    delay_durations_list: list = [int(x) for x in delay_durations.split(",")]

    # Fills missing values with defaults
    delay_cycles_list += [1000] * (4 - len(delay_cycles_list))
    delay_durations_list += [250, 5, 2, 1][len(delay_durations_list) :]

    # Notifies the user that the benchmark has started
    print("Timer Benchmark: Initialized.")

    # Initializes the timer class to benchmark
    timer = PrecisionTimer(precision="ns")

    # Runs and aggregates interval timing results into a storage array. The interval tests consist of executing the
    # requested delay (via python 'sleep' function) and timing the duration of the delay using each of the currently
    # supported precisions. It is advised to use second-precision delay intervals to properly test all supported
    # interval timers, even if this requires a few minutes to run the test cycles. By default, the test takes 4 minutes
    # (1 second x 60 cycles x 4 timers) to run, but this also depends on the interval_delay and interval_cycles.
    interval_results = []
    for precision in precisions:  # Loops over all precisions
        # noinspection PyTypeChecker
        timer.set_precision(precision=precision)
        elapsed_deltas = []
        # Executes the requested number of benchmarking cycles for each precision
        for _ in tqdm(
            range(interval_cycles), desc=f"Running interval timing benchmark for {precision} precision timer"
        ):
            timer.reset()  # Resets the timer
            # Delays for the requested number of seconds. Uses nanosecond-based busywait loop for better precision.
            # It is very likely that the SAME clock is used to delay and time the interval in this case.
            start = tm.perf_counter_ns()
            end = start + round((interval_delay * divisors[3]))
            while tm.perf_counter_ns() < end:
                pass
            elapsed_time = timer.elapsed  # Records the time counted by the timer during the delay
            elapsed_deltas.append(elapsed_time)

        # Calculates the mean and std for the recorded elapsed times and adds them to the results' list alongside some
        # ID information.
        interval_results.append(
            (precision, np.around(np.mean(elapsed_deltas), 3), np.around(np.std(elapsed_deltas), 3))
        )  # Appends cycle results to the storage list

    # Runs and aggregates delay timing results into a storage array. The delay timing tests rely on executing blocking
    # and non-blocking delay methods for each tested precision. Note, this collection explicitly uses busy-wait method
    # and a separate delay test suite is used to benchmark sleep-using delay methods.
    delay_results_busywait = []
    for index, precision in enumerate(precisions):  # Loops over all precisions
        # noinspection PyTypeChecker
        timer.set_precision(precision=precision)
        deltas_block = []
        deltas_noblock = []

        for _ in tqdm(
            range(delay_cycles_list[index]), desc=f"Running busywait delay benchmark for {precision} precision timer"
        ):
            # Tests blocking delay
            start = tm.perf_counter_ns()
            timer.delay_block(delay=delay_durations_list[index], allow_sleep=False)
            end = tm.perf_counter_ns()
            deltas_block.append((end - start) / divisors[index])

            # Tests non-blocking delay
            start = tm.perf_counter_ns()
            timer.delay_noblock(delay=delay_durations_list[index], allow_sleep=False)
            end = tm.perf_counter_ns()
            deltas_noblock.append((end - start) / divisors[index])

        # Calculates the mean and std for both blocking and non-blocking delays and adds them to the results' list
        # alongside some ID information.
        delay_results_busywait.append(
            (
                precision,
                delay_durations_list[index],
                np.around(np.mean(deltas_block), 3),
                np.around(np.std(deltas_block), 3),
                np.around(np.mean(deltas_noblock), 3),
                np.around(np.std(deltas_noblock), 3),
            )
        )

    # This benchmark evaluates ms and s precisions with sleep instead of busywait delay methods. The benchmark is
    # identical to the busywait benchmark otherwise.
    delay_results_sleep = []
    for index, precision in enumerate(["ms", "s"], start=2):  # Loops over all precisions
        # noinspection PyTypeChecker
        timer.set_precision(precision=precision)
        deltas_block = []
        deltas_noblock = []

        for _ in tqdm(
            range(delay_cycles_list[index]), desc=f"Running sleep delay benchmark for {precision} precision timer"
        ):
            # Tests blocking delay
            start = tm.perf_counter_ns()
            timer.delay_block(delay=delay_durations_list[index], allow_sleep=True)
            end = tm.perf_counter_ns()
            deltas_block.append((end - start) / divisors[index])

            # Tests non-blocking delay
            start = tm.perf_counter_ns()
            timer.delay_noblock(delay=delay_durations_list[index], allow_sleep=True)
            end = tm.perf_counter_ns()
            deltas_noblock.append((end - start) / divisors[index])

        # Calculates the mean and std for both blocking and non-blocking delays and adds them to the results' list
        # alongside some ID information.
        delay_results_sleep.append(
            (
                precision,
                delay_durations_list[index],
                np.around(np.mean(deltas_block), 3),
                np.around(np.std(deltas_block), 3),
                np.around(np.mean(deltas_noblock), 3),
                np.around(np.std(deltas_noblock), 3),
            )
        )

    # Displays the test results
    print("\nResults:")
    print("Interval Timing:")
    print("Precision | Interval Time | Mean Recorded Time | Std Recorded Time")
    print("----------+---------------+--------------------+------------------")
    for index, (precision, mean, std) in enumerate(interval_results, start=1):
        print(f"{precision:9} | {interval_delay * divisors[-index]:13} | {mean:18.3f} | {std:16.3f}")

    print("\nBusy-wait Delay Timing:")
    print("Precision | Delay Duration | Mean Block Time | Std Block Time | Mean Noblock Time | Std Noblock Time")
    print("----------+----------------+-----------------+----------------+-------------------+-----------------")
    for precision, delay_duration, block_mean, block_std, noblock_mean, noblock_std in delay_results_busywait:
        print(
            f"{precision:9} | {delay_duration:14} | {block_mean:15.3f} | {block_std:14.3f} | {noblock_mean:17.3f} | "
            f"{noblock_std:16.3f}"
        )

    print("\nSleep Delay Timing:")
    print("Precision | Delay Duration | Mean Block Time | Std Block Time | Mean Noblock Time | Std Noblock Time")
    print("----------+----------------+-----------------+----------------+-------------------+-----------------")
    for precision, delay_duration, block_mean, block_std, noblock_mean, noblock_std in delay_results_sleep:
        print(
            f"{precision:9} | {delay_duration:14} | {block_mean:15.3f} | {block_std:14.3f} | {noblock_mean:17.3f} | "
            f"{noblock_std:16.3f}"
        )

    sys.exit("Benchmark: Complete.")


if __name__ == "__main__":
    benchmark()
