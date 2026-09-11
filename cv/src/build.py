#!/usr/bin/env python3
"""Generate the five CV pages and PDFs from content.py and variants.py.

    PYTHONDONTWRITEBYTECODE=1 python3 cv/src/build.py [--no-pdf]

Writes cv/<file>.html for every variant, prints each one to cv/<file>.pdf
with headless Chrome, measures the page count with pdfinfo and compares it
to variant["pages"]. Prints "BUILD OK 5/5" and exits 0 only when every
count matches; otherwise prints "BUILD FAIL" and exits 1. --no-pdf writes
the HTML only and reports "HTML OK 5/5" instead.

Python 3, standard library only.
"""

import os
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SRC)
sys.path.insert(0, SRC)

import content  # noqa: E402
import template  # noqa: E402
import variants  # noqa: E402

CHROME = "/usr/bin/google-chrome"
PDFINFO = "/usr/bin/pdfinfo"

esc = template.esc

# Heading of the security section per variant id; anything else gets the default.
SECURITY_HEADINGS = {"pentest": "Security experience", "appsec": "Security experience"}
SECURITY_HEADING_DEFAULT = "Security record"


# ----- sections ---------------------------------------------------------------

def render_summary(v):
    return template.section("summary", "Summary", template.paragraph("summary", esc(content.SUMMARIES[v["summary"]])))


def render_experience(v):
    entries = []
    for rid in v["roles"]:
        role = content.ROLES[rid]
        items = variants.bullets_for(v, role)
        if not items:
            continue
        entries.append(template.entry(
            role["title"], role["period"], role["org"], role["loc"],
            [esc(t) for t in items],
            org_note=role.get("org_note"), engagement=role.get("engagement"),
        ))
    return template.section("experience", "Experience", "\n".join(entries))


def render_security(v):
    if not v.get("security"):
        return ""
    rec = content.SECURITY["bounty"]
    items = [esc(text) for tags, text in rec["bullets"] if tags in v["tags"]]
    if not items:
        return ""
    heading = SECURITY_HEADINGS.get(v["id"], SECURITY_HEADING_DEFAULT)
    entry = template.entry(rec["title"], rec["period"], rec["org"], rec["loc"], items)
    return template.section("security", heading, entry)


def render_projects(v):
    key = v["project_text"]
    cards = []
    for pid in v["projects"]:
        p = content.PROJECTS[pid]
        tag = p["tag_sec"] if key == "text_sec" and "tag_sec" in p else p["tag"]
        text = p.get(key, p["text"])
        cards.append(template.project(p["title"], tag, text))
    return template.section("projects", "Projects", template.project_grid(cards))


def render_skills(v):
    rows = [content.SKILLS[k] for k in v["skills"]]
    return template.section("skills", "Technical Skills", template.skills(rows))


def render_education(v):
    e = content.EDUCATION
    items = [
        esc(e["rank"]),
        f'<span class="k">Relevant coursework:</span> {esc(e[v["coursework"]])}',
    ]
    entry = template.entry(e["degree"], e["period"], e["school"], e["gpa"], items)
    return template.section("education", "Education", entry)


def render_certs(v):
    show_verify = "sec" in v["tags"]
    items = []
    for name, detail, url in content.CERTS:
        li = f"<strong>{esc(name)}</strong>: {esc(detail)}" if name else esc(detail)
        if url and show_verify:
            li += " " + template.verify_link(url)
        items.append(li)
    return template.section("certs", "Certifications", template.certs(items))


def render_langs(v):
    return template.section("langs", "Languages", template.paragraph("langs", esc(content.LANGUAGES)))


def render_certs_langs(v):
    """One-page variant: certifications and languages share one paragraph."""
    details = {name: detail for name, detail, _ in content.CERTS if name}
    inner = (
        f"<strong>eJPTv2</strong>: {esc(details['eJPTv2'])} · "
        f"<strong>PCEP</strong>: {esc(details['PCEP'])}<br>"
        f"{esc(content.LANGUAGES)}"
    )
    return template.section("certs", "Certifications & Languages", template.paragraph("langs", inner))


RENDERERS = {
    "summary": render_summary,
    "experience": render_experience,
    "security": render_security,
    "projects": render_projects,
    "skills": render_skills,
    "education": render_education,
    "certs": render_certs,
    "langs": render_langs,
    "certs_langs": render_certs_langs,
}


def render(v):
    sections = "".join(RENDERERS[key](v) for key in v["sections"])
    return template.page(v, sections)


# ----- pdf ---------------------------------------------------------------------

def print_pdf(html_path, pdf_path):
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        "--virtual-time-budget=8000", f"--print-to-pdf={pdf_path}", f"file://{html_path}",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def page_count(pdf_path):
    out = subprocess.run([PDFINFO, pdf_path], check=True, capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split()[1])
    raise RuntimeError(f"pdfinfo gave no page count for {pdf_path}")


# ----- main --------------------------------------------------------------------

def main(argv):
    no_pdf = "--no-pdf" in argv
    total = len(variants.VARIANTS)
    ok = 0
    for v in variants.VARIANTS:
        html_path = os.path.join(OUT, v["file"] + ".html")
        pdf_path = os.path.join(OUT, v["file"] + ".pdf")
        with open(html_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render(v))
        if no_pdf:
            print(f"{v['id']}: html written")
            ok += 1
            continue
        print_pdf(html_path, pdf_path)
        n = page_count(pdf_path)
        want = v["pages"]
        mark = "" if n == want else f"  (expected {want})"
        print(f"{v['id']}: {n} page(s){mark}")
        if n == want:
            ok += 1
    if ok == total:
        print(f"{'HTML' if no_pdf else 'BUILD'} OK {ok}/{total}")
        return 0
    print("BUILD FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
