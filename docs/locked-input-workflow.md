# Locked Changed-Input Record workflow

Student action. Close generative AI before choosing the input or writing the prediction. In the validation record, write one material input, its exact old and new values and units, the finance mechanism, the expected output direction and magnitude if defensible, the expected modeled and committee decision effects, and a timestamp with time zone. Record the baseline source commit. Commit the prediction and verify that the immutable commit is visible on GitHub **before running the experiment**. Preserve the URL. Local commits alone do not meet the published requirement.

With AI still closed and all other assumptions held fixed, capture the baseline and the single-input run from the locked revision. Replace FIELD and VALUE with your own locked setting. Use the Python environment set up in the README.

```powershell
.\.venv\Scripts\python.exe engine.py --base | Out-File -Encoding utf8 docs/locked-before.json
.\.venv\Scripts\python.exe engine.py --set-input FIELD VALUE | Out-File -Encoding utf8 docs/locked-after.json
```

Supported settings are `months` (whole monthly returns), `cost_bps` (annual basis points), `equity_shock_pp` (signed percentage points), `reserve_pct` (whole percent), and `years_remaining` (whole years). Check both command exit codes before interpreting output. Confirm that the two `inputs` objects differ in exactly one field. Preserve the files, record the actual modeled and committee decision effects, and explain any unexpected result or unchanged action. Keep the original prediction commit intact.
