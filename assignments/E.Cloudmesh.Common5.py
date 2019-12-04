from cloudmesh.common.StopWatch import StopWatch
import os

StopWatch.start("Start the stop watch")
os.sleep(100)
StopWatch.stop("Stop the stop watch")
Stopwatch.benchmark.print()

print(StopWatch.get("test"))