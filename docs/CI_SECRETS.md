# CI Secrets

Required for smoke tests:
- SUPABASE_URL
- SERVICE_ROLE_KEY

Add them as repository secrets in GitHub Actions: Settings → Secrets and variables → Actions.

Notes:
- Use service role only in CI/backends. Never expose in client.
- Rotate on compromise.
