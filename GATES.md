# Gates: CV and portfolio refresh (fifth security CV, XYZ rewrite, dash and slop sweep, site/CV parity)

OWNS: cv/**, index.html, Caddyfile, .gitignore, README.md, portfolio-projects.md, GATES.md

Scope: five CVs generated from one content source in Google XYZ form, a new Penetration Testing CV, the site Experience rewritten in XYZ (EN and AR) with the freelance row added, no em dashes or AI-sounding copy anywhere, and site/CV facts identical, verified by a repository-owned checker and by screenshots of the live deployment.

- [x] G0: this ledger states outcomes that can fail
  CHECK: node /home/daaz_/.claude/skills/unlazy/scripts/gate-lint.mjs GATES.md
  EXPECT: LINT OK
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=99c8201436305b613d766265eccd8d1911f3d021c84545bae3a7f18be87e05c3; output-bytes=411

- [x] G1: the generator rebuilds all five CV pages and PDFs from cv/src/content.py without error
  CHECK: PYTHONDONTWRITEBYTECODE=1 python3 cv/src/build.py
  EXPECT: BUILD OK 5/5
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=150d584a3ca18481fa5d6ddcb9860b7a83fc378c7586f1512a068bd2785ad59e; output-bytes=114

- [x] G2: PDF page counts measured by pdfinfo are merged 2, pentest 2, appsec 2, software 2, software-1page 1
  CHECK: python3 cv/src/check.py pages
  EXPECT: PAGES OK
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=acf1e34a1951ffa7362a622a36865d8f6d1020698c91b2bd88a9868c687d500a; output-bytes=9

- [x] G3: no em dash (literal or entity) remains in the prose of index.html, cv/index.html or any generated CV, after stripping style, script and comments
  CHECK: python3 cv/src/check.py dashes
  EXPECT: DASHES 0
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=37dc0bdfe66e59c4912e41972b702b463327cffd340df93af83c44112447a736; output-bytes=9

- [x] G4: no phrase from the slop list remains in the prose of the site, the hub or any CV
  CHECK: python3 cv/src/check.py slop
  EXPECT: SLOP 0
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=b424d9b3a37f8b4cceab25ef22cd7d03133014868545fa13fd54a58cf7dc10de; output-bytes=7

- [x] G5: every en dash in prose sits inside an allowed date or number range pattern
  CHECK: python3 cv/src/check.py ranges
  EXPECT: RANGES OK
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=85b53658c963bb37c7b656029c94041f0c2268861079e20f47d99768b067b1ee; output-bytes=10

- [x] G6: every role title, period and shared figure declared in cv/src/content.py appears verbatim in index.html and in every CV that includes that role
  CHECK: python3 cv/src/check.py parity
  EXPECT: PARITY OK
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=db2ef08983a73c1eb980c7760310833d67b6a8cc4cf977e5af33180fdbb9dac9; output-bytes=10

- [x] G7: no commit-count claim remains anywhere in prose (the word "commit" only inside "pre-commit")
  CHECK: python3 cv/src/check.py commits
  EXPECT: COMMITS 0
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=4ecbc136fa65eda26703a0ffda1eea29b120d97d82113d42c713121d5809d439; output-bytes=10

- [x] G8: the hub lists exactly five CV cards and each card's HTML and PDF file exists
  CHECK: python3 cv/src/check.py hub
  EXPECT: HUB 5/5
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=4acce78a702d6302b7d6059cc9b07d0a5007bfdc20f6044481f87c3a959f8e41; output-bytes=8

- [x] G9: required new content is present (pentest CV, bug bounty platforms, freelance row, toolkit) and retired content is absent (Freelance Flutter App card, 372/381, Packet Tracer, Recruiter-ready, Freelance Mobile Developer)
  CHECK: python3 cv/src/check.py required
  EXPECT: REQUIRED OK
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=9be9822ecadfca3a5361650d3b616df9d37dae5c93a8ffb54c527af96d098afb; output-bytes=12

- [x] G10: every English span in the site's Experience, Security, Skills and Contact sections has an Arabic sibling, and no Arabic string contains an em dash
  CHECK: python3 cv/src/check.py bilingual
  EXPECT: BILINGUAL OK
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=057ea12fb2edfdc447c61bf212bb8c314e6d85551328f21af78ac156596f47b7; output-bytes=13

- [x] G11: cv/src is not served (Caddyfile hides /cv/src/*) and Python bytecode is ignored by git
  CHECK: python3 cv/src/check.py serve
  EXPECT: SERVE OK
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=50cf98a75a96824789175fb6fc0c0ffd02104238978754c582d353581e1973e7; output-bytes=9

- [x] G12: the checker's absence tests fail on known-positive fixtures (an em dash, a slop phrase, a commit count, a stray en dash, a missing Arabic sibling each make the corresponding subcommand exit nonzero)
  CHECK: python3 cv/src/check.py selftest
  EXPECT: SELFTEST OK
  EVIDENCE: exit=0; shell=/bin/sh; cwd=/home/daaz_/Downloads/Life/Portfolio; path=eaed0b040f1e/13 entries; EXPECT=matched; output-sha256=a375a9767b166ca9b90914835eef192a5f7cd2acba5a09d7b5f16a008ecd5e38; output-bytes=12

- [x] G13: screenshots of /, /cv/ and all five CVs render correctly in dark and light themes at desktop and 400 px width, and the Arabic toggle shows the freelance row and rewritten bullets
  EVIDENCE: 2026-09-12 reviewed by the orchestrator in Chrome DevTools against http://127.0.0.1:8765: hero at 1440 dark+light, 1920 dark, 1440 Arabic, 400 mobile dark (chip row under the phone, no chip touches text or the phone screen; scrollWidth <= innerWidth at every width); terminal at 400 wraps (term-body scrollWidth == clientWidth 353); PDFs rendered via pdftoppm and inspected (merged, pentest, appsec, software 2 pages, software-1page 1 page, no orphaned headings). Visual QA agent screenshots qa-*.jpeg and fix-*.jpeg in the session scratchpad cover /cv/ (5 cards, 10 links 200) and every CV page at 1100 and 400; console empty on / and /cv/.

- [ ] G14: after push, the live site serves the new content on /, /cv/ and /cv/pentest.html, and /cv/src/content.py returns 404
  CHECK: python3 cv/src/check.py live
  EXPECT: LIVE OK
  EVIDENCE: pending
