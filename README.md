# Bill Sun Personal Website

Minimal static personal website for Bill Sun / Qingyun Sun.

## Preview

```bash
cd /Users/qingyunsun/Library/CloudStorage/Dropbox/Code/Bilsun_personal_website
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Tests

```bash
python3 -m unittest discover -s tests
python3 scripts/measure_site_size.py
```

## Notes

- Pure static HTML/CSS/JS.
- No build step.
- Structured as a single-page identity site rather than an academic CV archive.
- The live site uses `assets/qingyun-sun-portrait-1280.jpg`.
- The original source portrait is kept under `assets/source/` for future edits.
