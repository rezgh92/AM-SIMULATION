#!/bin/sh
# Build the manuscript PDFs: journal-style two-column (main) and double-spaced review copy.
set -e
cd "$(dirname "$0")"
cat refs_context.bib refs_materials.bib refs_extra.bib 2>/dev/null > refs.bib
for doc in main review; do
  pdflatex -interaction=nonstopmode -halt-on-error $doc.tex > /dev/null
  bibtex $doc > /dev/null || true
  pdflatex -interaction=nonstopmode -halt-on-error $doc.tex > /dev/null
  pdflatex -interaction=nonstopmode -halt-on-error $doc.tex > /dev/null
done
grep -E "undefined|Warning.*Citation" main.log | sort -u | head -20 || true
