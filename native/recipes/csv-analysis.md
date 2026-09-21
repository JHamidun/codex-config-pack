# Analyze CSV data in Codex

Identify the supplied CSV and the question. Establish row grain, key columns,
dimensions and metrics before calculating aggregates. Never treat numeric IDs,
postal codes or category codes as quantities merely because they contain digits.

Start with the included standard-library profiler; no pandas installation is needed:

```text
python "${CODEX_PACK_ROOT}/scripts/runtime.py" csv-profile "<input.csv>"
python "${CODEX_PACK_ROOT}/scripts/runtime.py" csv-profile "<input.csv>" --key "entity_id" --numeric "amount"
```

Repeat `--key` for composite keys and `--numeric` for explicit metrics. UTF-8/BOM
and comma, semicolon, tab or pipe separators are supported; `--delimiter` removes
ambiguity. The helper returns row counts, missing cells, distinct counts, extra
duplicate-key rows, and numeric valid/invalid counts plus sum/min/max/mean.
Numeric aggregates cover only valid finite cells; disclose missing or invalid
data rather than presenting these as whole-population estimates.

For statistical inference and charts, read the methodology reference at
`${CODEX_PACK_ROOT}/library/skills/csv-analysis/references/stats-methodology.md`
when it is relevant. Use the actual data and an available calculation environment;
test calculations against small known examples. Install an additional package only
when the requested analysis needs it and installation is authorized. The profiler
does not itself implement hypothesis testing, causal inference or visualization.

Input is limited to 20 MB and 100,000 rows. Larger or non-UTF-8 files require an
explicit conversion/streaming approach, not silent truncation. Do not modify the
input, execute spreadsheet formulas or upload data to a third party.
