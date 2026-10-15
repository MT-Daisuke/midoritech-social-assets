# SharePoint image import setup — verified 2026-10-15

## Implemented configuration
- GitHub Actions workflow: `.github/workflows/import-sharepoint-images.yml`; Python: `scripts/import_sharepoint_images.py`.
- Microsoft Entra existing application: `midoritech-wordpress-automation`.
- OIDC federated credential: `github-social-assets`, branch `main`, subject with organization and repository IDs.
- GitHub Actions repository variables: `AZURE_CLIENT_ID` and `AZURE_TENANT_ID`. Identifiers are not secrets. No PAT or client secret was created.
- GitHub Actions `GITHUB_TOKEN` writes approved files to `main`; Microsoft Graph access token is obtained transiently using OIDC.
- Successful first run: https://github.com/MT-Daisuke/midoritech-social-assets/actions/runs/38698950158 .
- Source: approved SharePoint batch. Target: `instagram/2026/2026-10-launch/` (four 1080×1350 PNGs).

## When onboarding a new repository
1. Verify the approved Entra app and least-privilege SharePoint Graph read access.
2. Create a branch-scoped federated credential matching the **actual** GitHub OIDC subject template (some accounts use repository/owner numeric IDs), issuer and audience.
3. Set repository Actions variables `AZURE_CLIENT_ID` and `AZURE_TENANT_ID`.
4. Ensure `contents: write`, `id-token: write` and branch rules permit the workflow bot.
5. Run the manual import and inspect logs. Do not place tokens in code, logs or issue comments.
6. Verify actual public image access and approved media before scheduling in Metricool.

## When onboarding a new post batch
The current Python importer and workflow input are **fixed to the first four approved images**. Before any new publication, add the new approved SharePoint item IDs, new destination directory and reviewed workflow input. Never replace the first batch's public URLs or source IDs with a different campaign. A generalized manifest-based importer is a future enhancement, not an implemented capability.

See [publishing SOP](instagram-publishing-sop.md) and [first publication record](instagram-launch-2026-10-15.md).
