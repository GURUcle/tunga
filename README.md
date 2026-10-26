# Tunga

A working prototype of a property crowdfunding platform for Namibia, built against the
**NAMFISA Regulatory Sandbox Crowdfunding Guidelines** (effective 28 November 2025).

> **This is a prototype.** No real money moves. No real securities are offered. Every
> issuer, investor, property and figure in it is illustrative. Tunga is not licensed by
> NAMFISA and nothing here is investment advice.

---

## Why it exists

The Cardone Capital model — pooled blind-pool funds, large raises, the operator holding
investor cash, promised distributions — cannot be operated in Namibia. Three rules stop it:

| Constraint | Rule | Effect |
|---|---|---|
| Issuer cap | s10(3) | Max N$10m per issuer per 12 months. No pooled multi-asset fund. One SPV per building. |
| Custody | s28(1)(b), s43 | The operator may never hold investor funds. A licensed bank custodian holds a segregated trust account per round. |
| Conduct | s28(1)(a),(c) | No investment advice, no promised returns, no guaranteed outcomes. |

What does work is the fractional-ownership structure: one company per property, shares sold
to retail, rent paid as dividends, a 5–7 year hold, an internal market for secondary trades.

## What it demonstrates

**Investor**

- Offering pages with full Annexure 1 disclosure across seven tabs, including a
  **Costs & fees** tab that discloses every charge, who receives it, and a worked example
  of the total cost on a N$50,000 subscription
- Subscription flow that hard-blocks on the s11 annual cap, the offering minimum, and the
  remaining target
- Four mandatory risk acknowledgements (s35) before a subscription is accepted
- 48-hour cooling-off with a live countdown and a working cancel (s22)
- Portfolio showing distributions received, value change and total return since inception

**Issuer**

- Round stepper with every statutory step and its deadline
- Annexure 1 completeness checklist that gates publication
- Ongoing obligations: quarterly updates, audited financials within 90 days, AGM
- Quarterly update composer that publishes to the offering page

**Regulator console**

- 90-day review clock per issuer (s37)
- Statutory deadline board computed from live timestamps
- Investor concentration monitor against each category's annual limit
- Filings log with overdue items flagged
- Quarterly return export (s47) as JSON, plus a CSV investor register

**Rulebook** — 14 guideline sections mapped to where each one is enforced in the software.

## Running it

No build step, no dependencies. It is one HTML file.

```bash
python3 -m http.server 8787
# open http://127.0.0.1:8787
```

Or just open `index.html` in a browser.

State lives in `localStorage` under the key `tunga.v2`. If the demo ever looks stale or
empty, use **Reset demo data** in the top right of the portfolio page.

## Structure

```
index.html          the entire application — markup, styles and logic
images/             property photography (illustrative, AI-generated)
images/originals/   full-resolution sources, excluded from the repo
```

## Compliance map

| Section | Obligation | Where it lives |
|---|---|---|
| s10(3) | N$10m issuer cap | Enforced at offering creation |
| s11 | Investor annual limits | Hard block in subscription step 1 |
| s13 | Offering document, 48h filing, 14-day pre-publication | Filing log and review clock |
| s15 | 60-day round | Countdown on every offering |
| s17–19 | Oversubscription, refunds, operator liability | Refund workflow |
| s21 | Funds released within 5 business days | Settlement step |
| s22 | 48-hour cooling-off | Portfolio cancel button |
| s28 | Operator prohibitions | Architecture — custodian holds cash |
| s35 | Risk acknowledgements | Subscription step 2 |
| s37 | 90-day review decision | Review queue clock |
| s42 | Post-offer inspection | Deadline board |
| s46 | 7-year records | Audit log |
| s47 | Quarterly reporting | Export function |

## Not built yet

This is a demonstrator, not a product. Still missing before it could take a single real dollar:

- Server-side storage, authentication and role-based permissions
- KYC / AML — identity verification, sanctions and PEP screening
- Payment rails and custodian bank API integration, with daily reconciliation
- Authoritative share registry and cap table
- Subscription agreements and e-signatures
- Secondary trading facility (s30)
- Tamper-evident audit trail with 7-year retention
- Hosting, backups, monitoring, penetration testing

The regulatory track runs in parallel and gates everything: sandbox admission, a custodian
agreement with a Bank of Namibia-licensed bank, fit-and-proper packs, platform rules and a
conflict-of-interest policy.

## Disclaimer

Prototype only. Illustrative data. Capital at risk. Not an offer of securities. Not licensed
by NAMFISA. Nothing on the site is investment advice.
