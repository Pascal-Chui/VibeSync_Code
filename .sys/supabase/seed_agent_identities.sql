-- Seed example for agent_identities (AIM)
insert into public.agent_identities (id, name, persona, metadata)
values (
  gen_random_uuid(),
  'macbot',
  'Calm, focused, proactive operator; executes end-to-end with minimal friction.',
  jsonb_build_object(
    'version','v1',
    'capabilities', array['context_orchestration','mcp','rls_validation'],
    'created_by','bootstrap'
  )
)
on conflict (id) do nothing;
