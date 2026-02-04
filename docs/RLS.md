# Row Level Security (RLS)

Steps to apply policies.sql to Supabase:
1. Export project URL (SUPABASE_URL) and Service Role (SERVICE_ROLE_KEY).
2. Connect via SQL editor (Dashboard) or  CLI.
3. Run .sys/supabase/policies.sql.
4. Validate:
   - service_role: can INSERT/SELECT on context_ledger, decision_graph, agent_identities.
   - anon: denied for ALL on these tables.
5. Record verification output below.

Verification log:
- [ ] context_ledger OK
- [ ] decision_graph OK
- [ ] agent_identities OK
