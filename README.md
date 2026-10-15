# Midoritech Social Assets

Public, **approved** image assets for HTTPS delivery to corporate social publishing tools such as Metricool.

## Source-of-truth and publication policy
- SharePoint is the authoritative location for approvals, source images, captions and the private publication ledger. This repository hosts **public delivery copies only**.
- Do not upload credentials, private documents, personal data, unapproved imagery or signed SharePoint download URLs.
- Keep published asset URLs stable. Deleting a public Git file does not necessarily erase it from Git history.
- Instagram images: `instagram/YYYY/YYYY-MM-slug/`; numbered filenames preserve carousel order.
- Validate GitHub Actions success, **every** public image URL, Metricool media ingestion, and the actual Instagram publication independently.
- Decide AI disclosure **per post** from production provenance and applicable platform rules; never blindly set `isAiGenerated`.

## Procedures
- [Publishing standard operating procedure](docs/instagram-publishing-sop.md)
- [SharePoint importer and OIDC setup](docs/import-setup.md)
- [First publication verification record](docs/instagram-launch-2026-10-15.md)

## First production publication
- Account: `@midoritech.gardening`
- Assets: `instagram/2026/2026-10-launch/` (four PNGs)
- SharePoint → GitHub Actions → GitHub Pages → Metricool → Instagram
- **Published 2026-10-15**; owner-confirmed via Instagram screenshot. [Import run](https://github.com/MT-Daisuke/midoritech-social-assets/actions/runs/38698950158).
- Importer supports reviewed manifest batches in `manifests/YYYY-MM-slug.json`; first-batch production evidence exists, and new-batch testing remains required.
