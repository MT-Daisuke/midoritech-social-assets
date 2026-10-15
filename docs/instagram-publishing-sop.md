# Instagram publishing standard operating procedure (v1.0)
Effective: 2026-10-15. Owner: Midoritech LLC. This public document contains no credentials or private draft material.

## Authority and roles
- SharePoint: authoritative approved source for assets, captions, approvals and publication ledger. Never use this public GitHub repository as the approval database.
- GitHub Actions: transfers **only approved, explicitly identified** SharePoint items through Microsoft Graph using Entra OIDC. No new GitHub PAT or client secret.
- GitHub Pages: public, durable HTTPS image URLs for Metricool ingestion. Public means no confidential or personal information.
- Metricool: corporate brand `7355568`, Instagram `@midoritech.gardening`, Asia/Tokyo. Never use the personal Metricool account.
- Instagram: final evidence of actual publication; a Metricool PENDING state is not proof of publication.

## Repeatable process
1. Create assets and caption in SharePoint; check official logo, typography, QR (if any), factual claims, copyrights, image order and crop. Record approval before publication.
2. Create a **new batch** with unique item IDs, a new `instagram/YYYY/YYYY-MM-slug/` directory and a new workflow input. Current importer is **hard-coded to 2026-10-launch only**; never rerun it for a different batch without updating and reviewing code.
3. Review the public/nonconfidential status of all assets. Import via the manually triggered GitHub Action on `main`. Preserve the OIDC branch/repository trust scope and least-privilege SharePoint access.
4. Verify a successful workflow, file count, correct ordering, PNG integrity, and actual public HTTPS access for **every** image. Confirm the exact approved image visually; a green workflow alone is insufficient.
5. Check AI disclosure decision **per post** (below), caption, destination account, carousel order, publication timezone and date. Obtain final publication authorization.
6. Schedule or update the existing Metricool post using `autoPublish=true`, `draft=false`, the four public URLs and the approved caption. Do not create duplicates; verify the scheduled post UUID and provider status.
7. After the due time, confirm the post in Instagram itself: account, images/count/order, caption, publication time and AI label. Record the Instagram permalink and any anomalies in the **private SharePoint publication ledger**. Metricool success alone is not sufficient.
8. Retain public image URLs while in use by Metricool and for audit/republication needs. Do not delete or rename files referenced by live posts. Archive the approval and verification evidence privately.

## AI disclosure decision (mandatory)
- Do **not** default `instagramData.isAiGenerated` to `true` or `false` without assessing the assets.
- If generative AI created or substantially altered realistic imagery or other content requiring disclosure under current Meta rules, disclose as required; check the platform's current requirements before posting.
- Conventional photography, cropping, color correction, typesetting, layout and AI-assisted **text drafting alone** do not automatically require labeling the visual as AI-generated.
- When the production provenance is uncertain, hold publication for review rather than silently setting `false`.
- Log: original image source; AI generation/editing tool and scope; reviewer; disclosure decision; reason; date. Check any automatic labels separately.
- Initial 2026-10-15 launch: `isAiGenerated=true` was passed to Metricool and Instagram visibly displayed `AIコンテンツ`. This is a factual publication record, **not** a blanket policy for later posts. Do not remove a justified label solely for aesthetics.

## Failure response
- OIDC failure: verify actual subject, issuer, audience, branch, Entra federation and repository variables; never paste access tokens into logs.
- Graph 403/404: verify the fixed SharePoint drive/item and approved resource-level read grant; do not grant tenant-wide access as a shortcut.
- Asset mismatch: stop, compare approved SharePoint source and GitHub bytes; do not overwrite published assets silently.
- Metricool media error: check unauthenticated public URL, MIME, image dimensions and availability; do not use temporary SharePoint signed download links.
- Scheduling mismatch: search existing corporate brand posts by UUID before create/update.
- Publication failure: inspect provider status and Instagram account connection; record failure and retry only after checking duplicates.

## Operational checks
Before each publication: approved source, rights/privacy, exact media, OIDC transfer, public URL, corporate brand, caption, AI disclosure, schedule, no duplicates.
After publication: Instagram permalink and visual check, Metricool status, private ledger entry.
Monthly: review Actions deprecation warnings, branch protections, OIDC federation, Graph permission scope, Pages availability and documentation currency.

## First production evidence
- 2026-10-15: first four-image carousel published on `@midoritech.gardening`, visually confirmed by the account owner in Instagram.
- GitHub Actions import run: https://github.com/MT-Daisuke/midoritech-social-assets/actions/runs/38698950158 (success, 27 seconds, screenshot).
- Asset path: `instagram/2026/2026-10-launch/` (four PNG files).
- Metricool post ID `396580407`, UUID `1097384764266401573`; scheduled for 2026-10-15 16:45 JST, auto-publish enabled.
- Instagram screenshot around 17:00 JST showed a four-image carousel, caption, and AI content label. Exact public Instagram permalink was not captured in this record.
