"""Create labels, 12 weekly milestones and their issues in a GitHub repo via the REST API.

Usage: python3 scripts/backlog.py OWNER/REPO [--dry-run]
Re-running skips labels, milestones and issues whose titles already exist.
"""
import json
import subprocess
import sys
from datetime import date, timedelta

START = date(2026, 11, 23)  # Monday of week 1

SCHEDULE = "https://pdos.csail.mit.edu/6.824/schedule.html"
APOSD = "https://web.stanford.edu/~ouster/cgi-bin/aposd.php"
HARD = "https://www.oreilly.com/library/view/software-architecture-the/9781492086888"
STAFF = "https://staffeng.com/book"
PATH = "https://www.oreilly.com/library/view/the-staff-engineers-path/9781098118723/"

LABELS = [
    ("code", "1f6feb", "Go: Gossip Glomers and MIT 6.5840"),
    ("paper", "8250df", "Monday: read a paper"),
    ("book", "bf8700", "Wednesday: read a book chapter"),
    ("real-world", "cf222e", "Friday: post-mortem + blog"),
    ("writing", "1a7f37", "Sunday: weekly note or ADR"),
]

BLOGS = [
    ("Marc Brooker", "https://brooker.co.za/blog/"),
    ("Murat Demirbas", "https://muratbuffalo.blogspot.com/"),
    ("Jack Vanlightly", "https://jack-vanlightly.com/"),
    ("Architecture Weekly", "https://www.architecture-weekly.com/"),
    ("Jepsen analyses", "https://jepsen.io/analyses"),
]

# (code, code links, paper, book, book link, sunday)
WEEKS = [
    ("Set up Maelstrom + Echo + Unique ID", ["https://github.com/jepsen-io/maelstrom", "https://fly.io/dist-sys/1", "https://fly.io/dist-sys/2"],
     "MapReduce (2004)", "A Philosophy of Software Design: first 1/4", APOSD, "Weekly note"),
    ("Broadcast: first parts", ["https://fly.io/dist-sys/3a"],
     "GFS (2003)", "A Philosophy of Software Design: 2/4", APOSD, "ADR #1"),
    ("Broadcast: remaining parts", ["https://fly.io/dist-sys/3a"],
     "Chain Replication (2004)", "A Philosophy of Software Design: 3/4", APOSD, "Weekly note"),
    ("Grow-Only Counter", ["https://fly.io/dist-sys/4"],
     "ZooKeeper (2010)", "A Philosophy of Software Design: last 1/4", APOSD, "ADR #2"),
    ("Kafka-Style Log", ["https://fly.io/dist-sys/5a"],
     "Linearizability (Herlihy), through Section 3.1", "The Hard Parts: chapters 1–2", HARD, "Weekly note"),
    ("Totally-Available Transactions", ["https://fly.io/dist-sys/6a"],
     "Distributed Transactions (6.033, chapter 9, selected sections)", "The Hard Parts: chapter 12, Transactional Sagas", HARD, "ADR #3"),
    ("MIT Lab 1: MapReduce", ["https://pdos.csail.mit.edu/6.824/labs/lab-mr.html"],
     "Spanner (2012)", "The Hard Parts: chapter 4, Architectural Decomposition", HARD, "Weekly note"),
    ("MIT Lab 2: Key/Value server", ["https://pdos.csail.mit.edu/6.824/labs/lab-kvsrv1.html"],
     "Memcached at Facebook (2013)", "The Hard Parts: 1 chapter that fits your work", HARD, "ADR #4"),
    ("MIT Lab 3: Raft, part 1", ["https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html"],
     "Raft (extended): to the end of Section 5", "Staff Engineer (Will Larson): first half", STAFF, "Weekly note"),
    ("MIT Lab 3: Raft, part 2", ["https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html"],
     "Raft: Section 7 to the end (not Section 6)", "Staff Engineer: second half", STAFF, "ADR #5"),
    ("MIT Lab 3: Raft, part 3", ["https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html"],
     "FaRM (2015)", "The Staff Engineer's Path: selected chapters", PATH, "Weekly note"),
    ("MIT Lab 3: Raft, finish, all tests pass", ["https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html"],
     "On-demand Container Loading (2023, AWS Lambda)", "The Staff Engineer's Path: continue", PATH, "ADR #6 + 12-week retro"),
]


def milestone(n):
    """Return (title, description, due_on) for week n."""
    w = WEEKS[n - 1]
    mon = START + timedelta(weeks=n - 1)
    sun = mon + timedelta(days=6)
    title = f"Week {n:02d} ({mon:%b %d} – {sun:%b %d, %Y})"
    desc = f"Code: {w[0]} · Paper: {w[2]} · Book: {w[3]}"
    return title, desc, f"{sun.isoformat()}T19:59:00Z"  # Sunday 23:59 Asia/Baku


def issues(n):
    """Return [(title, labels, body)] for week n, in a fixed order: code, paper, book, real-world, writing."""
    code, links, paper, book, book_link, sunday = WEEKS[n - 1]
    blog_name, blog_url = BLOGS[(n - 1) % len(BLOGS)]
    link_lines = "\n".join(f"- {u}" for u in links)
    adr = sunday.startswith("ADR")
    return [
        (f"W{n} · Code: {code}", ["code"],
         f"**Time:** Tuesday 1 h, Thursday 1 h, Saturday 2 h\n\n**Links:**\n{link_lines}\n\n"
         "- [ ] Tuesday: start, 1 commit\n- [ ] Thursday: continue, 1 commit\n- [ ] Saturday: tests pass\n\n"
         "Rule: if you are stuck for 45 minutes, look at the #dist-sys-challenge tag on the Fly.io Community. "
         "Do not take solution code from an LLM."),
        (f"W{n} · Paper: {paper}", ["paper"],
         f"**Time:** Monday 1 h\n\n**Link:** the paper link is in the MIT 6.5840 schedule: {SCHEDULE}\n\n"
         "- [ ] Read it\n- [ ] Write 5 lines in `notes/papers/`: problem, solution, trade-off"),
        (f"W{n} · Book: {book}", ["book"],
         f"**Time:** Wednesday 1 h\n\n**Link:** {book_link}\n\n"
         "- [ ] Read it\n- [ ] Write in `notes/books/`: 3 ideas + 1 idea to apply at work"),
        (f"W{n} · Real world: 1 post-mortem + {blog_name}", ["real-world"],
         "**Time:** Friday 1 h\n\n**Links:**\n- Post-mortem: https://github.com/danluu/post-mortems\n"
         f"- Blog: {blog_url}\n\n"
         "- [ ] Read 1 post-mortem\n- [ ] Read 1 blog post\n- [ ] Write 1 answer: \"Can this happen to us?\""),
        (f"W{n} · Writing: {sunday}", ["writing"],
         "**Time:** Sunday 1 h\n\n"
         + ("- [ ] Pick 1 real decision from work\n- [ ] Copy `adr/0000-template.md`, write 1 page\n"
            "- [ ] No confidential details (this repo is public)\n" if adr else
            "- [ ] Write a weekly note in `weekly/`: what I learned, where I got stuck, what changes next week\n")
         + "- [ ] Weekly check: all issues in this milestone are closed"),
    ]


def gh(repo, method, path, body=None, dry=False):
    if dry and method != "GET":
        print(f"[dry] {method} {path} {(body.get('title') or body.get('name') or body.get('new_name')) if body else ''}")
        return {"number": 0}
    cmd = ["gh", "api", "-X", method, f"repos/{repo}/{path}"]
    if body is not None:
        cmd += ["--input", "-"]
    out = subprocess.run(cmd, input=json.dumps(body) if body else None, capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"{method} {path} failed: {out.stdout} {out.stderr}")
    return json.loads(out.stdout) if out.stdout.strip() else {}


def get_all(repo, path):
    items, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = gh(repo, "GET", f"{path}{sep}per_page=100&page={page}")
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def main(repo, dry):
    existing_labels = {l["name"] for l in get_all(repo, "labels")}
    for name, color, desc in LABELS:
        if name not in existing_labels:
            gh(repo, "POST", "labels", {"name": name, "color": color, "description": desc}, dry)

    milestones = {m["title"]: m["number"] for m in get_all(repo, "milestones?state=all")}
    titles = {i["title"] for i in get_all(repo, "issues?state=all") if "pull_request" not in i}

    for n in range(1, len(WEEKS) + 1):
        mtitle, mdesc, due = milestone(n)
        if mtitle not in milestones:
            milestones[mtitle] = gh(repo, "POST", "milestones",
                                    {"title": mtitle, "description": mdesc, "due_on": due}, dry)["number"]
        for title, labels, body in issues(n):
            if title not in titles:
                gh(repo, "POST", "issues", {"title": title, "body": body, "labels": labels,
                                            "milestone": milestones[mtitle]}, dry)
    print("done")


if __name__ == "__main__":
    main(sys.argv[1], "--dry-run" in sys.argv)
