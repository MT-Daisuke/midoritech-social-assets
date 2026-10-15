# SharePoint image import setup

The workflow uses GitHub Actions OIDC with Microsoft Entra; no PAT or client secret is required.

1. Identify an approved existing Entra application with Microsoft Graph read access to the approved SharePoint image folder.
2. Add a federated identity credential for the actual OIDC subject issued to this repository on main. Check any custom subject template before configuring. Audience: `api://AzureADTokenExchange`.
3. In this repository, configure Actions variables `AZURE_CLIENT_ID` and `AZURE_TENANT_ID` using the approved application identifiers.
4. Verify least-privilege Graph access to the four approved SharePoint images; do not grant tenant-wide read access solely for this workflow.
5. Enable Actions and allow the workflow token to write repository contents, subject to branch protections.
6. Run `Import approved SharePoint Instagram assets` with batch `2026-10-launch`.
7. Verify four PNGs under `instagram/2026/2026-10-launch/`, public GitHub Pages image responses, and Metricool media ingestion.

No credentials should be pasted into issues, code, or workflow logs. Import has not yet been verified end-to-end.
