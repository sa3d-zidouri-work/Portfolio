#!/usr/bin/env python3
"""Gate oracle for GATES.md. Run from the repository root:

    python3 cv/src/check.py <subcommand>

Each subcommand prints its success token (see GATES.md) and exits 0 only when
every assertion holds. On any failure it prints "<NAME> FAIL" followed by one
diagnostic line per offending location and exits 1. Standard library only.
"""

import sys

sys.dont_write_bytecode = True

import html as htmllib  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import urllib.error  # noqa: E402
import urllib.request  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
sys.path.insert(0, HERE)

import content  # noqa: E402
import variants  # noqa: E402

SITE = "index.html"
HUB = "cv/index.html"
CVS = [
    "cv/merged.html",
    "cv/pentest.html",
    "cv/appsec.html",
    "cv/software.html",
    "cv/software-1page.html",
]
ALL = [SITE, HUB] + CVS

PDFINFO = "/usr/bin/pdfinfo"
LIVE_BASE = "https://portfolio-production-5c1c.up.railway.app"
USER_AGENT = "portfolio-gate-check/1.0 (+cv/src/check.py)"

EM = "\u2014"  # em dash
EN = "\u2013"  # en dash

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def load(path):
    """Read a repository-relative file as UTF-8."""
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def exists(path):
    return os.path.isfile(os.path.join(ROOT, path))


_SCRUB = re.compile(r"<!--.*?-->|<(style|script)\b[^>]*>.*?</\1\s*>", re.S | re.I)
_TAG = re.compile(r"<(?:/?[A-Za-z][^>]*|![^>]*)>", re.S)
_TAG_NAME = re.compile(r"</?([A-Za-z][A-Za-z0-9-]*)")
_WS = re.compile(r"\s+")

# Inline formatting tags vanish without leaving a space, because they are
# glued to words and punctuation ("<b>15 branches</b>."). Everything else
# (span, br, p, li, h*, ...) becomes a space so adjacent blocks stay apart.
_INLINE = frozenset(
    "a abbr b bdi bdo cite code del dfn em i ins kbd mark q s small strong sub sup time u var wbr".split()
)


def _newlines_of(match):
    return "\n" * match.group(0).count("\n")


def scrub(html):
    """Blank comments, <style> and <script> blocks while keeping line numbers."""
    return _SCRUB.sub(_newlines_of, html)


def _tag_gap(match):
    tag = match.group(0)
    name = _TAG_NAME.match(tag)
    gap = "" if name and name.group(1).lower() in _INLINE else " "
    return gap + "\n" * tag.count("\n")


def collapse(text):
    return _WS.sub(" ", text).strip()


def strip_tags(html):
    return _TAG.sub(_tag_gap, html)


def prose_lines(html):
    """(source line number, visible text) for every non-empty line."""
    text = strip_tags(scrub(html))
    out = []
    for number, line in enumerate(text.split("\n"), 1):
        line = collapse(htmllib.unescape(line))
        if line:
            out.append((number, line))
    return out


def prose(html):
    """The text a reader sees: no comments, style, script or tags; unescaped."""
    return collapse(" ".join(text for _, text in prose_lines(html)))


def snippet(text, index, width=48):
    start = max(0, index - width)
    end = min(len(text), index + width)
    head = "..." if start else ""
    tail = "..." if end < len(text) else ""
    return head + text[start:end] + tail


def line_of(source, offset):
    return source.count("\n", 0, offset) + 1


def load_all(paths, diags):
    """Yield (path, html) for the paths that exist; record the missing ones."""
    for path in paths:
        if exists(path):
            yield path, load(path)
        else:
            diags.append(f"{path}: missing")


# ---------------------------------------------------------------------------
# Core scanners. Each takes (path, html) and returns diagnostic lines so the
# selftest can run them on in-memory fixtures.
# ---------------------------------------------------------------------------


def em_dash_hits(path, html):
    hits = []
    for number, line in prose_lines(html):
        for match in re.finditer(EM, line):
            hits.append(f"{path}:{number}: {snippet(line, match.start())}")
    scrubbed = scrub(html)
    for match in _TAG.finditer(scrubbed):
        tag = collapse(match.group(0))
        index = tag.find("&mdash;")
        if index >= 0:
            hits.append(
                f"{path}:{line_of(scrubbed, match.start())}: &mdash; inside markup: {snippet(tag, index)}"
            )
    return hits


SLOP = [
    "seamless",
    "robust",
    "cutting-edge",
    "passionate",
    "leverag",
    "delve",
    "elevate",
    "empower",
    "unlock",
    "tapestry",
    "testament",
    "game-chang",
    "I answer fast",
    "could be yours",
    "in my own dialect",
    "line by line",
    "don't have to",
    "Recruiter-ready",
    "أردّ سريعًا",
    "سطرًا بسطر",
]
_JOURNEY_JOY = re.compile(r"journey\s+joy", re.I)
_SLOP_RE = [(phrase, re.compile(re.escape(phrase.lower()), re.I)) for phrase in SLOP]


def slop_hits(path, html):
    hits = []
    for number, line in prose_lines(html):
        cleaned = _JOURNEY_JOY.sub("", line).replace("\u2019", "'")
        for phrase, pattern in _SLOP_RE:
            for match in pattern.finditer(cleaned):
                hits.append(f"{path}:{number}: '{phrase}': {snippet(cleaned, match.start())}")
    return hits


_MON = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
_AR = "[\u0600-\u06FF]"
_ALLOWED_RANGE = re.compile(
    "|".join(
        [
            rf"\b{_MON} {EN} {_MON} \d{{4}}\b",
            rf"\b{_MON} \d{{4}} {EN} Present\b",
            rf"\b{_MON} \d{{4}} {EN} {_MON} \d{{4}}\b",
            rf"\b\d{{4}} {EN} \d{{4}}\b",
            rf"\d+{EN}\d+",
        ]
    )
)
# On a line that carries Arabic letters, a spaced en dash between two tokens
# is a month or year range when each side is an Arabic word or a number.
_ALLOWED_RANGE_AR = re.compile(rf"(?:\S*{_AR}\S*|\d+) {EN} (?:\S*{_AR}\S*|\d+)")
_HAS_ARABIC = re.compile(_AR)


def range_hits(path, html):
    hits = []
    for number, line in prose_lines(html):
        if EN not in line:
            continue
        spans = [m.span() for m in _ALLOWED_RANGE.finditer(line)]
        if _HAS_ARABIC.search(line):
            spans += [m.span() for m in _ALLOWED_RANGE_AR.finditer(line)]
        for match in re.finditer(EN, line):
            index = match.start()
            if not any(start <= index < end for start, end in spans):
                hits.append(f"{path}:{number}: {snippet(line, index)}")
    return hits


_COMMIT = re.compile(r"\bcommits?\b", re.I)


def commit_hits(path, html):
    hits = []
    for number, line in prose_lines(html):
        for match in _COMMIT.finditer(line):
            if line[max(0, match.start() - 4) : match.start()].lower() == "pre-":
                continue
            hits.append(f"{path}:{number}: {snippet(line, match.start())}")
    return hits


BILINGUAL_SECTIONS = ["experience", "security", "skills", "contact"]
_SPAN_TOKEN = re.compile(r"<span\b[^>]*>|</span\s*>", re.I)
_AR_SPAN_OPEN = re.compile(r'<span\b[^>]*\bclass="ar"[^>]*>', re.I)
_SECTION_BREAK = re.compile(r"<section\b|</main\b", re.I)


def ar_spans(scrubbed):
    """(line number, visible text) of every <span class="ar"> in scrubbed source."""
    out = []
    for match in _AR_SPAN_OPEN.finditer(scrubbed):
        depth = 1
        position = match.end()
        close_at = len(scrubbed)
        while depth:
            token = _SPAN_TOKEN.search(scrubbed, position)
            if token is None:
                break
            depth += -1 if token.group(0).startswith("</") else 1
            position = token.end()
            if depth == 0:
                close_at = token.start()
        inner = scrubbed[match.end() : close_at]
        text = collapse(htmllib.unescape(strip_tags(inner)))
        out.append((line_of(scrubbed, match.start()), text))
    return out


def bilingual_report(path, html):
    """(problems, per-section count lines) for the site's bilingual sections."""
    problems = []
    counts = []
    scrubbed = scrub(html)
    for section_id in BILINGUAL_SECTIONS:
        opener = re.search(rf'<section\b[^>]*\bid="{section_id}"[^>]*>', scrubbed, re.I)
        if opener is None:
            problems.append(f"{path}: section #{section_id} not found")
            continue
        stop = _SECTION_BREAK.search(scrubbed, opener.end())
        body = scrubbed[opener.start() : stop.start() if stop else len(scrubbed)]
        en = body.count('class="en"')
        ar = body.count('class="ar"')
        number = line_of(scrubbed, opener.start())
        verdict = "ok" if en == ar else "MISMATCH"
        counts.append(f"{path}:{number}: section #{section_id} en={en} ar={ar} {verdict}")
        if en != ar:
            problems.append(f"{path}:{number}: section #{section_id} en={en} ar={ar}")
    for number, text in ar_spans(scrubbed):
        index = text.find(EM)
        if index >= 0:
            problems.append(f"{path}:{number}: em dash in Arabic span: {snippet(text, index)}")
    return problems, counts


# ---------------------------------------------------------------------------
# Subcommands. Each returns (ok, lines to print on failure).
# ---------------------------------------------------------------------------


def check_pages():
    problems = []
    lines = []
    for variant in variants.VARIANTS:
        pdf = f"cv/{variant['file']}.pdf"
        expected = variant["pages"]
        if not exists(pdf):
            lines.append(f"{pdf}: missing, expected {expected}")
            problems.append(pdf)
            continue
        try:
            result = subprocess.run(
                [PDFINFO, os.path.join(ROOT, pdf)],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired) as error:
            lines.append(f"{pdf}: cannot run {PDFINFO}: {error}")
            problems.append(pdf)
            continue
        match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.M)
        if result.returncode != 0 or match is None:
            detail = collapse(result.stderr)[:120] or "no Pages: line"
            lines.append(f"{pdf}: pdfinfo failed: {detail}")
            problems.append(pdf)
            continue
        measured = int(match.group(1))
        verdict = "ok" if measured == expected else "MISMATCH"
        lines.append(f"{pdf}: measured {measured}, expected {expected} {verdict}")
        if measured != expected:
            problems.append(pdf)
    return not problems, lines


def check_dashes():
    diags = []
    for path, html in load_all(ALL, diags):
        diags.extend(em_dash_hits(path, html))
    return not diags, diags


def check_slop():
    diags = []
    for path, html in load_all(ALL, diags):
        diags.extend(slop_hits(path, html))
    return not diags, diags


def check_ranges():
    diags = []
    for path, html in load_all(ALL, diags):
        diags.extend(range_hits(path, html))
    return not diags, diags


def check_commits():
    diags = []
    for path, html in load_all(ALL, diags):
        diags.extend(commit_hits(path, html))
    return not diags, diags


def _require(haystack, needle, path, diags, label):
    if collapse(needle) not in haystack:
        diags.append(f"{path}: missing {label} {needle!r}")


def check_parity():
    diags = []
    roles = content.ROLES

    if exists(SITE):
        site = prose(load(SITE))
        for role_id in content.ROLE_ORDER:
            role = roles[role_id]
            _require(site, role["title"], SITE, diags, f"role title ({role_id})")
            _require(site, role["period"], SITE, diags, f"role period ({role_id})")
        shown = {}
        for variant in variants.VARIANTS:
            for role_id in variant["roles"]:
                for text in variants.bullets_for(variant, roles[role_id]):
                    shown.setdefault(text, role_id)
        for text, role_id in shown.items():
            _require(site, text, SITE, diags, f"bullet ({role_id})")
        for figure in content.FIGURES:
            _require(site, figure, SITE, diags, "figure")
    else:
        diags.append(f"{SITE}: missing")

    merged = "cv/merged.html"
    if exists(merged):
        merged_prose = prose(load(merged))
        for figure in content.FIGURES:
            _require(merged_prose, figure, merged, diags, "figure")
    else:
        diags.append(f"{merged}: missing")

    for variant in variants.VARIANTS:
        path = f"cv/{variant['file']}.html"
        if not exists(path):
            diags.append(f"{path}: missing")
            continue
        text = prose(load(path))
        for role_id in variant["roles"]:
            role = roles[role_id]
            _require(text, role["title"], path, diags, f"role title ({role_id})")
            _require(text, role["period"], path, diags, f"role period ({role_id})")
    return not diags, list(dict.fromkeys(diags))


def _resolve_hub_href(href):
    """Repository path for a hub link, or None when it leaves cv/."""
    href = href.split("#", 1)[0].split("?", 1)[0].strip()
    if not href or re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I) or href.startswith("//"):
        return None
    if href.startswith("/"):
        candidate = os.path.normpath(href.lstrip("/"))
    else:
        candidate = os.path.normpath(os.path.join("cv", href))
    if candidate == "cv" or not candidate.startswith("cv" + os.sep):
        return None
    return candidate.replace(os.sep, "/")


def check_hub():
    if not exists(HUB):
        return False, [f"{HUB}: missing"]
    source = scrub(load(HUB))
    cards = list(re.finditer(r'<article\b[^>]*\bclass="card"[^>]*>', source, re.I))
    diags = []
    if len(cards) != 5:
        diags.append(f"{HUB}: {len(cards)} <article class=\"card\"> elements, expected 5")
    for index, card in enumerate(cards, 1):
        number = line_of(source, card.start())
        close = source.find("</article", card.end())
        body = source[card.end() : close if close >= 0 else len(source)]
        for css_class in ("btn-view", "btn-dl"):
            hrefs = []
            for anchor in re.finditer(r"<a\b[^>]*>", body, re.I):
                tag = anchor.group(0)
                classes = re.search(r'\bclass="([^"]*)"', tag)
                if classes and css_class in classes.group(1).split():
                    href = re.search(r'\bhref="([^"]*)"', tag)
                    hrefs.append(href.group(1) if href else "")
            if len(hrefs) != 1:
                diags.append(f"{HUB}:{number}: card {index} has {len(hrefs)} .{css_class} links, expected 1")
                continue
            target = _resolve_hub_href(hrefs[0])
            if target is None:
                diags.append(f"{HUB}:{number}: card {index} .{css_class} href {hrefs[0]!r} does not point under cv/")
            elif not exists(target):
                diags.append(f"{HUB}:{number}: card {index} .{css_class} href {hrefs[0]!r}: {target} does not exist")
    return not diags, diags


REQUIRED_SITE = ["Freelance Software Engineer", "BugBounty.sa", "HackerOne", "Bugcrowd"]
REQUIRED_PENTEST = ["Penetration Testing", "BugBounty.sa"]
REQUIRED_EVERY_CV = ["Freelance Software Engineer"]
RETIRED = [
    "Freelance Flutter App",
    "372",
    "381",
    "Packet Tracer",
    "Recruiter-ready",
    "Freelance Mobile Developer",
    "21 security",
]
_RETIRED_RE = [(phrase, re.compile(re.escape(phrase), re.I)) for phrase in RETIRED]


def check_required():
    diags = []
    if exists(SITE):
        site = prose(load(SITE))
        for needle in REQUIRED_SITE:
            _require(site, needle, SITE, diags, "required text")
    else:
        diags.append(f"{SITE}: missing")

    pentest = "cv/pentest.html"
    if exists(pentest):
        text = prose(load(pentest))
        for needle in REQUIRED_PENTEST:
            _require(text, needle, pentest, diags, "required text")
    else:
        diags.append(f"{pentest}: missing")

    for path in CVS:
        if exists(path):
            text = prose(load(path))
            for needle in REQUIRED_EVERY_CV:
                _require(text, needle, path, diags, "required text")
        elif path != pentest:
            diags.append(f"{path}: missing")

    for path, html in load_all(ALL, []):
        for number, line in prose_lines(html):
            for phrase, pattern in _RETIRED_RE:
                for match in pattern.finditer(line):
                    diags.append(f"{path}:{number}: retired {phrase!r}: {snippet(line, match.start())}")
    return not diags, diags


def check_bilingual():
    if not exists(SITE):
        return False, [f"{SITE}: missing"]
    problems, counts = bilingual_report(SITE, load(SITE))
    return not problems, counts + problems if problems else []


def check_serve():
    diags = []
    if exists("Caddyfile"):
        seen = False
        for number, raw in enumerate(load("Caddyfile").splitlines(), 1):
            line = raw.strip()
            if line.startswith("@hidden path"):
                seen = True
                if "/cv/src/*" not in line.split():
                    diags.append(f"Caddyfile:{number}: '@hidden path' lacks /cv/src/*: {line}")
        if not seen:
            diags.append("Caddyfile: no '@hidden path' line")
    else:
        diags.append("Caddyfile: missing")

    if exists(".gitignore"):
        lines = [raw.strip() for raw in load(".gitignore").splitlines()]
        if "__pycache__/" not in lines:
            diags.append(".gitignore: no '__pycache__/' line")
    else:
        diags.append(".gitignore: missing")
    return not diags, diags


def _fetch(path):
    request = urllib.request.Request(LIVE_BASE + path, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        try:
            body = error.read().decode("utf-8", "replace")
        except OSError:
            body = ""
        return error.code, body
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return None, str(error)


LIVE_EXPECTATIONS = [
    ("/", 200, "Freelance Software Engineer"),
    ("/cv/", 200, "Penetration Testing"),
    ("/cv/pentest.html", 200, "BugBounty.sa"),
    ("/cv/src/content.py", 404, None),
]


def check_live():
    diags = []
    for path, status, needle in LIVE_EXPECTATIONS:
        got, body = _fetch(path)
        if got is None:
            diags.append(f"GET {path}: error: {body}")
            continue
        wrong = []
        if got != status:
            wrong.append(f"expected {status}")
        if needle and needle not in body and needle not in prose(body):
            wrong.append(f"body lacks {needle!r}")
        if wrong:
            diags.append(f"GET {path}: HTTP {got}, " + ", ".join(wrong))
    return not diags, diags


def check_selftest():
    failures = []

    def expect(condition, label):
        if not condition:
            failures.append(label)

    expect(em_dash_hits("a.html", f"<p>foo {EM} bar</p>"), "(a) literal em dash in prose not detected")
    expect(em_dash_hits("b.html", "<p>foo &mdash; bar</p>"), "(b) &mdash; in prose not detected")
    hidden = (
        f"<style>p::before{{content:'{EM}'}}</style>\n"
        f"<script>var s = '{EM}';</script>\n"
        f"<!-- {EM} &mdash; -->\n<p>plain</p>"
    )
    expect(not em_dash_hits("c.html", hidden), "(c) em dash inside style, script or comment was counted")
    expect(slop_hits("d.html", "<p>I answer fast.</p>"), "(d) 'I answer fast' not detected")
    expect(slop_hits("d2.html", "<p>A ROBUST pipeline</p>"), "(d) case-insensitive slop word not detected")
    expect(commit_hits("e.html", "<p>412 commits on main</p>"), "(e) 'commits' not detected")
    expect(commit_hits("e2.html", "<p>One Commit.</p>"), "(e) 'Commit' not detected")
    expect(not commit_hits("e3.html", "<p>a pre-commit secret scanner</p>"), "(e) 'pre-commit' was flagged")
    expect(range_hits("f.html", f"<p>Flutter {EN} Dart</p>"), "(f) stray en dash not detected")
    expect(range_hits("f2.html", "<p>Flutter &ndash; Dart</p>"), "(f) stray &ndash; not detected")
    for allowed in [
        f"Jan {EN} May 2026",
        f"Mar 2026 {EN} Present",
        f"Sep 2025 {EN} Jan 2026",
        f"2025 {EN} 2026",
        f"10{EN}15 s",
        f"يناير {EN} مايو 2026",
        f"مايو 2026 {EN} حتى الآن",
    ]:
        expect(not range_hits("g.html", f"<p>{allowed}</p>"), f"(g) allowed range {allowed!r} was flagged")
    lonely = (
        '<main><section id="experience"><span class="en">Only English</span></section>'
        '<section id="security"><span class="en">A</span><span class="ar" lang="ar">أ</span></section>'
        '<section id="skills"><span class="en">B</span><span class="ar" lang="ar">ب</span></section>'
        '<section id="contact"><span class="en">C</span><span class="ar" lang="ar">ج</span></section></main>'
    )
    problems, _ = bilingual_report("h.html", lonely)
    expect(problems, "(h) English span without Arabic sibling not detected")
    paired = lonely.replace('<span class="en">Only English</span>', '<span class="en">E</span><span class="ar" lang="ar">ع</span>')
    problems, counts = bilingual_report("h2.html", paired)
    expect(not problems and len(counts) == 4, "(h) balanced sections were reported as a problem")
    dashed = paired.replace('<span class="ar" lang="ar">ع</span>', f'<span class="ar" lang="ar">ع {EM} ع</span>')
    problems, _ = bilingual_report("h3.html", dashed)
    expect(problems, "(h) em dash inside an Arabic span not detected")
    stripped = prose("<p>daily by <b>300+ staff</b> across <b>15 branches</b>.</p>\n<p>next</p>")
    expect(stripped == "daily by 300+ staff across 15 branches. next", f"(i) prose() mangles inline tags: {stripped!r}")
    return not failures, failures


TOKENS = {
    "pages": ("PAGES OK", check_pages),
    "dashes": ("DASHES 0", check_dashes),
    "slop": ("SLOP 0", check_slop),
    "ranges": ("RANGES OK", check_ranges),
    "parity": ("PARITY OK", check_parity),
    "commits": ("COMMITS 0", check_commits),
    "hub": ("HUB 5/5", check_hub),
    "required": ("REQUIRED OK", check_required),
    "bilingual": ("BILINGUAL OK", check_bilingual),
    "serve": ("SERVE OK", check_serve),
    "selftest": ("SELFTEST OK", check_selftest),
    "live": ("LIVE OK", check_live),
}
ALL_ORDER = ["pages", "dashes", "slop", "ranges", "parity", "commits", "hub", "required", "bilingual", "serve"]


def run(name):
    token, function = TOKENS[name]
    ok, lines = function()
    if ok:
        print(token)
    else:
        print(f"{name.upper()} FAIL")
        for line in lines:
            print(f"  {line}")
    return ok


def main(argv):
    if len(argv) != 2 or argv[1] not in TOKENS and argv[1] != "all":
        names = ", ".join(list(TOKENS) + ["all"])
        print(f"usage: python3 cv/src/check.py <{names}>", file=sys.stderr)
        return 2
    if argv[1] == "all":
        results = [run(name) for name in ALL_ORDER]
        return 0 if all(results) else 1
    return 0 if run(argv[1]) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
