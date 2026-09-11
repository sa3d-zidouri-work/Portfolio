"""The five CV variants: what each one shows, in what order, and how tight.

Each variant is a dict:
  file        output basename (html + pdf)
  title       <title> and the hub name
  eyebrow     toolbar label
  subtitle    line under the name
  summary     key into content.SUMMARIES
  sections    ordered list of section keys
  roles       ordered role ids from content.ROLES
  tags        which bullet tags this variant accepts ({"all","dev"} or {"all","sec"})
  caps        per-role bullet cap, "*" is the default
  security    include the bug-bounty entry (SECURITY) in the "security" section
  projects    ordered project ids from content.PROJECTS
  project_text which project text key to prefer: "text", "text_sec" or "text_one"
  skills      ordered skills row keys
  coursework  "coursework_sec" or "coursework_dev"
  certs_style "list" (own section) or "inline" (merged with languages, one-page)
  one_page    adds body.one for the tighter print rules
  pages       expected PDF page count (checked after build)
"""

VARIANTS = [
    {
        "id": "merged",
        "file": "merged",
        "title": "Dual-Track CV",
        "eyebrow": "DUAL-TRACK",
        "subtitle": "Mobile Software Engineering · Application Security",
        "summary": "merged",
        "sections": ["summary", "experience", "security", "projects", "skills", "education", "certs", "langs"],
        "roles": ["sysdev", "freelance", "intern", "club", "lab"],
        "tags": {"all", "dev", "sec"},
        "caps": {"*": 4, "freelance": 4},
        "security": True,
        "projects": ["jj", "peregrine", "rugaib", "ctf"],
        "project_text": "text_merged",
        "skills": ["security", "mobile", "languages", "systems"],
        "coursework": "coursework_sec",
        "certs_style": "list",
        "one_page": False,
        "pages": 2,
    },
    {
        "id": "pentest",
        "file": "pentest",
        "title": "Penetration Testing CV",
        "eyebrow": "PENETRATION TESTING",
        "subtitle": "Penetration Testing · Bug Bounty · Application Security",
        "summary": "pentest",
        "sections": ["summary", "certs", "security", "projects", "experience", "skills", "education", "langs"],
        "roles": ["sysdev", "freelance", "intern", "club", "lab"],
        "tags": {"all", "sec"},
        "caps": {"*": 2, "freelance": 3, "club": 1, "lab": 1},
        "security": True,
        "projects": ["jj", "ctf", "rugaib"],
        "project_text": "text_sec",
        "skills": ["security", "languages", "mobile", "systems"],
        "coursework": "coursework_sec",
        "certs_style": "list",
        "one_page": False,
        "pages": 2,
    },
    {
        "id": "appsec",
        "file": "appsec",
        "title": "Application Security CV",
        "eyebrow": "APPLICATION SECURITY",
        "subtitle": "Application Security · Secure Development",
        "summary": "appsec",
        "sections": ["summary", "certs", "security", "projects", "experience", "skills", "education", "langs"],
        "roles": ["sysdev", "freelance", "intern", "club", "lab"],
        "tags": {"all", "sec"},
        "caps": {"*": 3, "freelance": 3, "club": 1, "lab": 1},
        "security": True,
        "projects": ["jj", "peregrine", "rugaib", "ctf"],
        "project_text": "text_sec",
        "skills": ["security", "mobile", "languages", "systems"],
        "coursework": "coursework_sec",
        "certs_style": "list",
        "one_page": False,
        "pages": 2,
    },
    {
        "id": "software",
        "file": "software",
        "title": "Software / Mobile CV",
        "eyebrow": "SOFTWARE · MOBILE",
        "subtitle": "Software Engineer · Mobile (Flutter) · Full-Stack",
        "summary": "software",
        "sections": ["summary", "experience", "projects", "skills", "education", "certs", "langs"],
        "roles": ["sysdev", "freelance", "intern", "club", "lab"],
        "tags": {"all", "dev"},
        "caps": {"*": 4, "freelance": 5},
        "security": False,
        "projects": ["rugaib", "jj", "ctf", "ml"],
        "project_text": "text",
        "skills": ["mobile", "languages", "systems", "security_short"],
        "coursework": "coursework_dev",
        "certs_style": "list",
        "one_page": False,
        "pages": 2,
    },
    {
        "id": "software-1page",
        "file": "software-1page",
        "title": "Software / Mobile CV, one page",
        "eyebrow": "SOFTWARE · MOBILE · ONE PAGE",
        "subtitle": "Software Engineer · Mobile (Flutter)",
        "summary": "software-1page",
        "sections": ["summary", "experience", "skills", "education", "certs_langs"],
        "roles": ["sysdev", "freelance", "intern", "lab"],
        "tags": {"all", "dev"},
        "caps": {"*": 2, "freelance": 2, "lab": 1},
        "security": False,
        "projects": [],
        "project_text": "text",
        "skills": ["mobile", "languages", "systems", "security_short"],
        "coursework": "coursework_dev",
        "certs_style": "inline",
        "one_page": True,
        "pages": 1,
    },
]


def bullets_for(variant, role):
    """Bullets a variant shows for a role: tag-filtered, then capped."""
    cap = variant["caps"].get(role_id_of(variant, role), variant["caps"]["*"])
    picked = [text for tags, text in role["bullets"] if tags in variant["tags"]]
    return picked[:cap]


def role_id_of(variant, role):
    from content import ROLES
    for rid, r in ROLES.items():
        if r is role:
            return rid
    raise KeyError("role not registered in content.ROLES")
