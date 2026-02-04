-- VibeSync_Code RLS Policies
-- Applied directly to Supabase eynfodzjjwyroyetrwlt

-- 1. Enable RLS
ALTER TABLE public.context_ledger ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.decision_graph ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_identities ENABLE ROW LEVEL SECURITY;

-- 2. Context Ledger: Authenticated service role has full access
CREATE POLICY "Service role full access" ON public.context_ledger
FOR ALL USING (auth.role() = 'service_role');

-- 3. Decision Graph: Authenticated service role has full access
CREATE POLICY "Service role full access" ON public.decision_graph
FOR ALL USING (auth.role() = 'service_role');

-- 4. Agent Identities: Authenticated service role has full access
CREATE POLICY "Service role full access" ON public.agent_identities
FOR ALL USING (auth.role() = 'service_role');

-- 5. Public read access (optional, currently restricted to service_role for security)
-- CREATE POLICY "Public read access" ON public.context_ledger FOR SELECT USING (true);
