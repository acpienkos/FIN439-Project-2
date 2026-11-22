# Validation and AI use

Snapshot October 20, 2026. Source dates, use limits, and archive gates are in the [data card](data-card.md). The app uses the same engine as the [frozen output](visible-output.json). Setups and open items are in the [readiness record](lab20-readiness.md).

## Baseline and mandate check

The engine evaluates all 1,771 long-only, fully invested four-fund allocations on a five-percentage-point grid. It uses the Lab 14 weighted return, inverse volatility, covariance, and portfolio volatility functions. Annualized monthly arithmetic returns are estimates. Subtract 20 basis points of assumed incremental annual costs at the base. Adjusted closes already reflect historical fund-level expenses through fund performance. No taxes, market impact, or client-specific transaction costs are modeled explicitly.

Equal weight and inverse volatility fail the modeled mandate. The BIL-only benchmark fails the 4% net objective. The sole modeled pass at default inputs is 90% BIL and 10% VT with 4.20% estimated net return and 1.66% annualized volatility. Its 90% BIL clears the reserve gate, and 10% VT meets the conservative corporate issuer bound and the five-year equity cap. The proposed 4% annualized volatility cap applies when the known BAA observation reaches 6%. Five-day liquidity and fund-exposure checks are open, so modeled eligibility does not authorize a live allocation.

## AI-assisted sensitivity runs

| Scenario | Feasible mixes | Minimum-risk passing mix | Highest net within modeled risk limits |
|---|---:|---|---:|
| Base, 59 months, 20 bp | 1 | 90% BIL / 10% VT | 4.20% |
| VT annual estimate down 1 percentage point | 1 | 90% BIL / 10% VT | 4.10% |
| Last 36 monthly returns | 41 | 100% BIL | 5.75% |
| 50 bp annual drag | 0 | None | 3.90% |
| 40% BIL reserve floor | 1 | 90% BIL / 10% VT | 4.20% |
| One year until purchase | 0 | None | 3.83% |

The 36-month row's highest net estimate is for a different mix from the minimum-risk passing mix. The latter estimates 4.17% net. The 40% reserve stress leaves the result unchanged because the base passes with 90% BIL. At 50 bp the net estimate loses 30 bp while asset weights, means and covariance inputs stay fixed. At one year, the modeled equity cap drops to 5%, so the 90/10 portfolio is ineligible. The live decision remains reject throughout while the operational checks are open. The tested cost cutoff for modeled feasibility is 39 bp passes / 40 bp fails at integer precision.

## Locked Changed-Input Record

Status: student prediction and run pending. Follow the [AI-off workflow](locked-input-workflow.md).

| Pre-run field | Student entry |
|---|---|
| Timestamp with time zone | |
| Baseline source commit | |
| Exact input and old → new values with units | |
| Finance mechanism and expected output direction | |
| Expected modeled eligibility and committee decision effects | |

After pushing the prediction, record its immutable GitHub URL below. Keep the original commit intact.

| Post-run field | Student entry |
|---|---|
| Prediction commit permalink and pre-run verification | |
| Before/after output paths and execution timestamp | |
| Actual output changes and modeled eligibility | |
| Actual committee decision effect | |
| Reconciliation or diagnosis of unexpected/no change | |

## AI disclosure

On November 17, 2026, OpenAI Codex assisted with course and repository review, design, implementation, automated tests, and documentation. The model version was not exposed in the work environment for this record. Codex proposed a 90/10 candidate based on the engine output. Validation recomputes its net estimate directly as 90% of the BIL estimate plus 10% of the VT estimate minus annual drag and probes the modeled 39/40 bp boundary. The result is accepted for a frozen scenario and qualified for deployment because the estimate is in-sample and operational mandate gates are open. Student review and ownership evidence remain pending.


## Standalone validation, November 22, 2026

| Claim or failure mode | Test and outcome |
|---|---|
| Monthly source transformation | Rebuilt 60 aligned monthly prices per fund from the four archived Lab 14 chart JSON files; SHA-256 matched the frozen file. |
| Portfolio arithmetic | Direct weighted sample volatility from the monthly return series agrees with the engine covariance calculation at 11 decimal places. Direct weights-times-returns minus cost reproduces 4.196694% at the base. |
| Grid and benchmark | 1,771 unique fully invested grid rows. BIL alone fails the 4% net objective at the default window and cost. |
| Timing and inputs | Same-day and missing BAA archives fail. Invalid options and missing or malformed price data fail. Both frozen input hashes match. |
| Reproducibility and stability | Frozen base and engineering stresses match the regenerated JSON. Each engineering stress varies one assumption and the restored baseline is identical. |
| Clean runtime | All eight automated checks passed in a fresh temporary file tree against fresh-installed Streamlit 1.66.0 dependencies on Windows using Python 3.13.7. The loopback health endpoint returned HTTP 200 after disabling the temporary target install's development mode. This exercise used the local frozen snapshots. Partner and remote access validation remain open. |

See the [execution log](project2-test-results.txt) for first failures and retries. The research controls and regression tests validate the tool's behavior. The separate human-led locked experiment above is still pending.

OpenAI Codex on November 22, 2026 assisted with the standalone implementation, evidence packaging, financial cross-checks and recording drafts. The exposed surface is Codex and a model revision was not shown. Codex's inherited 90/10 claim was checked by independently computing risk from the weighted monthly return series rather than the covariance matrix and by substituting the published estimates into the net-return formula. The calculation supports a modeled pass. The committee recommendation remains qualified by in-sample data, the small net-return margin and the open implementation gates. Andrew's own review and judgment remain pending.
