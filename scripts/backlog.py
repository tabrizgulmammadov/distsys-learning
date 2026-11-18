"""Create labels, 12 weekly milestones and their issues in a GitHub repo via the REST API.

Usage: python3 backlog.py OWNER/REPO [--dry-run]
Re-running skips labels, milestones and issues whose titles already exist.
"""
import json
import subprocess
import sys
from datetime import date, timedelta

REPO = sys.argv[1]
DRY = "--dry-run" in sys.argv
START = date(2026, 11, 23)  # Monday of week 1

SCHEDULE = "https://pdos.csail.mit.edu/6.824/schedule.html"
APOSD = "https://web.stanford.edu/~ouster/cgi-bin/aposd.php"
HARD = "https://www.oreilly.com/library/view/software-architecture-the/9781492086888"
STAFF = "https://staffeng.com/book"
PATH = "https://www.oreilly.com/library/view/the-staff-engineers-path/9781098118723/"

LABELS = [
    ("kod", "1f6feb", "Go: Gossip Glomers və MIT 6.5840"),
    ("paper", "8250df", "Bazar ertəsi: paper oxu"),
    ("kitab", "bf8700", "Çərşənbə: kitab fəsli"),
    ("real-dunya", "cf222e", "Cümə: post-mortem + bloq"),
    ("yazi", "1a7f37", "Bazar: həftəlik qeyd və ya ADR"),
]

BLOGS = [
    ("Marc Brooker", "https://brooker.co.za/blog/"),
    ("Murat Demirbas", "https://muratbuffalo.blogspot.com/"),
    ("Jack Vanlightly", "https://jack-vanlightly.com/"),
    ("Architecture Weekly", "https://www.architecture-weekly.com/"),
    ("Jepsen analizləri", "https://jepsen.io/analyses"),
]

# (code, code links, paper, book, book link, sunday)
WEEKS = [
    ("Maelstrom qur + Echo + Unique ID", ["https://github.com/jepsen-io/maelstrom", "https://fly.io/dist-sys/1", "https://fly.io/dist-sys/2"],
     "MapReduce (2004)", "A Philosophy of Software Design: kitabın 1/4-i", APOSD, "Həftəlik qeyd"),
    ("Broadcast: ilk hissələr", ["https://fly.io/dist-sys/3a"],
     "GFS (2003)", "A Philosophy of Software Design: 2/4", APOSD, "ADR #1"),
    ("Broadcast: qalan hissələr", ["https://fly.io/dist-sys/3a"],
     "Chain Replication (2004)", "A Philosophy of Software Design: 3/4", APOSD, "Həftəlik qeyd"),
    ("Grow-Only Counter", ["https://fly.io/dist-sys/4"],
     "ZooKeeper (2010)", "A Philosophy of Software Design: son 1/4", APOSD, "ADR #2"),
    ("Kafka-Style Log", ["https://fly.io/dist-sys/5a"],
     "Linearizability (Herlihy), 3.1-ə qədər", "The Hard Parts: fəsil 1–2", HARD, "Həftəlik qeyd"),
    ("Totally-Available Transactions", ["https://fly.io/dist-sys/6a"],
     "Distributed Transactions (6.033, fəsil 9, seçilmiş hissələr)", "The Hard Parts: fəsil 12, Transactional Sagas", HARD, "ADR #3"),
    ("MIT Lab 1: MapReduce", ["https://pdos.csail.mit.edu/6.824/labs/lab-mr.html"],
     "Spanner (2012)", "The Hard Parts: fəsil 4, Architectural Decomposition", HARD, "Həftəlik qeyd"),
    ("MIT Lab 2: Key/Value server", ["https://pdos.csail.mit.edu/6.824/labs/lab-kvsrv1.html"],
     "Memcached at Facebook (2013)", "The Hard Parts: işinə uyğun 1 fəsil", HARD, "ADR #4"),
    ("MIT Lab 3: Raft, 1-ci hissə", ["https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html"],
     "Raft (extended): 5-ci bölmənin sonuna qədər", "Staff Engineer (Will Larson): 1-ci yarı", STAFF, "Həftəlik qeyd"),
    ("MIT Lab 3: Raft, 2-ci hissə", ["https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html"],
     "Raft: 7-ci bölmədən sona qədər (6-cı bölmə yox)", "Staff Engineer: 2-ci yarı", STAFF, "ADR #5"),
    ("MIT Lab 3: Raft, 3-cü hissə", ["https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html"],
     "FaRM (2015)", "The Staff Engineer's Path: seçilmiş fəsillər", PATH, "Həftəlik qeyd"),
    ("MIT Lab 3: Raft, bitir, bütün testlər keçsin", ["https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html"],
     "On-demand Container Loading (2023, AWS Lambda)", "The Staff Engineer's Path: davam", PATH, "ADR #6 + 12 həftənin retrosu"),
]


def gh(method, path, body=None):
    if DRY and method != "GET":
        print(f"[dry] {method} {path} {body.get('title') or body.get('name') if body else ''}")
        return {"number": 0}
    cmd = ["gh", "api", "-X", method, f"repos/{REPO}/{path}"]
    if body is not None:
        cmd += ["--input", "-"]
    out = subprocess.run(cmd, input=json.dumps(body) if body else None, capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"{method} {path} failed: {out.stdout} {out.stderr}")
    return json.loads(out.stdout) if out.stdout.strip() else {}


def get_all(path):
    if DRY:
        return []
    items, page = [], 1
    while True:
        batch = gh("GET", f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def issue_bodies(n, w):
    code, links, paper, book, book_link, sunday = w
    blog_name, blog_url = BLOGS[(n - 1) % len(BLOGS)]
    link_lines = "\n".join(f"- {u}" for u in links)
    adr = sunday.startswith("ADR")
    return [
        (f"H{n} · Kod: {code}", ["kod"],
         f"**Vaxt:** Ç.a. 1 saat, C.a. 1 saat, Şənbə 2 saat\n\n**Linklər:**\n{link_lines}\n\n"
         "- [ ] Çərşənbə axşamı: başla, 1 commit\n- [ ] Cümə axşamı: davam, 1 commit\n- [ ] Şənbə: testlər keçir\n\n"
         "Qayda: 45 dəqiqə ilişsən, Fly.io Community-də #dist-sys-challenge tag-inə bax. Həll kodunu LLM-dən alma."),
        (f"H{n} · Paper: {paper}", ["paper"],
         f"**Vaxt:** Bazar ertəsi 1 saat\n\n**Link:** paper linki MIT 6.5840 cədvəlindədir: {SCHEDULE}\n\n"
         "- [ ] Oxu\n- [ ] `notes/papers/`-də 5 sətir yaz: problem, həll, trade-off"),
        (f"H{n} · Kitab: {book}", ["kitab"],
         f"**Vaxt:** Çərşənbə 1 saat\n\n**Link:** {book_link}\n\n"
         "- [ ] Oxu\n- [ ] `notes/books/`-də yaz: 3 fikir + işdə 1 tətbiq ideyası"),
        (f"H{n} · Real dünya: 1 post-mortem + {blog_name}", ["real-dunya"],
         "**Vaxt:** Cümə 1 saat\n\n**Linklər:**\n- Post-mortem: https://github.com/danluu/post-mortems\n"
         f"- Bloq: {blog_url}\n\n"
         "- [ ] 1 post-mortem oxu\n- [ ] 1 bloq yazısı oxu\n- [ ] 1 cavab yaz: \"Bu bizə də ola bilərmi?\""),
        (f"H{n} · Yazı: {sunday}", ["yazi"],
         "**Vaxt:** Bazar 1 saat\n\n"
         + ("- [ ] İşdəki real bir qərarı seç\n- [ ] `adr/0000-template.md`-dən kopyala, 1 səhifə yaz\n"
            "- [ ] Konfidensial detal yoxdur (repo public-dir)\n" if adr else
            "- [ ] `weekly/`-də həftəlik qeyd yaz: nə öyrəndim, harada ilişdim, növbəti həftə nə dəyişir\n")
         + "- [ ] Həftəlik yoxlama: bu milestone-un bütün issue-ları bağlıdır"),
    ]


def main():
    existing_labels = {l["name"] for l in get_all("labels")}
    for name, color, desc in LABELS:
        if name not in existing_labels:
            gh("POST", "labels", {"name": name, "color": color, "description": desc})

    milestones = {m["title"]: m["number"] for m in get_all("milestones?state=all")}
    titles = {i["title"] for i in get_all("issues?state=all") if "pull_request" not in i}

    for n, w in enumerate(WEEKS, start=1):
        mon = START + timedelta(weeks=n - 1)
        sun = mon + timedelta(days=6)
        mtitle = f"Həftə {n:02d} ({mon:%d.%m} – {sun:%d.%m.%Y})"
        if mtitle not in milestones:
            m = gh("POST", "milestones", {
                "title": mtitle,
                "description": f"Kod: {w[0]} · Paper: {w[2]} · Kitab: {w[3]}",
                "due_on": f"{sun.isoformat()}T19:59:00Z",  # Sunday 23:59 Asia/Baku
            })
            milestones[mtitle] = m["number"]
        for title, labels, body in issue_bodies(n, w):
            if title not in titles:
                gh("POST", "issues", {"title": title, "body": body, "labels": labels,
                                      "milestone": milestones[mtitle]})
    print("done")


main()
