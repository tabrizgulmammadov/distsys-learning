# distsys-learning

A 12-week self-study plan for senior/architect growth: distributed systems in Go, papers, books and architecture decision records (ADRs).

- **Time budget:** 8 hours per week (1 hour per day, 2 hours on Saturday). 96 hours in total.
- **Dates:** Monday, 23 November 2026 – Sunday, 14 February 2027.
- **Split:** 50% building code, 25% reading, 25% real-world cases and writing. Video is optional.

## How this repo works

- **Backlog:** each week is a [milestone](https://github.com/tabrizgulmammadov/distsys-learning/milestones). Each task is an [issue](https://github.com/tabrizgulmammadov/distsys-learning/issues).
- **Labels:** `code`, `paper`, `book`, `real-world`, `writing`.
- **End of the week:** close the issues. The milestone shows the progress.
- **Regenerate the backlog:** `python3 scripts/backlog.py OWNER/REPO`. The script skips items that already exist.

| Folder | Content |
| --- | --- |
| `glomers/<n>-<name>/` | Gossip Glomers solutions, one Go module per challenge (e.g. `glomers/1-echo`) |
| `notes/papers/` | 5 lines per paper: problem, key idea, trade-off, 1 failure case, 1 open question |
| `notes/books/` | One file per book, a `## Week N` section per week: 3 ideas + 1 idea to apply at work |
| `weekly/` | One note per ISO week, for example `2026-W48.md`. Friday's post-mortem answer goes here too |
| `adr/` | ADRs, numbered `0001-<short-title>.md`, from `adr/0000-template.md` |

> [!WARNING]
> This repo is public.
> - Do not commit MIT 6.5840 lab code. The [collaboration policy](https://pdos.csail.mit.edu/6.824/labs/collab.html) asks you not to publish it. Work in `~/6.5840`, back it up only to a private repo.
> - Do not write confidential work details in ADRs.

## Weekly template

Each day has one task and one output. No output means the day is not done.

| Day | Time | Task | Output |
| --- | --- | --- | --- |
| Monday | 1 h | Read the paper of the week | 5-line note: problem, solution, trade-off |
| Tuesday | 1 h | Code: the task of the week | 1 commit |
| Wednesday | 1 h | Book: the chapter of the week | 3 ideas + 1 idea to apply at work |
| Thursday | 1 h | Code: continue | 1 commit, tests |
| Friday | 1 h | 1 post-mortem + 1 blog post | 1 answer: "Can this happen to us?" |
| Saturday | 2 h | Code: deep session | The task tests pass |
| Sunday | 1 h | Writing: weekly note or ADR | 1 page |

If you miss a day, do not add it to Saturday. Continue from the next day.

## 12-week plan

Weeks 1–6: Gossip Glomers. Weeks 7–12: MIT 6.5840 labs. Each paper matches the topic of the code task.

| Week | Code (Tue, Thu, Sat) | Paper (Mon) | Book (Wed) | Sunday |
| --- | --- | --- | --- | --- |
| 1 | Set up [Maelstrom](https://github.com/jepsen-io/maelstrom), then [Echo](https://fly.io/dist-sys/1) and [Unique ID](https://fly.io/dist-sys/2) | MapReduce (2004) | [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/aposd.php): first 1/4 | Weekly note |
| 2 | Broadcast [3a](https://fly.io/dist-sys/3a), [3b](https://fly.io/dist-sys/3b), [3c](https://fly.io/dist-sys/3c) | GFS (2003) | APOSD: 2/4 | ADR #1 |
| 3 | Broadcast [3d](https://fly.io/dist-sys/3d), [3e](https://fly.io/dist-sys/3e) (efficiency) | Chain Replication (2004) | APOSD: 3/4 | Weekly note |
| 4 | [Grow-Only Counter](https://fly.io/dist-sys/4) | ZooKeeper (2010) | APOSD: last 1/4 | ADR #2 |
| 5 | Kafka-Style Log [5a](https://fly.io/dist-sys/5a), [5b](https://fly.io/dist-sys/5b), [5c](https://fly.io/dist-sys/5c) | Linearizability (Herlihy), through Section 3.1 | [Software Architecture: The Hard Parts](https://www.oreilly.com/library/view/software-architecture-the/9781492086888): chapters 1–2 | Weekly note |
| 6 | Totally-Available Transactions [6a](https://fly.io/dist-sys/6a), [6b](https://fly.io/dist-sys/6b), [6c](https://fly.io/dist-sys/6c) | Distributed Transactions (6.033, chapter 9, selected sections) | The Hard Parts: chapter 12, Transactional Sagas | ADR #3 |
| 7 | [MIT Lab 1: MapReduce](https://pdos.csail.mit.edu/6.824/labs/lab-mr.html) | Spanner (2012) | The Hard Parts: chapter 4, Architectural Decomposition | Weekly note |
| 8 | [MIT Lab 2: Key/Value server](https://pdos.csail.mit.edu/6.824/labs/lab-kvsrv1.html) | Memcached at Facebook (2013) | The Hard Parts: 1 chapter that fits your work | ADR #4 |
| 9 | [MIT Lab 3A](https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html): leader election | Raft (extended): to the end of Section 5 | [Staff Engineer](https://staffeng.com/book) (Will Larson): first half | Weekly note |
| 10 | Lab 3B: log | Raft: Section 7 to the end (not Section 6) | Staff Engineer: second half | ADR #5 |
| 11 | Lab 3C: persistence | FaRM (2015) | [The Staff Engineer's Path](https://www.oreilly.com/library/view/the-staff-engineers-path/9781098118723/): selected chapters | Weekly note |
| 12 | Lab 3D: log compaction | On-demand Container Loading (2023, AWS Lambda) | The Staff Engineer's Path: continue | ADR #6 + 12-week retro |

The paper links are in the [MIT 6.5840 schedule](https://pdos.csail.mit.edu/6.824/schedule.html), next to each lecture. The Raft lab can take more than 4 weeks. This is normal: move the plan by one week.

## Sources

Links checked on 18 November 2026. "Not opened separately" means the link came from another official page.

| Source | Used for | Status |
| --- | --- | --- |
| [Gossip Glomers](https://fly.io/dist-sys/) | Code, weeks 1–6 | Opened: 6 challenges |
| [Maelstrom](https://github.com/jepsen-io/maelstrom) | Code, week 1 | From the Fly.io page, not opened separately |
| [MIT 6.5840](https://pdos.csail.mit.edu/6.824/) | Code and papers, weeks 1–12 | Opened: Spring 2026 |
| [MIT 6.5840 schedule](https://pdos.csail.mit.edu/6.824/schedule.html) | Paper links | Opened |
| [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/aposd.php) | Book, weeks 1–4 | Author's page, found by search |
| [Software Architecture: The Hard Parts](https://www.oreilly.com/library/view/software-architecture-the/9781492086888) | Book, weeks 5–8 | O'Reilly page found |
| [Staff Engineer](https://staffeng.com/book) | Book, weeks 9–10 | Opened: most of the book is free on the site |
| [The Staff Engineer's Path](https://www.oreilly.com/library/view/the-staff-engineers-path/9781098118723/) | Book, weeks 11–12 | O'Reilly page found |
| [Dan Luu: post-mortems](https://github.com/danluu/post-mortems) | Friday: post-mortem | Opened |
| [Google SRE book](https://sre.google/sre-book/table-of-contents/) | Friday: 1 chapter instead of a post-mortem | Opened: CC BY-NC-ND license |
| [Marc Brooker](https://brooker.co.za/blog/) | Friday: blog | Opened |
| [Murat Demirbas](https://muratbuffalo.blogspot.com/) | Friday: blog | Opened |
| [Jack Vanlightly](https://jack-vanlightly.com/) | Friday: blog | Opened |
| [Architecture Weekly](https://www.architecture-weekly.com/) (Oskar Dudycz) | Friday: blog | Opened |
| [Jepsen analyses](https://jepsen.io/analyses) | Friday: blog | From the Fly.io page, not opened separately |
| [ADR templates](https://adr.github.io/adr-templates/) | Sunday: ADR | Listed on adr.github.io |
| [Nygard: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html) | Sunday: ADR | From adr.github.io, not opened separately |

After the 12 weeks: [CMU 15-445 Database Systems](https://15445.courses.cs.cmu.edu/) (videos on the CMU-DB YouTube channel), [Learning Domain-Driven Design](https://www.oreilly.com/library/view/-/9781098100124), [Designing Data-Intensive Applications, 2nd edition](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/).

## Rules

- **Video:** 1 hour per week at most, only after the plan of the day is done. Do not replace a planned task with a video.
- **45-minute rule:** if you are stuck for 45 minutes, look at the #dist-sys-challenge tag on the Fly.io Community Discourse. Then continue on your own.
- **LLM rule:** do not take solution code from an LLM. Ask about concepts, write the code yourself. The goal is to build a mental model of how the system fails.
- **ADR:** pick 1 real decision from work. Template: Title, Status, Context, Decision, Consequences. Keep it to 1 page.
- **Delays:** the plan is not tied to dates. If you miss a week, continue from the same row.

Sunday checklist:

- [ ] 3 code sessions done
- [ ] Paper note written
- [ ] Book note written
- [ ] 1 post-mortem and 1 blog post read
- [ ] Sunday writing (note or ADR) done
