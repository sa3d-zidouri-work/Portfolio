"""Single source of truth for every fact on the five CVs.

Edit here, then run `python3 cv/src/build.py`. The site (index.html) is
hand-written and bilingual, but `check.py parity` asserts that every role,
period, bullet and figure below appears there verbatim, so the site can
never drift from the CVs.

Style rules (enforced by check.py): no em dashes; en dash only inside
ranges; bullets in "accomplished X, measured by Y, by doing Z" shape; no
commit counts; no taglines.
"""

CONTACT = {
    "name": "Saad Zidouri",
    "phone": "+966 55 871 8087",
    "phone_href": "tel:+966558718087",
    "email": "saad.zidoori@gmail.com",
    "linkedin": "linkedin.com/in/saad-zidouri",
    "github": "github.com/sa3d-zidouri-work",
    "location": "Khobar / Dhahran, Saudi Arabia",
    "site": "https://portfolio-production-5c1c.up.railway.app/",
}

# ---------------------------------------------------------------------------
# Roles. Bullets are (tags, text). Tags: "dev" = software/mobile variants,
# "sec" = security variants, "all" = both. Variants take the first N bullets
# that match their tag filter, so order bullets by priority within each role.
# ---------------------------------------------------------------------------

ROLES = {
    "sysdev": {
        "title": "System Developer",
        "org": "H. M. Al Rugaib & Sons Trading Co.",
        "loc": "Khobar · Part-time",
        "period": "May 2026 – Present",
        "bullets": [
            ("all", "Built a quotations module that writes directly into Microsoft Dynamics 365 production and produces VAT-correct bilingual PDFs with product photos."),
            ("all", "Took the Tabby buy-now-pay-later gateway from sandbox to production in Dynamics 365 by owning the integration end to end with Tabby's team."),
            ("all", "Kept showroom price tags printing at true physical size by recalibrating the 4-up template across the render templates, server, printers admin page and desktop print agent of the price-tag pipeline, continued from an existing base."),
            ("all", "Caught payment defects before release by running full ERP payment flows and filing prioritized issue reports."),
        ],
    },
    "freelance": {
        "title": "Freelance Software Engineer",
        "org": "Independent client work",
        "org_note": "taking inherited apps through to store submission",
        "loc": "Remote",
        "period": "Mar 2026 – Present",
        "engagement": "Journey Joy (rebranded Rifqah for the 2.x release), campus ride-hailing platform: Node/Express + MySQL backend, React admin panel, Flutter driver and passenger apps · Jul 2026 – Present",
        "bullets": [
            ("all", "Took the platform from an inherited English-only, partly integrated codebase (v1.x apps already on the App Store and Google Play) to a 2.x release candidate now with the owner's team for store submission, with the backend and admin panel changes below already in production."),
            ("sec", "Removed four vulnerabilities from the platform: a MASTER_OTP login backdoor that let one universal code sign in to any account, two broken-object-level-authorization (IDOR) flaws and an unauthenticated path traversal."),
            ("dev", "Hardened the inherited Paymob card integration and made it reconcile: charging the booking actually being paid for, a saved-card toggle, subscription cancellation and renewal, and refund reconciliation through the gateway's transaction inquiry, with the server side prepared for Apple Pay behind config."),
            ("dev", "Made the platform usable by Arabic-speaking passengers and drivers by localizing all three surfaces (driver, passenger, admin) with RTL layout, Arabic typography and Arabic district names generated from the platform's live district list."),
            ("sec", "Purged 43 customers' personal data from git history with a verified rewrite, then added per-IP and per-account rate limiting, HMAC verification on Paymob callbacks, presigned S3 reads and a pre-commit secret scanner."),
            ("dev", "Made production deploys repeatable on the existing AWS EC2, RDS and S3 stack with a deploy script, drift check and schema preflight, and wrote the credential-rotation runbook after diagnosing two rotations that never reached the server."),
            ("dev", "Took the backend from no test runner to 2,363 passing mocha tests and added a weekly dependency-audit workflow that fails on High or Critical advisories."),
        ],
    },
    "intern": {
        "title": "System Developer Intern",
        "org": "H. M. Al Rugaib & Sons Trading Co.",
        "loc": "Khobar",
        "period": "Jan – May 2026",
        "bullets": [
            ("all", "Cut catalog load time from 10–15 s to under 3 s on a 160,000-item catalog by tuning queries, adding caching and moving heavy work to scheduled jobs."),
            ("all", "After testing showed regular staff could open manager-only screens, closed them by designing role-based access control mapped to the company hierarchy."),
            ("all", "Grew the internal app from a single SKU-lookup screen into a superapp used daily by 300+ staff across 15 branches by shipping the orders and analytics screens, the bonus-reconciliation cron and the BOM/kit endpoint."),
            ("all", "Kept app and ERP records in agreement by owning Dynamics 365 sandbox/UAT testing and reconciling every payment method before each release."),
        ],
    },
    "club": {
        "title": "Logistics & Operations Team Lead",
        "org": "KFUPM Cybersecurity Club",
        "loc": "Dhahran",
        "period": "Sep 2025 – Present",
        "bullets": [
            ("all", "Kept the club's workshops, competitions and events on schedule by running their logistics and automating routine tasks with Python."),
        ],
    },
    "lab": {
        "title": "Lab Assistant",
        "org": "KFUPM College of Computing & Mathematics",
        "loc": "Dhahran",
        "period": "Jan – Aug 2025",
        "bullets": [
            ("all", "Cut manual scheduling errors by 40% with a Python/Tkinter room scheduler that detects conflicts; cut a 2-hour feedback-delivery task to 15 minutes with a Power Automate and Excel workflow."),
        ],
    },
}

# Order roles appear in (newest start date first). Same order on the site.
ROLE_ORDER = ["sysdev", "freelance", "intern", "club", "lab"]

# ---------------------------------------------------------------------------
# Security record (pentest, appsec and merged variants; site Security section)
# ---------------------------------------------------------------------------

SECURITY = {
    "bounty": {
        "title": "Bug Bounty Hunter (independent)",
        "org": "HackerOne · Bugcrowd · BugBounty.sa",
        "loc": "Remote",
        "period": "2025 – 2026",
        "bullets": [
            ("sec", "Tested public programs on HackerOne, Bugcrowd and BugBounty.sa after training on INE eWPTX labs (authentication and SSO attacks; advanced web application pentesting), PortSwigger Web Security Academy, Hack The Box and TryHackMe."),
            ("sec", "Worked each program from scope review through reconnaissance and testing against the OWASP Web Security Testing Guide checklist to a write-up mapped to WSTG test IDs."),
            ("sec", "Automated the repetitive half of reconnaissance with a personal Python and Bash toolkit: a subdomain enumeration pipeline, endpoint and JavaScript discovery, scheduled asset-change monitoring, and report templating mapped to the OWASP WSTG."),
        ],
    },
}

# ---------------------------------------------------------------------------
# Projects. "variants" lists which CVs show the entry; "text" may differ per
# audience via the optional "text_sec" key.
# ---------------------------------------------------------------------------

STORE_LINKS = {
    "ios_passenger": "https://apps.apple.com/sa/app/journey-joy/id6747132253",
    "ios_driver": "https://apps.apple.com/sa/app/journey-joy-partner/id6747132364",
    "play_passenger": "https://play.google.com/store/apps/details?id=app.journeyjoy.student",
}

PROJECTS = {
    "jj": {
        "title": "Journey Joy",
        "tag": "Ride-hailing · Production",
        "tag_sec": "Ride-hailing · Security",
        "variants": ["merged", "pentest", "appsec", "software"],
        "text": "Node/Express + MySQL backend, React admin panel, Flutter driver and passenger apps; the v1.x apps are on the App Store and Google Play and my 2.x work is in the release candidate. Added since inheriting it: per-driver zone polygons on Google Maps with point-in-polygon matching, an SOS panic button with operator contacts, and 1:1 chat with report and block.",
        "text_merged": "The v1.x apps are on the App Store and Google Play; my 2.x work is in the release candidate. Added since inheriting the English-only codebase: Arabic and RTL across all three surfaces, per-driver zone polygons on Google Maps with point-in-polygon matching, SOS panic button and 1:1 chat, repeatable AWS deploys, a 2,363-test mocha suite, and a security pass that also purged 43 customers' personal data from git history.",
        "text_sec": "Authorized security work on a production ride-hailing platform (Node/Express, React, Flutter) whose code I also maintain: the backdoor, IDOR and path-traversal fixes and the hardening are itemized under Freelance Software Engineer, and every fix is deployed to the production backend.",
    },
    "rugaib": {
        "title": "Al Rugaib Sales Platform",
        "tag": "Mobile · Production",
        "variants": ["merged", "pentest", "appsec", "software"],
        "text": "Flutter/Dart superapp for H. M. Al Rugaib & Sons: orders, catalog, quotations written into Dynamics 365, analytics, bonus tracking, and role-based access mapped to the company hierarchy.",
    },
    "peregrine": {
        "title": "Peregrine",
        "tag": "AI job-search SaaS · Solo",
        "variants": ["merged", "appsec"],
        "text": "Pre-launch SaaS that parses a CV into a profile, scores roles against it and runs recruiter outreach behind a CAN-SPAM, CASL and GDPR compliance gate re-checked at send time. TypeScript monorepo (Next.js 15, Supabase Postgres): 21 tables, all under row-level security (57 policies); strict CSP with a per-request nonce; magic-byte upload validation; an SSRF-guarded fetcher; 467 unit tests.",
    },
    "ctf": {
        "title": "KFUPM CTF, 3rd place",
        "tag": "Security · Team lead",
        "variants": ["merged", "pentest", "appsec", "software"],
        "text": "Led the team through the web and network exploitation challenges with Wireshark, Metasploit and Nmap.",
    },
    "ml": {
        "title": "ML & Data Science",
        "tag": "Coursework · KFUPM",
        "variants": ["software"],
        "text": "Vehicle classification with KNN, SVM and MLP over 19 features; heart-disease prediction classifier.",
    },
}

# ---------------------------------------------------------------------------
# Skills rows (dt, dd). Variants pick rows by key and order.
# ---------------------------------------------------------------------------

SKILLS = {
    "security": ("Security", "Web penetration testing, bug bounty reconnaissance, vulnerability assessment, OWASP Top 10 and WSTG, secure code review, RBAC · Burp Suite, OWASP ZAP, Nmap, Metasploit, ffuf, sqlmap, subfinder, amass, httpx, nuclei, Wireshark, Scapy, Kali Linux"),
    "security_short": ("Security", "OWASP Top 10, RBAC, vulnerability assessment · Burp Suite, Nmap, Wireshark (eJPTv2 certified)"),
    "mobile": ("Mobile / Dev", "Flutter, Dart, Riverpod, REST APIs, Supabase, Node/Express, MySQL, Google Play and App Store release preparation"),
    "languages": ("Languages", "Python (PCEP), Bash, Dart, TypeScript/JavaScript, Java, C"),
    "systems": ("Systems", "Microsoft Dynamics 365, AWS (EC2, RDS, S3), Postman, Power Automate, Git/GitHub, Railway, Vercel, Linux"),
}

CERTS = [
    ("eJPTv2", "INE Junior Penetration Tester, earned Jan 2025", "https://certs.ine.com/e5c12a68-a072-4847-8db0-08cc06f696ee"),
    ("eWPTX", "INE Web Application Penetration Tester eXtreme, in progress", None),
    ("PCEP", "Certified Entry-Level Python Programmer", None),
    (None, "CompTIA Security+, Network+, A+ and Cisco CCNA: coursework complete, exams pending", None),
]

EDUCATION = {
    "degree": "B.S. Computer Engineering",
    "period": "Expected December 2026",
    "school": "King Fahd University of Petroleum & Minerals (KFUPM), Dhahran",
    "gpa": "GPA 3.27 / 4.00 · Second Honors",
    "rank": "QS World University Rankings 2026: #63 worldwide, 1st in the Arab region",
    "coursework_sec": "Computer & Network Security · Operating Systems · Mobile Computing & OS · Data Structures & Algorithms",
    "coursework_dev": "Mobile Computing & OS · Data Structures & Algorithms · Intro to AI (A+) · Embedded Systems",
}

LANGUAGES = "Arabic (native) · English (full professional, IELTS 6.5) · French & Japanese (elementary)"

SUMMARIES = {
    "merged": "Computer Engineering senior at KFUPM, graduating December 2026, open to software engineering and security roles. Production Flutter and full-stack work at Al Rugaib and for a freelance ride-hailing client, and security testing of that same code: eJPTv2 certified, with bug-bounty work on HackerOne, Bugcrowd and BugBounty.sa.",
    "pentest": "eJPTv2 certified (INE, Jan 2025), eWPTX in progress. Web application testing is the focus: WSTG-mapped write-ups on public bug-bounty programs, a security pass on a production ride-hailing platform whose code I also maintain, and a KFUPM CTF team lead. Computer Engineering senior at KFUPM, graduating December 2026, seeking a penetration testing or security analyst role.",
    "appsec": "Security work done from the developer's seat: RBAC design in an ERP-backed Flutter app, a security pass on a production Node/Express platform I also maintain, and a Supabase schema with row-level security on every table. eJPTv2 certified (INE, Jan 2025), eWPTX in progress. Computer Engineering senior at KFUPM, graduating December 2026, seeking an application security or secure-development role.",
    "software": "Flutter and Node/Express engineer with two production codebases in daily use: an ERP-backed sales superapp at Al Rugaib (intern, now part-time developer) and a freelance ride-hailing platform whose apps are on the App Store and Google Play. Takes work through to release: payment-gateway integration, deploy scripts, a mocha test suite and the store-submission handover. Computer Engineering senior at KFUPM, graduating December 2026.",
    "software-1page": "Flutter developer with two production codebases in daily use: an ERP-backed sales superapp at Al Rugaib and a freelance ride-hailing platform whose apps are on the App Store and Google Play. Computer Engineering senior at KFUPM, graduating December 2026.",
}

# Figures that must read identically on the site and on the CVs.
FIGURES = [
    "300+ staff across 15 branches",
    "160,000-item catalog",
    "10–15 s to under 3 s",
    "43 customers' personal data",
    "2,363",
    "GPA 3.27",
    "#63 worldwide",
    "eJPTv2",
    "3rd place",
    "Jan 2025",
]
