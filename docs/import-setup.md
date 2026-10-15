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
**Manifest-driven batch import is now implemented.** Create and review `manifests/YYYY-MM-slug.json` with `schema_version: 1`, `approved: true`, the approved SharePoint `drive_id`, `batch`, `destination: instagram/YYYY/YYYY-MM-slug`, and ordered `images` entries (`filename`, `item_id`, `dimensions`, optional `sha256`). Select that batch name in the manual Actions workflow input. The importer validates names, dimensions, PNG signatures, optional hashes, and refuses changed overwrites. **Only the original batch has production success evidence; the generalized path has not yet been tested on a new approved batch.** Never repurpose an existing public path.

See [publishing SOP](instagram-publishing-sop.md) and [first publication record](instagram-launch-2026-10-15.md).
