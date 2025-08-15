Power BI Starter Pack — Insurance Claims

Files included:
- clean_claims.csv — the dataset (use this in Power BI: Get Data > Text/CSV)
- summary.xlsx — validation KPIs and pivots (optional)
- dax_measures.txt — copy/paste measures into Power BI Desktop
- theme.json — import as a custom theme (View > Themes > Browse for themes)

Recommended visuals to build in Power BI (takes ~5 minutes):

1) KPI Cards (3 cards)
   - Total Claims = [Total Claims]
   - Approval Rate = [Approval Rate]
   - Fraud Rate = [Fraud Rate]

2) Column Chart — Claim Counts by Region
   - Axis: Region
   - Values: ClaimID (Count)

3) Column Chart — Average Claim Amount by Claim Type
   - Axis: ClaimType
   - Values: ClaimAmount (Average)

4) Line Chart — Monthly Claim Volume
   - Axis: YearMonth (from column) or a Date hierarchy on ClaimDate
   - Values: ClaimID (Count)

5) Table — Agent Performance
   - Columns: AgentID, ClaimID (Count), [Approved Claims], [Approval Rate]

Slicer Filters:
- Region
- ClaimType
- YearMonth (or ClaimDate)

Build Steps:
1. Open Power BI Desktop.
2. Get Data > Text/CSV > select clean_claims.csv.
3. Load.
4. Modeling > New Measure > paste all measures from dax_measures.txt.
5. View > Themes > Browse for themes > select theme.json.
6. Build the visuals as listed above.
7. Save as: Insurance_Claims_Dashboard.pbix

Validation (compare to summary.xlsx KPIs):
- Total Claims should be 600.
- Approval Rate ≈ 67.17%.
- Fraud Rate ≈ 13.17%.
- Avg Settlement Days (approved only) ≈ 19.2.
