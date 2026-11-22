# Personal website

This repository contains the static website and the PDF copies linked from its
notes page. Editing a document in `Latex_docs` does **not** automatically change
the PDF in this repository or the published website.

## Update the notes

1. Save and compile the edited LaTeX document in your usual editor. The website
   needs the updated **PDF**; saving a `.tex` file alone is not enough.
2. From this repository, refresh the website copies:

   ```sh
   python3 scripts/sync_notes.py
   ```

3. Review and publish the changes through Git:

   ```sh
   git status --short
   git diff -- misc/index.html
   git add files/notes misc/index.html scripts/sync_notes.py README.md
   git commit -m "Update website notes"
   git push origin main
   ```

   GitHub Pages must finish deploying the pushed commit before visitors see the
   new PDFs. If an already-open PDF still shows the old version, reload it after
   deployment.

The sync command reads from `~/Documents/Latex_docs`. It copies only the five
PDFs listed below, leaves the original documents untouched, and does not compile,
commit, push or run in the background.

| Local PDF, relative to `Latex_docs` | Website copy in `files/notes` |
| --- | --- |
| `MAT495/Notes/main.pdf` | `random-matrix-products.pdf` |
| `MAT436/Homework/Paper1.pdf` | `pontryagin-duality.pdf` |
| `research/paper reading/PSW.pdf` | `psw.pdf` |
| `MAT495/On research /notes.pdf` | `limit-sets-and-flag-varieties.pdf` |
| `MAT464/notes.pdf` | `mat464.pdf` |

The existing folder name `On research ` has a trailing space; the script preserves
it. If you move `Latex_docs`, pass its new location:

```sh
python3 scripts/sync_notes.py --source-root "/path/to/Latex_docs"
```

To check whether the website PDFs match the compiled local PDFs without copying:

```sh
python3 scripts/sync_notes.py --check
```

This checks PDF contents, not whether the PDFs have been recompiled after a LaTeX
edit. To add a different document later, add its source/destination pair to
`NOTES` in the script and a link in `misc/index.html`.
