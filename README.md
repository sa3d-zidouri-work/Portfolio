# Portfolio

Source of the portfolio site and the CV pages it links to.

## CVs

The five CV pages in cv/*.html and their PDFs in cv/*.pdf are generated files. Do not edit them by hand. Every fact on them lives in cv/src/content.py, and what each variant shows, in which order and how many bullets per role, lives in cv/src/variants.py. After editing either file, rebuild with:

    PYTHONDONTWRITEBYTECODE=1 python3 cv/src/build.py

The build writes the HTML, prints each PDF with headless Chrome, measures the page counts with pdfinfo and ends with "BUILD OK 5/5" when every count matches the variant's target. Pass --no-pdf to write the HTML only.

The site is hand written, so a checker keeps it in step with the CV source:

    python3 cv/src/check.py <subcommand>

Subcommands: pages (PDF page counts), dashes (no em dash in prose), slop (no phrase from the slop list), ranges (en dashes only inside date or number ranges), parity (every role, period and shared figure appears verbatim on the site and the CVs), commits (the prose never quantifies git history), hub (the hub lists five CVs and their files exist), required (new content present, retired content absent), bilingual (every English span in the site's Experience, Security, Skills and Contact sections has an Arabic sibling), serve (cv/src is hidden by the Caddyfile and bytecode is ignored by git), selftest (the checker fails on known positive fixtures) and live (the deployed site serves the new content).
