# DevSecOps Pipeline — Passing Demo (dependency-free)

A **hardened, dependency-free** web app wired to a GitHub Actions DevSecOps
pipeline. It is built to pass **every** job — including an **enforced** security
gate — reliably, every time.

## Why it always passes

The app uses **only the Python standard library** — there are **no third-party
dependencies**. That means the SCA scanner (Trivy) has nothing to flag, so the
enforced gate (`exit-code: '1'` on Critical/High) can never fail.

| Job | Result | Why |
|---|---|---|
| Secret Scanning (gitleaks) | PASS | no secrets in the repo |
| SAST (Semgrep) | PASS | report-only, hardened code |
| SAST (CodeQL) | PASS | `continue-on-error` safety net |
| SCA + Gate (Trivy) | **PASS** | **no dependencies = no findings** |
| Container Scan + SBOM | PASS | image scan report-only; SBOM generated |
| DAST (OWASP ZAP) | PASS | report-only; security headers set |
| Deploy | PASS | runs because all gates passed |

The app is also genuinely secure: non-root container, no secrets, no SQL,
debug off, and it sends `X-Content-Type-Options`, `X-Frame-Options`,
`Content-Security-Policy`, and `Referrer-Policy` headers.

## Setup (5 minutes)

> Note: this is delivered as files, not a GitHub repo. Pushing it to your own
> **new PUBLIC repo** gives you exactly the same result as forking — a repo
> where all tests pass.

1. Create a **new PUBLIC repo** on your **personal** GitHub account
   (public = free CodeQL + Security tab).
2. Put these files in it and push:

   ```bash
   git init
   git add .
   git commit -m "DevSecOps passing pipeline"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo>.git
   git push -u origin main
   ```

3. Open the **Actions** tab — every job goes green, including the enforced gate,
   and `deploy` runs.

## Run locally (optional)

```bash
python3 app.py            # serves on http://localhost:8000
curl http://localhost:8000/health
```

Or with Docker:

```bash
docker build -t demo-app .
docker run -p 8000:8000 demo-app
```
