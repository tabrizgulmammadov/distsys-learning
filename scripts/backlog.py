"""Create (or update) labels, 12 weekly milestones and their issues in a GitHub repo via the REST API.

Usage:
  python3 scripts/backlog.py OWNER/REPO            # create missing items only
  python3 scripts/backlog.py OWNER/REPO --update   # also overwrite existing issue titles and bodies
  python3 scripts/backlog.py OWNER/REPO --dry-run  # print what would change

Issues are matched by milestone + label, so --update keeps issue numbers.
--update overwrites checkboxes: run it only before you start ticking them.
"""
import json
import subprocess
import sys
from datetime import date, timedelta

START = date(2026, 11, 23)  # Monday of week 1

LABELS = [
    ("code", "1f6feb", "Go: Gossip Glomers and MIT 6.5840"),
    ("paper", "8250df", "Monday: read a paper"),
    ("book", "bf8700", "Wednesday: read a book chapter"),
    ("real-world", "cf222e", "Friday: post-mortem + blog"),
    ("writing", "1a7f37", "Sunday: weekly note or ADR"),
]

MAELSTROM = "~/maelstrom/maelstrom test"
MIT_POLICY = "https://pdos.csail.mit.edu/6.824/labs/collab.html"
PAPERS = "https://pdos.csail.mit.edu/6.824/papers"
POSTMORTEMS = "https://github.com/danluu/post-mortems"

# ---------------------------------------------------------------- code (Tue, Thu, Sat)
# Each week: title, setup lines, [(checkbox text, test command or None)]
GLOMERS = {
    1: ("Echo + Unique ID",
        "**Folders:** `glomers/1-echo` (module `maelstrom-echo`), `glomers/2-unique-ids` (module `maelstrom-unique-ids`)\n\n"
        "**Links:** https://github.com/jepsen-io/maelstrom · https://fly.io/dist-sys/1 · https://fly.io/dist-sys/2",
        [("[x] Download Maelstrom 0.2.3", None),
         ("[ ] Toolchain check: `go version` and `java -version` work", None),
         ("[ ] Echo test passes, commit `W1: echo passes (#N)`",
          f"{MAELSTROM} -w echo --bin ~/go/bin/maelstrom-echo --node-count 1 --time-limit 10"),
         ("[ ] Unique ID test passes, commit `W1: unique-ids passes (#N)`",
          f"{MAELSTROM} -w unique-ids --bin ~/go/bin/maelstrom-unique-ids --time-limit 30 --rate 1000 "
          "--node-count 3 --availability total --nemesis partition")]),
    2: ("Broadcast 3a–3c",
        "**Folder:** `glomers/3-broadcast` (module `maelstrom-broadcast`). One folder for 3a–3e: each part extends the same code.\n\n"
        "**Links:** https://fly.io/dist-sys/3a · https://fly.io/dist-sys/3b · https://fly.io/dist-sys/3c",
        [("[ ] 3a Single-Node Broadcast passes, `git tag broadcast-3a`",
          f"{MAELSTROM} -w broadcast --bin ~/go/bin/maelstrom-broadcast --node-count 1 --time-limit 20 --rate 10"),
         ("[ ] 3b Multi-Node Broadcast passes, `git tag broadcast-3b`",
          f"{MAELSTROM} -w broadcast --bin ~/go/bin/maelstrom-broadcast --node-count 5 --time-limit 20 --rate 10"),
         ("[ ] 3c Fault Tolerant Broadcast passes, `git tag broadcast-3c`",
          f"{MAELSTROM} -w broadcast --bin ~/go/bin/maelstrom-broadcast --node-count 5 --time-limit 20 --rate 10 --nemesis partition")]),
    3: ("Broadcast 3d–3e (efficiency)",
        "**Folder:** `glomers/3-broadcast` (same code as week 2)\n\n"
        "**Links:** https://fly.io/dist-sys/3d · https://fly.io/dist-sys/3e\n\n"
        "Read the numbers in the test output: messages-per-operation, median latency, maximum latency.",
        [("[ ] 3d Efficient Broadcast I: msgs-per-op < 30, median < 400 ms, max < 600 ms, `git tag broadcast-3d`",
          f"{MAELSTROM} -w broadcast --bin ~/go/bin/maelstrom-broadcast --node-count 25 --time-limit 20 --rate 100 --latency 100"),
         ("[ ] 3e Efficient Broadcast II: msgs-per-op < 20, median < 1 s, max < 2 s, `git tag broadcast-3e`",
          f"{MAELSTROM} -w broadcast --bin ~/go/bin/maelstrom-broadcast --node-count 25 --time-limit 20 --rate 100 --latency 100"),
         ("[ ] Write the 3d and 3e numbers and your topology choice in `glomers/3-broadcast/README.md`", None)]),
    4: ("Grow-Only Counter",
        "**Folder:** `glomers/4-g-counter` (module `maelstrom-counter`). Uses the Maelstrom `seq-kv` service.\n\n"
        "**Link:** https://fly.io/dist-sys/4",
        [("[ ] G-Counter passes with partitions, commit `W4: g-counter passes (#N)`",
          f"{MAELSTROM} -w g-counter --bin ~/go/bin/maelstrom-counter --node-count 3 --rate 100 --time-limit 20 --nemesis partition"),
         ("[ ] Write in `glomers/4-g-counter/README.md` why your design converges after a partition", None)]),
    5: ("Kafka-Style Log 5a–5c",
        "**Folder:** `glomers/5-kafka-log` (module `maelstrom-kafka`)\n\n"
        "**Links:** https://fly.io/dist-sys/5a · https://fly.io/dist-sys/5b · https://fly.io/dist-sys/5c",
        [("[ ] 5a Single-Node Kafka-Style Log passes, `git tag kafka-5a`",
          f"{MAELSTROM} -w kafka --bin ~/go/bin/maelstrom-kafka --node-count 1 --concurrency 2n --time-limit 20 --rate 1000"),
         ("[ ] 5b Multi-Node Kafka-Style Log passes, `git tag kafka-5b`",
          f"{MAELSTROM} -w kafka --bin ~/go/bin/maelstrom-kafka --node-count 2 --concurrency 2n --time-limit 20 --rate 1000"),
         ("[ ] 5c Efficient Kafka-Style Log passes, `git tag kafka-5c`",
          f"{MAELSTROM} -w kafka --bin ~/go/bin/maelstrom-kafka --node-count 2 --concurrency 2n --time-limit 20 --rate 1000")]),
    6: ("Totally-Available Transactions 6a–6c",
        "**Folder:** `glomers/6-txn` (module `maelstrom-txn`)\n\n"
        "**Links:** https://fly.io/dist-sys/6a · https://fly.io/dist-sys/6b · https://fly.io/dist-sys/6c",
        [("[ ] 6a Single-Node, Totally-Available Transactions passes, `git tag txn-6a`",
          f"{MAELSTROM} -w txn-rw-register --bin ~/go/bin/maelstrom-txn --node-count 1 --time-limit 20 --rate 1000 "
          "--concurrency 2n --consistency-models read-uncommitted --availability total"),
         ("[ ] 6b Read Uncommitted passes: test 1 (no partition)",
          f"{MAELSTROM} -w txn-rw-register --bin ~/go/bin/maelstrom-txn --node-count 2 --concurrency 2n --time-limit 20 "
          "--rate 1000 --consistency-models read-uncommitted"),
         ("[ ] 6b Read Uncommitted passes: test 2 (with partition), `git tag txn-6b`",
          f"{MAELSTROM} -w txn-rw-register --bin ~/go/bin/maelstrom-txn --node-count 2 --concurrency 2n --time-limit 20 "
          "--rate 1000 --consistency-models read-uncommitted --availability total --nemesis partition"),
         ("[ ] 6c Read Committed passes, `git tag txn-6c`",
          f"{MAELSTROM} -w txn-rw-register --bin ~/go/bin/maelstrom-txn --node-count 2 --concurrency 2n --time-limit 20 "
          "--rate 1000 --consistency-models read-committed --availability total --nemesis partition")]),
}

MIT_SETUP = (
    f"> [!CAUTION]\n> Do **not** commit lab code to this public repo. The [6.5840 collaboration policy]({MIT_POLICY}) "
    "asks you not to publish your code. Work in `~/6.5840`. A **private** repo is fine as a backup.\n\n"
)
MIT = {
    7: ("MIT Lab 1: MapReduce", "https://pdos.csail.mit.edu/6.824/labs/lab-mr.html",
        [("[ ] Clone the labs once: `git clone git://g.csail.mit.edu/6.5840-golabs-2026 ~/6.5840`", None),
         ("[ ] All MapReduce tests pass", "cd ~/6.5840/src && make mr")]),
    8: ("MIT Lab 2: Key/Value server", "https://pdos.csail.mit.edu/6.824/labs/lab-kvsrv1.html",
        [("[ ] Part 1: KV server, reliable network", 'cd ~/6.5840/src && make RUN="-run Reliable" kvsrv1'),
         ("[ ] Part 2: lock, reliable network", 'cd ~/6.5840/src && make RUN="-run Reliable" lock1'),
         ("[ ] Part 3: KV server, dropped messages", "cd ~/6.5840/src && make kvsrv1"),
         ("[ ] Part 4: lock, unreliable network", "cd ~/6.5840/src && make lock1")]),
    9: ("MIT Lab 3A: Raft leader election", "https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html",
        [("[ ] 3A tests pass", 'cd ~/6.5840/src && make RUN="-run 3A" raft1')]),
    10: ("MIT Lab 3B: Raft log", "https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html",
         [("[ ] 3B tests pass", 'cd ~/6.5840/src && make RUN="-run 3B" raft1'),
          ("[ ] 3A tests still pass", 'cd ~/6.5840/src && make RUN="-run 3A" raft1')]),
    11: ("MIT Lab 3C: Raft persistence", "https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html",
         [("[ ] 3C tests pass", 'cd ~/6.5840/src && make RUN="-run 3C" raft1'),
          ("[ ] 3A and 3B tests still pass", None)]),
    12: ("MIT Lab 3D: Raft log compaction", "https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html",
         [("[ ] 3D tests pass", 'cd ~/6.5840/src && make RUN="-run 3D" raft1'),
          ("[ ] Full Lab 3 passes", "cd ~/6.5840/src && make raft1")]),
}

# ---------------------------------------------------------------- paper (Mon)
# (title, url, scope, notes file)
PAPER = {
    1: ("MapReduce (2004)", f"{PAPERS}/mapreduce.pdf", "the whole paper", "mapreduce"),
    2: ("GFS (2003)", f"{PAPERS}/gfs.pdf", "the whole paper", "gfs"),
    3: ("Chain Replication (2004)", f"{PAPERS}/cr-osdi04.pdf", "the whole paper", "chain-replication"),
    4: ("ZooKeeper (2010)", f"{PAPERS}/zookeeper.pdf", "the whole paper", "zookeeper"),
    5: ("Linearizability (Herlihy)", f"{PAPERS}/p463-herlihy.pdf", "through Section 3.1", "linearizability"),
    6: ("Distributed Transactions (6.033, chapter 9)",
        "https://ocw.mit.edu/resources/res-6-004-principles-of-computer-system-design-an-introduction-spring-2009/online-textbook/",
        "the sections listed for lecture 11 in the [MIT 6.5840 schedule](https://pdos.csail.mit.edu/6.824/schedule.html)",
        "distributed-transactions"),
    7: ("Spanner (2012)", f"{PAPERS}/spanner.pdf", "the whole paper", "spanner"),
    8: ("Memcached at Facebook (2013)", f"{PAPERS}/memcache-fb.pdf", "the whole paper", "memcache-fb"),
    9: ("Raft (extended), part 1", f"{PAPERS}/raft-extended.pdf", "to the end of Section 5", "raft"),
    10: ("Raft (extended), part 2", f"{PAPERS}/raft-extended.pdf", "Section 7 to the end (skip Section 6)", "raft"),
    11: ("FaRM (2015)", f"{PAPERS}/farm-2015.pdf", "the whole paper", "farm"),
    12: ("On-demand Container Loading in AWS Lambda (2023)", f"{PAPERS}/atc23-brooker.pdf", "the whole paper",
         "aws-lambda-container-loading"),
}

# ---------------------------------------------------------------- book (Wed)
APOSD = ("A Philosophy of Software Design", "https://web.stanford.edu/~ouster/cgi-bin/aposd.php", "aposd")
HARD = ("Software Architecture: The Hard Parts",
        "https://www.oreilly.com/library/view/software-architecture-the/9781492086888", "the-hard-parts")
STAFF = ("Staff Engineer (Will Larson)", "https://staffeng.com/book", "staff-engineer")
PATH = ("The Staff Engineer's Path", "https://www.oreilly.com/library/view/the-staff-engineers-path/9781098118723/",
        "staff-engineers-path")
BOOK = {
    1: (APOSD, "first 1/4"), 2: (APOSD, "second 1/4"), 3: (APOSD, "third 1/4"), 4: (APOSD, "last 1/4"),
    5: (HARD, "chapters 1–2"), 6: (HARD, "chapter 12, Transactional Sagas"),
    7: (HARD, "chapter 4, Architectural Decomposition"), 8: (HARD, "1 chapter that fits your work"),
    9: (STAFF, "first half"), 10: (STAFF, "second half"),
    11: (PATH, "selected chapters, part 1"), 12: (PATH, "selected chapters, part 2"),
}

# ---------------------------------------------------------------- real world (Fri)
BLOGS = [
    ("Marc Brooker", "https://brooker.co.za/blog/"),
    ("Murat Demirbas", "https://muratbuffalo.blogspot.com/"),
    ("Jack Vanlightly", "https://jack-vanlightly.com/"),
    ("Architecture Weekly", "https://www.architecture-weekly.com/"),
    ("Jepsen analyses", "https://jepsen.io/analyses"),
]
PM_SECTIONS = ["Config Errors", "Conflicts", "Time", "Database", "Hardware/Power Failures", "Uncategorized"]

# ---------------------------------------------------------------- writing (Sun)
ADR_WEEKS = {2: 1, 4: 2, 6: 3, 8: 4, 10: 5, 12: 6}


def week_dates(n):
    mon = START + timedelta(weeks=n - 1)
    return mon, mon + timedelta(days=6)


def iso_week(n):
    y, w, _ = week_dates(n)[0].isocalendar()
    return f"{y}-W{w:02d}"


def code_title(n):
    return GLOMERS[n][0] if n in GLOMERS else MIT[n][0]


def milestone(n):
    mon, sun = week_dates(n)
    title = f"Week {n:02d} ({mon:%b %d} – {sun:%b %d, %Y})"
    desc = f"Code: {code_title(n)} · Paper: {PAPER[n][0]} · Book: {BOOK[n][0][0]}, {BOOK[n][1]}"
    return title, desc, f"{sun.isoformat()}T19:59:00Z"  # Sunday 23:59 Asia/Baku


def checklist(items, num):
    lines, cmds = [], []
    for text, cmd in items:
        lines.append("- " + text.replace("#N", f"#{num}"))
        if cmd:
            cmds.append((text.split("] ", 1)[1].split(",")[0].split(":")[0], cmd))
    out = "\n".join(lines)
    if cmds:
        out += "\n\n**Test commands:**\n\n" + "\n\n".join(f"{label}:\n```bash\n{cmd}\n```" for label, cmd in cmds)
    return out


def issues(n, numbers=None):
    """Return {label: (title, body)} for week n. numbers maps label -> issue number (for commit refs)."""
    numbers = numbers or {}
    wk = iso_week(n)
    rules = ("**Rules:** stuck for 45 minutes? Look at the #dist-sys-challenge tag on the Fly.io Community Discourse. "
             "Do not take solution code from an LLM.")

    # code
    code_num = numbers.get("code", "N")
    if n in GLOMERS:
        name, setup, items = GLOMERS[n]
        code_body = (f"**Time:** Tuesday 1 h, Thursday 1 h, Saturday 2 h\n\n{setup}\n\n"
                     f"{checklist(items, code_num)}\n\nAfter each code change: `go install .` in the folder, then run the test.\n\n{rules}")
    else:
        name, url, items = MIT[n]
        code_body = (f"**Time:** Tuesday 1 h, Thursday 1 h, Saturday 2 h\n\n**Link:** {url}\n\n{MIT_SETUP}"
                     f"{checklist(items, code_num)}\n\n"
                     f"- [ ] Write the design and the bugs you found in `weekly/{wk}.md` (text only, no lab code)\n\n"
                     "Tip: run each test several times. Concurrency bugs often appear only in some runs.\n\n"
                     "**Rule:** do not take solution code from an LLM.")

    # paper
    ptitle, purl, scope, slug = PAPER[n]
    paper_body = (f"**Time:** Monday 1 h\n\n**Paper:** {purl}\n\n**Read:** {scope}\n\n"
                  f"- [ ] Read {scope}\n"
                  f"- [ ] Write `notes/papers/{slug}.md` (5 lines): problem, key idea, trade-off, 1 failure case, 1 open question")

    # book
    (btitle, burl, bslug), bscope = BOOK[n]
    book_body = (f"**Time:** Wednesday 1 h\n\n**Book:** [{btitle}]({burl})\n\n**Read:** {bscope}\n\n"
                 f"- [ ] Read {bscope}\n"
                 f"- [ ] Add a `## Week {n}` section to `notes/books/{bslug}.md`: 3 ideas + 1 idea to apply at work")

    # real world
    blog_name, blog_url = BLOGS[(n - 1) % len(BLOGS)]
    section = PM_SECTIONS[(n - 1) % len(PM_SECTIONS)]
    rw_body = (f"**Time:** Friday 1 h\n\n**Links:**\n- Post-mortems: {POSTMORTEMS} (this week: section *{section}*)\n"
               f"- Blog: {blog_url}\n\n"
               f"- [ ] Read 1 post-mortem from the *{section}* section\n"
               f"- [ ] Read 1 post from {blog_name}\n"
               f"- [ ] Add to `weekly/{wk}.md`: what failed, why, and \"Can this happen to us?\" (3–5 lines)")

    # writing
    if n in ADR_WEEKS:
        adr = f"adr/{ADR_WEEKS[n]:04d}-<short-title>.md"
        wtitle = f"ADR #{ADR_WEEKS[n]}" + (" + 12-week retro" if n == 12 else "")
        write_items = (f"- [ ] Pick 1 real decision from work\n"
                       f"- [ ] Copy `adr/0000-template.md` to `{adr}`, fill it in, keep it to 1 page\n"
                       "- [ ] Check: no confidential details (this repo is public)\n"
                       f"- [ ] Finish `weekly/{wk}.md`: 3 lines on what you learned and where you got stuck\n")
    else:
        wtitle = "Weekly note"
        write_items = (f"- [ ] Finish `weekly/{wk}.md`: what I learned, where I got stuck, what I change next week\n")
    if n == 12:
        write_items += "- [ ] Write `weekly/retro-12-weeks.md`: what worked, what did not, what comes next\n"
    write_body = (f"**Time:** Sunday 1 h\n\n{write_items}"
                  "- [ ] Commit and push the week's notes\n"
                  "- [ ] Close the other 4 issues of this milestone, then close this one")

    return {
        "code": (f"W{n} · Code: {name}", code_body),
        "paper": (f"W{n} · Paper: {ptitle}", paper_body),
        "book": (f"W{n} · Book: {btitle}, {bscope}", book_body),
        "real-world": (f"W{n} · Real world: 1 post-mortem + {blog_name}", rw_body),
        "writing": (f"W{n} · Writing: {wtitle}", write_body),
    }


def gh(repo, method, path, body=None, dry=False):
    if dry and method != "GET":
        print(f"[dry] {method} {path} {(body.get('title') or body.get('name')) if body else ''}")
        return {"number": 0}
    cmd = ["gh", "api", "-X", method, f"repos/{repo}/{path}"]
    if body is not None:
        cmd += ["--input", "-"]
    out = subprocess.run(cmd, input=json.dumps(body) if body else None, capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"{method} {path} failed: {out.stdout} {out.stderr}")
    return json.loads(out.stdout) if out.stdout.strip() else {}


FOOTER = "\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_"


def clean(text):
    """Drop the footer that some API proxies append, so re-runs compare real content."""
    text = text or ""
    return text[: -len(FOOTER)] if text.endswith(FOOTER) else text


def get_all(repo, path):
    items, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = gh(repo, "GET", f"{path}{sep}per_page=100&page={page}")
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def main(repo, update, dry):
    have = {l["name"] for l in get_all(repo, "labels")}
    for name, color, desc in LABELS:
        if name not in have:
            gh(repo, "POST", "labels", {"name": name, "color": color, "description": desc}, dry)

    ms = {m["title"]: m for m in get_all(repo, "milestones?state=all")}
    existing = {}  # (milestone number, label) -> issue
    for i in get_all(repo, "issues?state=all"):
        if "pull_request" in i or not i.get("milestone"):
            continue
        for l in i["labels"]:
            existing[(i["milestone"]["number"], l["name"])] = i

    for n in range(1, 13):
        mtitle, mdesc, due = milestone(n)
        if mtitle not in ms:
            ms[mtitle] = gh(repo, "POST", "milestones", {"title": mtitle, "description": mdesc, "due_on": due}, dry)
        elif update and clean(ms[mtitle].get("description")) != mdesc:
            gh(repo, "PATCH", f"milestones/{ms[mtitle]['number']}", {"description": mdesc}, dry)
        mnum = ms[mtitle]["number"]
        numbers = {lab: existing[(mnum, lab)]["number"] for lab, *_ in LABELS if (mnum, lab) in existing}
        for label, (title, body) in issues(n, numbers).items():
            cur = existing.get((mnum, label))
            if cur is None:
                gh(repo, "POST", "issues", {"title": title, "body": body, "labels": [label], "milestone": mnum}, dry)
            elif update and (cur["title"] != title or clean(cur.get("body")) != body):
                gh(repo, "PATCH", f"issues/{cur['number']}", {"title": title, "body": body}, dry)
    print("done")


if __name__ == "__main__":
    main(sys.argv[1], "--update" in sys.argv, "--dry-run" in sys.argv)
