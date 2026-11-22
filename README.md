# Home Down-Payment Portfolio

OpenAI Codex assisted with implementation, financial checks, testing, and drafting. Andrew Pienkos is responsible for reviewing and owning the analysis and decision. Education, not investment advice.

**Committee decision for the October 20, 2026 research snapshot: reject live allocation through this process (0%).** The Lab 13 client is a 25-year-old professional investing $50,000 for a first home within five years, targeting 4–5% net annually. The app shows which portfolios satisfy the modeled rules, which operational checks remain open, and how sensitive the decision is to assumptions.

## Run on Windows

The local working copy has the two exact inputs. A new clone needs the authorized October 20 adjusted closes and September 30 ALFRED archive. Set the first path below to your authorized source copy. Use the fingerprints in `data/SHA256SUMS`; verify.py checks normalized line endings and exact contents. See the [data card](docs/data-card.md) for original sources and sharing limits.

```powershell
$source = Read-Host 'Path to the authorized frozen input folder'
Copy-Item -LiteralPath "$source\prices.csv","$source\BAA_2026-09-30.csv" -Destination .\data
```

Use standard 64-bit Python 3.13. From the repository root in PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

Open http://127.0.0.1:8501. For an offline calculation or regression check:

```powershell
.\.venv\Scripts\python.exe engine.py --base
.\.venv\Scripts\python.exe verify.py
```

## How to read the decision

Compare equal weight, inverse volatility, the BIL policy benchmark and the minimum-volatility feasible mix. Expand **Mandate rules and implementation gates** to distinguish modeled passes from checks that would have to clear before any trade. Sidebar controls stress the window, cost, equity-return estimate, reserve and purchase horizon. The 4% hurdle is the low end of the client's target. Allocation stops if evidence is missing or no allocation clears the modeled gates.

`app.py` renders the decision. `engine.py` admits frozen inputs and applies the mandate across 1,771 allocation combinations. `portfolio.py` supplies return and covariance arithmetic. `verify.py` validates the pipeline and app. No account, network connection, or API key is needed at runtime after setup.

- [Committee memo](docs/decision-memo.md) and [frozen output](docs/visible-output.json)
- [Source and timing ledger](docs/data-card.md), [validation and AI use](docs/validation-and-ai-use.md), and [requirements audit](docs/requirements-audit.md)
- [Submission manifest](docs/submission-manifest.csv) and [recording scripts](docs/video-scripts.md)

The research estimates are in-sample. Annualized volatility measures dispersion. It cannot guarantee the cash available on a purchase date. Fund look-through and liquidation-to-withdrawal timing require separate evidence.
