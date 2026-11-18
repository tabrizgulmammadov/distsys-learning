# Həftəlik öyrənmə rutini — Senior/Arxitekt yolu (12 həftə)

## Bu repo necə işləyir

- **Backlog:** hər həftə bir [Milestone](https://github.com/tabrizgulmammadov/staff-engineer-path/milestones)-dir. Hər iş bir [Issue](https://github.com/tabrizgulmammadov/staff-engineer-path/issues)-dir.
- **Label-lər:** `kod`, `paper`, `kitab`, `real-dunya`, `yazi`.
- **Həftə bitəndə:** issue-ları bağla. Milestone faizi irəliləyişi göstərir.

| Qovluq | Nə yazılır |
| --- | --- |
| `notes/papers/` | Hər paper üçün 5 sətir: problem, həll, trade-off |
| `notes/books/` | Hər fəsil üçün 3 fikir + işdə 1 tətbiq ideyası |
| `weekly/` | Bazar günü həftəlik qeyd (`2026-W48.md` kimi) |
| `adr/` | ADR-lər, `adr/0000-template.md` şablonu ilə |

Diqqət:

- MIT 6.5840 lab həllərini public repo-ya qoyma. Kursun collaboration policy-sinə bax.
- ADR-lərdə işdəki konfidensial detalları yazma. Repo-nu public etsən, əvvəlcə ADR-ləri yoxla.

Tarix: 18 noyabr 2026

## Xülasə

Plan 12 həftədir: həftədə 8 saat, cəmi 96 saat. Hər gün 1 saat ayırırsan, şənbə günü isə 2 saat.

Vaxtın yarısı öz əlinlə qurmağa gedir. Video sadəcə əlavədir.

| Blok | Həftədə | Pay |
| --- | --- | --- |
| Kod (Go): Gossip Glomers, sonra MIT 6.5840 labları | 4 saat | 50% |
| Oxu: 1 paper + 1 kitab fəsli | 2 saat | 25% |
| Real dünya və yazı: post-mortem, bloq, ADR | 2 saat | 25% |

Başlanğıc: 23 noyabr 2026 (bazar ertəsi). Son: 14 fevral 2027.

## Həftəlik şablon

Hər günün bir işi və bir nəticəsi var. Nəticə olmasa, o günü bitmiş sayma.

| Gün | Vaxt | Fəaliyyət | Nəticə |
| --- | --- | --- | --- |
| Bazar ertəsi | 1 saat | Həftənin paper-ini oxu | 5 sətir qeyd: problem, həll, trade-off |
| Çərşənbə axşamı | 1 saat | Kod: həftənin tapşırığı | 1 commit |
| Çərşənbə | 1 saat | Kitab: həftənin fəsli | 3 fikir + işdə 1 tətbiq ideyası |
| Cümə axşamı | 1 saat | Kod: davam | 1 commit, testlər |
| Cümə | 1 saat | 1 post-mortem + 1 bloq yazısı | 1 cavab: "Bu bizə də ola bilərmi?" |
| Şənbə | 2 saat | Kod: dərin sessiya | Tapşırığın testi keçir |
| Bazar | 1 saat | Yazı: həftəlik qeyd və ya ADR | 1 səhifə |

Cəmi: 8 saat. Bir günü buraxsan, onu şənbəyə əlavə etmə. Sadəcə növbəti gündən davam et.

## 12 həftəlik plan

Həftə 1–6: Gossip Glomers. Həftə 7–12: MIT 6.5840 labları. Paper-lər kodla eyni mövzuda gedir.

| Həftə | Kod (Ç.a., C.a., Ş.) | Paper (B.e.) | Kitab (Ç.) | Bazar yazısı |
| --- | --- | --- | --- | --- |
| 1 | Əvvəlcə [Maelstrom](https://github.com/jepsen-io/maelstrom) qur. Sonra [Echo](https://fly.io/dist-sys/1) və [Unique ID](https://fly.io/dist-sys/2) | MapReduce (2004) | [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/aposd.php): kitabın 1/4-i | Həftəlik qeyd |
| 2 | [Broadcast](https://fly.io/dist-sys/3a): ilk hissələr | GFS (2003) | APOSD: 2/4 | ADR #1 |
| 3 | Broadcast: qalan hissələr | Chain Replication (2004) | APOSD: 3/4 | Həftəlik qeyd |
| 4 | [Grow-Only Counter](https://fly.io/dist-sys/4) | ZooKeeper (2010) | APOSD: son 1/4 | ADR #2 |
| 5 | [Kafka-Style Log](https://fly.io/dist-sys/5a) | Linearizability (Herlihy), 3.1-ə qədər | [Software Architecture: The Hard Parts](https://www.oreilly.com/library/view/software-architecture-the/9781492086888): fəsil 1–2 | Həftəlik qeyd |
| 6 | [Totally-Available Transactions](https://fly.io/dist-sys/6a) | Distributed Transactions (6.033, fəsil 9, seçilmiş hissələr) | The Hard Parts: fəsil 12, Transactional Sagas | ADR #3 |
| 7 | [MIT Lab 1: MapReduce](https://pdos.csail.mit.edu/6.824/labs/lab-mr.html) | Spanner (2012) | The Hard Parts: fəsil 4, Architectural Decomposition | Həftəlik qeyd |
| 8 | [MIT Lab 2: Key/Value server](https://pdos.csail.mit.edu/6.824/labs/lab-kvsrv1.html) | Memcached at Facebook (2013) | The Hard Parts: işinə uyğun 1 fəsil | ADR #4 |
| 9 | [MIT Lab 3: Raft](https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html): 1-ci hissə | Raft (extended): 5-ci bölmənin sonuna qədər | [Staff Engineer](https://staffeng.com/book) (Will Larson): 1-ci yarı | Həftəlik qeyd |
| 10 | Lab 3: 2-ci hissə | Raft: 7-ci bölmədən sona qədər (6-cı bölmə yox) | Staff Engineer: 2-ci yarı | ADR #5 |
| 11 | Lab 3: 3-cü hissə | FaRM (2015) | [The Staff Engineer's Path](https://www.oreilly.com/library/view/the-staff-engineers-path/9781098118723/): seçilmiş fəsillər | Həftəlik qeyd |
| 12 | Lab 3: bitir, bütün testlər keçsin | On-demand Container Loading (2023, AWS Lambda) | The Staff Engineer's Path: davam | ADR #6 + 12 həftənin retrosu |

Paper-lərin linkləri [MIT 6.5840 schedule](https://pdos.csail.mit.edu/6.824/schedule.html) səhifəsində hər mühazirənin yanındadır. Raft labı 4 həftədən uzun çəkə bilər. Bu normaldır: planı bir həftə sürüşdür.

## Mənbələr və linklər

Linkləri 18 noyabr 2026-da açıb yoxladım. "Ayrıca açılmayıb" yazılan sətirlərdə linki başqa rəsmi səhifədə gördüm, özünü ayrıca açmadım.

| Mənbə | Harada | Status |
| --- | --- | --- |
| [Gossip Glomers](https://fly.io/dist-sys/) | Kod, həftə 1–6 | Açıldı: 6 tapşırıq |
| [Maelstrom](https://github.com/jepsen-io/maelstrom) | Kod, həftə 1 | Fly.io səhifəsindən götürülüb, ayrıca açılmayıb |
| [MIT 6.5840](https://pdos.csail.mit.edu/6.824/) | Kod və paper, həftə 1–12 | Açıldı: Spring 2026 |
| [MIT 6.5840 schedule](https://pdos.csail.mit.edu/6.824/schedule.html) | Paper linkləri | Açıldı |
| [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/aposd.php) | Kitab, həftə 1–4 | Müəllifin səhifəsi, axtarışda tapıldı |
| [Software Architecture: The Hard Parts](https://www.oreilly.com/library/view/software-architecture-the/9781492086888) | Kitab, həftə 5–8 | O'Reilly səhifəsi tapıldı |
| [Staff Engineer](https://staffeng.com/book) | Kitab, həftə 9–10 | Açıldı: kitabın çoxu saytda pulsuzdur |
| [The Staff Engineer's Path](https://www.oreilly.com/library/view/the-staff-engineers-path/9781098118723/) | Kitab, həftə 11–12 | O'Reilly səhifəsi tapıldı |
| [Dan Luu: post-mortems](https://github.com/danluu/post-mortems) | Cümə: post-mortem | Açıldı |
| [Google SRE kitabı](https://sre.google/sre-book/table-of-contents/) | Cümə: post-mortem əvəzinə 1 fəsil | Açıldı: CC BY-NC-ND lisenziyası |
| [Marc Brooker](https://brooker.co.za/blog/) | Cümə: bloq | Açıldı: son yazı 16.11.2026 |
| [Murat Demirbas](https://muratbuffalo.blogspot.com/) | Cümə: bloq | Açıldı: son yazı 18.11.2026 |
| [Jack Vanlightly](https://jack-vanlightly.com/) | Cümə: bloq | Açıldı: son yazı 28.08.2026 |
| [Architecture Weekly](https://www.architecture-weekly.com/) (Oskar Dudycz) | Cümə: bloq | Açıldı, son yazının tarixi görünmədi |
| [Jepsen analizləri](https://jepsen.io/analyses) | Cümə: bloq | Fly.io səhifəsindən götürülüb, ayrıca açılmayıb |
| [ADR şablonları](https://adr.github.io/adr-templates/) | Bazar: ADR | adr.github.io səhifəsində görüldü |
| [Nygard: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html) | Bazar: ADR | adr.github.io səhifəsindən götürülüb, ayrıca açılmayıb |

12 həftədən sonra: [CMU 15-445 Database Systems](https://15445.courses.cs.cmu.edu/) (videolar CMU-DB YouTube kanalındadır), [Learning Domain-Driven Design](https://www.oreilly.com/library/view/-/9781098100124), [DDIA 2-ci nəşr](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/).

## Qaydalar

- **Video:** həftədə ən çox 1 saat, planın bitdiyi günlərdə. Plandakı işi videoya dəyişmə.
- **45 dəqiqə qaydası:** 45 dəqiqə ilişsən, Fly.io Community Discourse-da #dist-sys-challenge tag-inə bax. Sonra özün davam et.
- **LLM qaydası:** həll kodunu LLM-dən alma. Konsept haqqında soruş, kodu özün yaz. Məqsəd kodun özü deyil, sistemin necə sıradan çıxdığını başında qurmaqdır.
- **ADR:** işdəki real bir qərarı seç. Nygard şablonu: Title, Status, Context, Decision, Consequences. 1 səhifədən uzun yazma.
- **Gecikmə:** plan tarixə bağlı deyil. Həftəni buraxsan, cədvəldə eyni sətrdən davam et.

Bazar günü yoxla:

- [ ] 3 kod sessiyası oldu
- [ ] Paper qeydi yazıldı
- [ ] Kitab qeydi yazıldı
- [ ] 1 post-mortem və 1 bloq yazısı oxundu
- [ ] Bazar yazısı (qeyd və ya ADR) bitdi
