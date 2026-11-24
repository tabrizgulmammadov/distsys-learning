# MapReduce (Dean, Ghemawat, OSDI 2004)

Paper: <https://pdos.csail.mit.edu/6.824/papers/mapreduce.pdf>. Read on 24 November 2026 (week 1).

1. **Problem:** The computations at Google were simple, but the input was too large for one machine. Each team wrote complex code for parallelization, data distribution and failure handling, and this code hid the simple logic (§1).
2. **Key idea:** The user writes only `map(k1,v1) → list(k2,v2)` and `reduce(k2,list(v2)) → list(v2)`. The library splits the input, groups values by key, schedules tasks, balances load and re-executes failed tasks. Re-execution is safe because the functions are deterministic (§2.2, §3.1, §3.3).
3. **Trade-off:** One master keeps all task state in one place, so scheduling is simple. But the master is a single point of failure: if it fails, the job aborts and the client must retry (§3.3).
4. **Failure case:** The master pings each worker. If worker A does not answer, A's completed map tasks run again, because their output was on A's local disk. Completed reduce tasks do not run again, because their output is in GFS (§3.3). With 200 of 1746 workers killed, the sort job took only 5% longer (§5.5).
5. **Open question:** For a job that runs for hours, a restart after a master failure costs a lot of time. When do checkpoints of the master state become worth their cost? The paper says checkpoints are easy, but it does not use them (§3.3).
