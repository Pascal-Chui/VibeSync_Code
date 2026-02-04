# VibeSync Blueprint — V6.1 Plan

Scope (current)
- Core: ledger_sync + decision_sync delivered (tests 201 OK)
- DB: policies.sql (RLS) exported; AIM table present
- CI: smoke.yml present (needs Supabase secrets)
- Crons: nightly (01:00), morning brief (08:00), hourly ops sweep

Blocking items
- RLS not yet applied on Supabase → controlled access not active
- GitHub Action secrets required for CI

Next actions (ordered)
1) Apply RLS (policies.sql) and validate (service_role OK, anon deny)
2) Seed AIM (agent_identities) then confirm read access function
3) Extend README: tests, how to apply RLS, CI secrets
4) Initialize MCP server skeleton (.sys/mcp) + R/W endpoints and integration doc

Execution tracks
- Track A (CI-first): Use GitHub Action `apply-rls.yml` with one secret
  - Secret: SUPABASE_CONNECTION_STRING (copy psql string from Supabase → Project Settings → Database → Connection string → psql)
  - Run: Actions → apply-rls → Run workflow
- Track B (Dashboard): Paste .sys/supabase/policies.sql then seed_agent_identities.sql in SQL Editor

Acceptance criteria
- RLS enabled on context_ledger, decision_graph, agent_identities
- Policies grant FOR ALL to service_role only; anon denied by default
- AIM seeded with at least one identity (`macbot`) and readable via service role
- README updated with procedures and CI secrets
- MCP skeleton present with documented endpoints
