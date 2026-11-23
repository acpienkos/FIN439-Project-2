# Validation and AI use

Snapshot October 20, 2026. Source dates, use limits, and archive gates are in the [data card](data-card.md). The app uses the same engine as the [frozen output](visible-output.json). See the [README](../README.md) for setup and the [execution log](project2-test-results.txt) for the standalone test run.

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

Status: completed on November 23, 2026. The student executed both cases independently with AI off. See the [AI-off workflow](locked-input-workflow.md).

| Pre-run field | Student entry |
|---|---|
| Timestamp with time zone | 2026-11-22T18:19:38.9486922-05:00 |
| Baseline source commit | 6bd94fc446ffe9f8d10ad9dd358d1a4a9d91d546 |
| Exact input and old → new values with units | reserve_pct: 20% → 40% |
| Finance mechanism and expected output direction | I'm increasing the reserve requirement from 20% to 40%. Since the reserve is held in BIL, this change forces more of the portfolio into a low-risk, highly liquid asset and leaves less money available for higher-return investments like VT. Because of that, I expect the portfolio's estimated net return to decrease. I also expect volatility to decrease because a larger share of the portfolio is invested in a lower-risk asset.<br><br>I expect net return to be lower than the baseline 4.1967%, volatility to be lower than the baseline 1.6615%, and the number of qualifying portfolios to stay the same or decrease. |
| Expected modeled eligibility and committee decision effects | For someone planning to buy a home within five years, keeping more money in liquid, lower-risk investments helps protect the down payment from market swings. I think the model will still find at least one qualifying portfolio, but there may be fewer qualifying options because of the stricter reserve requirement. I expect the selected portfolio to become more conservative. I do not expect the committee recommendation to change, and I expect the authorized allocation to remain at 0% because the project documentation says the committee action stays the same until the additional operational checks are completed. |


| Post-run field | Student entry |
|---|---|
| Prediction commit permalink and pre-run verification | The [original prediction commit](https://github.com/acpienkos/FIN439-Project-2/commit/828d4ad3b9a39d28194f75dc8aafaa516fd42a84) was verified on GitHub at 2026-11-23T13:00:44.9682579-05:00, before execution. Local main matched that commit and the working tree was clean. |
| Before/after output paths and execution timestamp | I executed both cases independently in PowerShell using Python with AI off. The run started at 2026-11-23T13:02:06.2125594-05:00 and finished at 2026-11-23T13:02:07.7505811-05:00. The [baseline output](locked-before.json) and [changed-case output](locked-after.json) confirm that only the BIL reserve floor changed, from 20% to 40%. |
| Actual output changes and modeled eligibility | The lowest-risk qualifying portfolio remained 90% BIL, 0% IEF, 0% LQD, and 10% VT. Estimated annual net return stayed at 4.1967% and annualized volatility stayed at 1.6615%, each a change of 0 percentage points. One portfolio qualified in both runs. The selected mix passed all six modeled rules. The equal-weight portfolio held 25% BIL and newly failed the BIL reserve rule. It already failed the 4% net objective, corporate issuer bound, and volatility cap, so its overall eligibility and the qualifying count stayed the same. |
| Actual committee decision effect | The recommendation remained “Reject live allocation,” and the authorized allocation remained 0%. All four implementation gates remained open: five-business-day availability, fund holdings and derivatives policy, client purchase timing and loss tolerance, and independent holdout validation. |
| Reconciliation or diagnosis of unexpected/no change | My prediction was partially correct. I expected lower net return and volatility and a more conservative selected portfolio. The selected mix already held 90% BIL, above both reserve floors, so the higher minimum left its weights and estimates unchanged. I correctly expected at least one qualifying portfolio, a qualifying count that stayed the same or fell, and an unchanged committee recommendation and authorized allocation. Tightening a constraint can leave the chosen portfolio unchanged when its existing allocation already meets the stricter limit. |

## AI disclosure

Andrew Pienkos independently selected the changed input and developed the financial prediction with AI off. OpenAI Codex copied Andrew’s original wording into the pre-run table verbatim and published the prediction commit before execution. On November 23, Andrew ran both PowerShell cases with ChatGPT and Codex closed and independently evaluated the results before returning to AI assistance. After that evaluation, ChatGPT and Codex assisted with organizing, reviewing, documenting, and explaining the experiment. Codex checked the preserved JSON and edited the post-run record using Andrew’s findings. Both original outputs were preserved.

On November 17, 2026, OpenAI Codex assisted with course and repository review, design, implementation, automated tests, and documentation. The model version was not exposed in the work environment for this record. Codex proposed a 90/10 candidate based on the engine output. Validation recomputes its net estimate directly as 90% of the BIL estimate plus 10% of the VT estimate minus annual drag and probes the modeled 39/40 bp boundary. The checks support the modeled result for the frozen scenario. The estimate is in-sample and the operational gates remain open.


## Standalone validation, November 22, 2026

| Claim or failure mode | Test and outcome |
|---|---|
| Monthly source transformation | Rebuilt 60 aligned monthly prices per fund from the four archived Lab 14 chart JSON files; SHA-256 matched the frozen file. |
| Portfolio arithmetic | Direct weighted sample volatility from the monthly return series agrees with the engine covariance calculation at 11 decimal places. Direct weights-times-returns minus cost reproduces 4.196694% at the base. |
| Grid and benchmark | 1,771 unique fully invested grid rows. BIL alone fails the 4% net objective at the default window and cost. |
| Timing and inputs | Same-day and missing BAA archives fail. Invalid options and missing or malformed price data fail. Both frozen input hashes match. |
| Reproducibility and stability | Frozen base and engineering stresses match the regenerated JSON. Each engineering stress varies one assumption and the restored baseline is identical. |
| Clean runtime | All eight automated checks passed in a fresh temporary file tree against fresh-installed Streamlit 1.66.0 dependencies on Windows using Python 3.13.7. The loopback health endpoint returned HTTP 200 after disabling the temporary target install's development mode. This exercise used the local frozen snapshots. Partner and remote access validation remain open. |

See the [execution log](project2-test-results.txt) for first failures and retries. The research controls and regression tests validate the tool's behavior. The separate student-run locked experiment is documented above with its original outputs and reconciliation.

OpenAI Codex on November 22, 2026 assisted with the standalone implementation, evidence packaging, financial cross-checks and recording drafts. The exposed surface is Codex and a model revision was not shown. The Codex-assisted validation checked the 90/10 result in two ways. It calculated risk directly from the weighted monthly return series and compared it with the covariance-based result. It also substituted the published estimates into the net-return formula. The calculation supports a modeled pass. The committee recommendation remains qualified by in-sample data, the small net-return margin and the open implementation gates. The student's reconciliation of the locked experiment is recorded above.
