# Compatibility matrix

Native procedures are separated from historical dependency flags. No provider or Claude hook was executed. Procedure coverage is not live workflow verification.

| Kind | Name | Execution | Historical source status | Dependencies |
|---|---|---|---|---|
| agent | backend-dev | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, upstream_home |
| agent | book-fact-checker | native-procedure | requires-runtime-review | legacy_tool |
| agent | business-analyst | native-procedure | requires-runtime-review | legacy_tool, runtime_script, unresolved-or-illustrative-local-reference |
| agent | code-reviewer | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, upstream_home |
| agent | devops-engineer | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| agent | error-handler | native-procedure | instructions-adapted |  |
| agent | frontend-dev | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| agent | gemini-agent | connection-required | requires-runtime-review | credential_or_session |
| agent | gpt-agent | connection-required | requires-runtime-review | credential_or_session |
| agent | gsd-advisor-researcher | native-procedure | requires-runtime-review | legacy_tool |
| agent | gsd-assumptions-analyzer | native-procedure | requires-runtime-review | legacy_tool |
| agent | gsd-codebase-mapper | native-procedure | requires-runtime-review | credential_or_session |
| agent | gsd-debugger | native-procedure | requires-runtime-review | credential_or_session, legacy_tool, reference-code-not-adapted, unresolved-or-illustrative-local-reference, upstream_home |
| agent | gsd-executor | native-procedure | requires-runtime-review | legacy_tool, parameterized-or-external-local-reference, reference-code-not-adapted, upstream_home |
| agent | gsd-integration-checker | native-procedure | instructions-adapted |  |
| agent | gsd-nyquist-auditor | native-procedure | instructions-adapted |  |
| agent | gsd-phase-researcher | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, runtime_script, upstream_home |
| agent | gsd-plan-checker | native-procedure | requires-runtime-review | credential_or_session, legacy_tool, reference-code-not-adapted, upstream_home |
| agent | gsd-planner | native-procedure | requires-runtime-review | credential_or_session, legacy_tool, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, upstream_home |
| agent | gsd-project-researcher | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, upstream_home |
| agent | gsd-research-synthesizer | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| agent | gsd-roadmapper | native-procedure | requires-runtime-review | upstream_home |
| agent | gsd-ui-auditor | native-procedure | requires-runtime-review | upstream_home |
| agent | gsd-ui-checker | native-procedure | requires-runtime-review | upstream_home |
| agent | gsd-ui-researcher | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, upstream_home |
| agent | gsd-user-profiler | native-procedure | requires-runtime-review | credential_or_session, legacy_tool |
| agent | gsd-verifier | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| agent | bug-fixer | native-procedure | requires-runtime-review | credential_or_session, legacy_tool, upstream_home |
| agent | bug-hunter | native-procedure | requires-runtime-review | credential_or_session, legacy_tool |
| agent | dead-code-hunter | native-procedure | requires-runtime-review | legacy_tool |
| agent | dead-code-remover | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| agent | dependency-auditor | native-procedure | requires-runtime-review | legacy_tool |
| agent | dependency-updater | native-procedure | requires-runtime-review | legacy_tool |
| agent | reuse-fixer | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| agent | reuse-hunter | native-procedure | requires-runtime-review | legacy_tool |
| agent | security-scanner | native-procedure | requires-runtime-review | credential_or_session, legacy_tool |
| agent | vulnerability-fixer | native-procedure | requires-runtime-review | credential_or_session, legacy_tool, upstream_home |
| agent | image-generator | native-procedure | requires-runtime-review | credential_or_session |
| agent | integration-dev | native-procedure | requires-runtime-review | credential_or_session |
| agent | kimi-algorithm-specialist | connection-required | instructions-adapted |  |
| agent | legacy-modernizer | native-procedure | instructions-adapted |  |
| agent | memory-agent | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| agent | meta-agent-v3 | native-procedure | requires-runtime-review | claude_runtime, credential_or_session, legacy_tool, upstream_home |
| agent | ml-specialist | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| agent | orchestrator | native-procedure | instructions-adapted |  |
| agent | pentest-engineer | native-procedure | instructions-adapted |  |
| agent | presentation-master | native-procedure | instructions-adapted |  |
| agent | product-designer | native-procedure | requires-runtime-review | legacy_tool, runtime_script, unresolved-or-illustrative-local-reference |
| agent | prompt-engineer | native-procedure | instructions-adapted |  |
| agent | proofreader-ortho | native-procedure | instructions-adapted |  |
| agent | proofreader-punctuation | native-procedure | instructions-adapted |  |
| agent | proofreader-typography | native-procedure | instructions-adapted |  |
| agent | qa-specialist | native-procedure | instructions-adapted |  |
| agent | security-engineer | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| agent | senior-developer | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| agent | slide-designer | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| agent | software-architect | native-procedure | requires-runtime-review | credential_or_session, legacy_tool, runtime_script, unresolved-or-illustrative-local-reference |
| agent | system-analyst | native-procedure | requires-runtime-review | credential_or_session |
| agent | tech-lead | native-procedure | instructions-adapted |  |
| agent | accessibility-tester | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| agent | integration-tester | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| agent | mobile-fixes-implementer | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| agent | mobile-responsiveness-tester | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| agent | performance-optimizer | native-procedure | instructions-adapted |  |
| agent | test-writer | native-procedure | requires-runtime-review | legacy_tool, runtime_script |
| agent | vf-editor | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| agent | vf-operator | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| agent | vf-prompter | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| agent | vf-qc | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| agent | vf-screenwriter | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| agent | vf-sound | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| agent | vf-storyboard | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| agent | video-factory | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | README | native-procedure | requires-runtime-review | runtime_script, unresolved-or-illustrative-local-reference |
| command | add-auth | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| command | analyze | native-procedure | instructions-adapted |  |
| command | beads-init | native-procedure | requires-runtime-review | upstream_home |
| command | bot-debug | native-procedure | requires-runtime-review | runtime_script |
| command | bot-deploy | connection-required | requires-runtime-review | runtime_script |
| command | bot-test | native-procedure | requires-runtime-review | legacy_tool, runtime_script |
| command | brand-review | native-procedure | requires-runtime-review | legacy_tool, unresolved-or-illustrative-local-reference, upstream_home |
| command | bug-triage | native-procedure | requires-runtime-review | runtime_script |
| command | call-summary | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | campaign-plan | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | changelog | native-procedure | instructions-adapted |  |
| command | code-review | native-procedure | instructions-adapted |  |
| command | competitive-brief-mktg | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | competitive-brief | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | context-optimize | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| command | daily | native-procedure | instructions-adapted |  |
| command | deep-research | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | deploy | connection-required | instructions-adapted |  |
| command | docs | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| command | domain-dns-ops | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | draft-content | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | email-sequence | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | estimate | native-procedure | instructions-adapted |  |
| command | feature-cycle | native-procedure | instructions-adapted |  |
| command | forecast | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | gads | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | ganalytics | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | gcalendar | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | gchat | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | gcloud-storage | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | gcontacts | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | gdocs | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | gdrive | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | generate-api | native-procedure | requires-runtime-review | runtime_script |
| command | gmail | connection-required | requires-runtime-review | credential_or_session, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | gmeet | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | gsd:add-backlog | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:add-phase | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:add-tests | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:add-todo | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:audit-milestone | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, upstream_home |
| command | gsd:audit-uat | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:autonomous | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:check-todos | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:cleanup | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:complete-milestone | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:debug | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, upstream_home |
| command | gsd:discuss-phase | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, unresolved-or-illustrative-local-reference, upstream_home |
| command | gsd:do | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:execute-phase | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, upstream_home |
| command | gsd:fast | native-procedure | requires-runtime-review | upstream_home |
| command | gsd:forensics | native-procedure | requires-runtime-review | credential_or_session, upstream_home |
| command | gsd:health | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, unresolved-or-illustrative-local-reference, upstream_home |
| command | gsd:help | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | gsd:insert-phase | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:join-discord | native-procedure | instructions-adapted |  |
| command | gsd:list-phase-assumptions | native-procedure | requires-runtime-review | upstream_home |
| command | gsd:list-workspaces | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:manager | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, upstream_home |
| command | gsd:map-codebase | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:milestone-summary | native-procedure | requires-runtime-review | upstream_home |
| command | gsd:new-milestone | native-procedure | requires-runtime-review | legacy_tool, parameterized-or-external-local-reference, reference-code-not-adapted, upstream_home |
| command | gsd:new-project | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:new-workspace | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:next | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:note | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, unresolved-or-illustrative-local-reference, upstream_home |
| command | gsd:pause-work | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:plan-milestone-gaps | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:plan-phase | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, upstream_home |
| command | gsd:plant-seed | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:pr-branch | native-procedure | requires-runtime-review | upstream_home |
| command | gsd:profile-user | native-procedure | requires-runtime-review | reference-code-not-adapted, unresolved-or-illustrative-local-reference, upstream_home |
| command | gsd:progress | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:quick | native-procedure | requires-runtime-review | legacy_tool, parameterized-or-external-local-reference, reference-code-not-adapted, upstream_home |
| command | reapply-patches | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | gsd:remove-phase | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:remove-workspace | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:research-phase | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, upstream_home |
| command | gsd:resume-work | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:review-backlog | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:review | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:session-report | native-procedure | requires-runtime-review | upstream_home |
| command | gsd:set-profile | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:settings | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:ship | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:stats | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:thread | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:ui-phase | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, upstream_home |
| command | gsd:ui-review | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:update | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | gsd:validate-phase | native-procedure | requires-runtime-review | reference-code-not-adapted, upstream_home |
| command | gsd:verify-work | native-procedure | requires-runtime-review | legacy_tool, reference-code-not-adapted, upstream_home |
| command | workstreams | native-procedure | instructions-adapted |  |
| command | gsearch-console | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | gsheets | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | gtasks | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | gtd | connection-required | requires-runtime-review | credential_or_session, legacy_tool, upstream_home |
| command | gtranslate | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | health-bugs | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| command | health-cleanup | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| command | health-deps | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| command | health-reuse | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| command | health-security | native-procedure | requires-runtime-review | legacy_tool, upstream_home |
| command | init-project | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| command | kb | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| command | kimi-reasoning | connection-required | requires-runtime-review | credential_or_session |
| command | manus | connection-required | requires-runtime-review | credential_or_session, runtime_script, upstream_home |
| command | meeting | native-procedure | instructions-adapted |  |
| command | memory-extract | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | memory-ingest | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | memory-learn | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| command | memory-search | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | memory-stats | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| command | metrics-review | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | monitor-agents | native-procedure | instructions-adapted |  |
| command | orchestrate | native-procedure | requires-runtime-review | legacy_tool |
| command | outlook | connection-required | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| command | parallel-dev | native-procedure | instructions-adapted |  |
| command | performance-report | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | performance | native-procedure | requires-runtime-review | runtime_script |
| command | pipeline-review | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | plan-my-day | connection-required | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| command | prompt-log | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, upstream_home |
| command | proofread | native-procedure | instructions-adapted |  |
| command | push | connection-required | requires-runtime-review | runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | quick-deploy | connection-required | requires-runtime-review | runtime_script |
| command | rename-sessions | native-procedure | requires-runtime-review | legacy_tool, unresolved-or-illustrative-local-reference, upstream_home |
| command | retro | native-procedure | requires-runtime-review | runtime_script |
| command | review | native-procedure | instructions-adapted |  |
| command | roadmap-update | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | roadmap | native-procedure | instructions-adapted |  |
| command | scaffold | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| command | search-chats | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| command | security-scan | native-procedure | requires-runtime-review | credential_or_session |
| command | self-learn | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | seo-audit | native-procedure | requires-runtime-review | legacy_tool, unresolved-or-illustrative-local-reference, upstream_home |
| command | setup-db | native-procedure | requires-runtime-review | credential_or_session, runtime_script, unresolved-or-illustrative-local-reference |
| command | slides | connection-required | requires-runtime-review | reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| command | specs | native-procedure | instructions-adapted |  |
| command | sprint-planning-pm | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | sprint-planning | native-procedure | instructions-adapted |  |
| command | stakeholder-update | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | standup-report | native-procedure | instructions-adapted |  |
| command | start-feature | native-procedure | instructions-adapted |  |
| command | synthesize-research | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | test-frontend | native-procedure | instructions-adapted |  |
| command | transcribe | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | translate | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| command | ultra-think | native-procedure | instructions-adapted |  |
| command | userflow | native-procedure | instructions-adapted |  |
| command | video-factory | native-procedure | instructions-adapted |  |
| command | weekly-synthesis | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| command | worktree | native-procedure | instructions-adapted |  |
| command | write-spec | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| command | youtube-upload | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | a11y-audit | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | ab-testing-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | account-research | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | ace-step | native-helper | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, upstream_home |
| skill | ad-benchmarks-ru | native-procedure | instructions-adapted |  |
| skill | ad-spy | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | agent-api-server | native-procedure | requires-runtime-review | claude_runtime, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | ai-creative-factory-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | ai-marketing-stack-ru | native-procedure | requires-runtime-review | runtime_script, unresolved-or-illustrative-local-reference |
| skill | ai-seo-agent-pipeline | connection-required | requires-runtime-review | legacy_tool, runtime_script, unresolved-or-illustrative-local-reference |
| skill | algorithmic-art | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted |
| skill | animations | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted |
| skill | api-documentation | native-procedure | instructions-adapted |  |
| skill | apify-scraping | connection-required | instructions-adapted |  |
| skill | apple-developer | connection-required | requires-runtime-review | credential_or_session, runtime_script |
| skill | article-pipeline | native-procedure | requires-runtime-review | legacy_tool, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | author-voice | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | autocad-com | native-helper | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | autonomous-agent-creator | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, dependency-manifest-not-installed, legacy_tool, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | away-summary | native-procedure | instructions-adapted |  |
| skill | aws-skills | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| skill | b2b-marketing-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | beads | native-procedure | instructions-adapted |  |
| skill | book-polish-pipeline | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | book-post | native-procedure | requires-runtime-review | bundled-reference-code, dependency-manifest-not-installed, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | brand-extractor | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | brand-guidelines | native-procedure | instructions-adapted |  |
| skill | brand-voice | native-procedure | instructions-adapted |  |
| skill | btw | native-procedure | instructions-adapted |  |
| skill | build-fix | native-procedure | instructions-adapted |  |
| skill | call-prep | native-procedure | instructions-adapted |  |
| skill | campaign-planning | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | canonical-html | native-procedure | instructions-adapted |  |
| skill | canvas-design | native-procedure | instructions-adapted |  |
| skill | capi-no-code-setup | connection-required | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | cards-creator | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | career-ops | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | ceo-council | native-procedure | requires-runtime-review | legacy_tool, unresolved-or-illustrative-local-reference, upstream_home |
| skill | changelog-generator | native-procedure | requires-runtime-review | credential_or_session, runtime_script, unresolved-or-illustrative-local-reference |
| skill | check-skill-solo | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, unresolved-or-illustrative-local-reference, upstream_home |
| skill | churn-prevention-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | citp-research-ru | native-procedure | instructions-adapted |  |
| skill | claude-api | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | claude-cli-runner | native-procedure | requires-runtime-review | claude_runtime, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | claude-design | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, legacy_tool, reference-code-not-adapted, unresolved-or-illustrative-local-reference |
| skill | claude-in-html | connection-required | requires-runtime-review | credential_or_session, runtime_script |
| skill | claude-server-auth | connection-required | requires-runtime-review | bundled-reference-code, claude_runtime, credential_or_session, reference-code-not-adapted, runtime_script, upstream_home |
| skill | codegraph | native-procedure | requires-runtime-review | runtime_script |
| skill | color-system-builder | native-procedure | requires-runtime-review | runtime_script |
| skill | comment-injector | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | comment-replies | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | comparison-mode | native-procedure | requires-runtime-review | runtime_script |
| skill | competitive-analysis-mktg | native-procedure | requires-runtime-review | upstream_home |
| skill | competitive-analysis | native-procedure | requires-runtime-review | credential_or_session |
| skill | competitive-intelligence | native-procedure | requires-runtime-review | upstream_home |
| skill | component-playground | native-procedure | instructions-adapted |  |
| skill | content-creation | native-procedure | instructions-adapted |  |
| skill | content-engine | native-procedure | instructions-adapted |  |
| skill | content-machine-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | content-policy | native-procedure | instructions-adapted |  |
| skill | content-research | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | content-rules | native-procedure | instructions-adapted |  |
| skill | context-engineering | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| skill | cookbook | native-procedure | instructions-adapted |  |
| skill | create-an-asset | native-procedure | instructions-adapted |  |
| skill | critique-mode | native-procedure | instructions-adapted |  |
| skill | csv-analysis | native-helper | instructions-adapted |  |
| skill | d3-visualization | native-procedure | instructions-adapted |  |
| skill | daily-briefing | native-procedure | instructions-adapted |  |
| skill | dark-mode-add | native-procedure | instructions-adapted |  |
| skill | database-design | native-procedure | requires-runtime-review | runtime_script, unresolved-or-illustrative-local-reference |
| skill | de-ai-ify | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | deck-themes | native-procedure | instructions-adapted |  |
| skill | deepgram | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | deepl-pro | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | deepseek | connection-required | requires-runtime-review | credential_or_session, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | deepwiki | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | design-canvas | native-procedure | instructions-adapted |  |
| skill | design-guardrails | native-procedure | instructions-adapted |  |
| skill | design-guide | native-procedure | instructions-adapted |  |
| skill | design-md-brands | native-procedure | instructions-adapted |  |
| skill | design-orchestrator | native-procedure | instructions-adapted |  |
| skill | design-system-create | native-procedure | instructions-adapted |  |
| skill | design-taste | native-procedure | instructions-adapted |  |
| skill | design-tokens-w3c | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | dev-browser | native-procedure | requires-runtime-review | bundled-reference-code, dependency-manifest-not-installed, reference-code-not-adapted, runtime_script |
| skill | dev-handoff | native-procedure | instructions-adapted |  |
| skill | developer-growth | native-procedure | instructions-adapted |  |
| skill | device-frames | native-procedure | instructions-adapted |  |
| skill | did | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | d-id | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | document-import | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | docx | native-procedure | requires-runtime-review | runtime_script, upstream_home |
| skill | domain-brainstormer | native-procedure | requires-runtime-review | credential_or_session |
| skill | draft-outreach | native-procedure | requires-runtime-review | upstream_home |
| skill | dream | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | edit-banana | native-helper | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | elevenlabs | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | email-imap | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | emil-design-eng | native-procedure | instructions-adapted |  |
| skill | epub-tools | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, upstream_home |
| skill | excalidraw-flowchart | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, upstream_home |
| skill | export-pdf | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | export-png | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | export-pptx | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | feature-spec | native-procedure | requires-runtime-review | credential_or_session |
| skill | figma-api | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | figma-import | connection-required | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | figma-write-back | connection-required | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | file-converter | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, upstream_home |
| skill | file-organizer | native-procedure | requires-runtime-review | runtime_script |
| skill | fonts-bundle | native-procedure | instructions-adapted |  |
| skill | form-cro-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | forms-a11y | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | free-tools-lead-magnets-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | frontend-design | native-procedure | instructions-adapted |  |
| skill | full-funnel-analytics-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | funnel-design-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | gamma | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | gemini-3-pro | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, unresolved-or-illustrative-local-reference, upstream_home |
| skill | generate-report-header | native-procedure | requires-runtime-review | legacy_tool |
| skill | geo-aeo-ru | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | git-workflow | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| skill | github-gem-seeker | native-procedure | instructions-adapted |  |
| skill | github-import | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | google-ads-pro-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | google-workspace | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, legacy_tool, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | graph-memory | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | gstack | native-procedure | requires-runtime-review | bundled-reference-code, dependency-manifest-not-installed, legacy_tool, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | browse | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | document-release | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | gstack-upgrade | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | plan-ceo-review | native-procedure | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | plan-eng-review | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | qa-only | native-procedure | requires-runtime-review | credential_or_session, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | qa | native-procedure | requires-runtime-review | credential_or_session, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | retro | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | review | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | setup-browser-cookies | native-procedure | requires-runtime-review | runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | ship | native-procedure | requires-runtime-review | runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | habr-post | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | health-inline | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | heygen | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | home-assistant | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | html-email | native-procedure | instructions-adapted |  |
| skill | i18n-stress-test | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | image-enhancer | native-helper | requires-runtime-review | credential_or_session |
| skill | image-generation | native-procedure | requires-runtime-review | credential_or_session, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | influencer-buying-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | installer-builder | native-procedure | requires-runtime-review | runtime_script, unresolved-or-illustrative-local-reference |
| skill | interactive-prototype | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| skill | internal-comms | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | investor-materials | native-procedure | instructions-adapted |  |
| skill | invoice-organizer | native-procedure | instructions-adapted |  |
| skill | javascript-typescript-dev | native-procedure | instructions-adapted |  |
| skill | jtbd | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | kimi | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | landing-page-effects | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | last30days | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, legacy_tool, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | launch-strategy-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | lead-research | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | leak-scan | native-helper | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | license-check | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | linkedin-comment-drafter | native-procedure | instructions-adapted |  |
| skill | linkedin-reply-handler | native-procedure | requires-runtime-review | credential_or_session |
| skill | linkedin-thread-engagement | native-procedure | instructions-adapted |  |
| skill | linkedin-employee-advocacy | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | linkedin-humanizer | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, unresolved-or-illustrative-local-reference |
| skill | linkedin-detector-tester | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | linkedin-emoji-detector | native-procedure | instructions-adapted |  |
| skill | linkedin-post-audit | native-procedure | instructions-adapted |  |
| skill | linkedin-rules-explainer | native-procedure | instructions-adapted |  |
| skill | linkedin-post-author | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | linkedin-post-writer | native-procedure | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference |
| skill | linkedin-content-planner | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | linkedin-hook-extractor | native-procedure | instructions-adapted |  |
| skill | linkedin-profile-optimizer | native-procedure | instructions-adapted |  |
| skill | linkedin | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | live-preview | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | llm-evals | connection-required | requires-runtime-review | bundled-reference-code, claude_runtime, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | manus-slides | connection-required | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | manus | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | manychat-funnel-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | maps-places | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | market-selection-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | marketing-decisions-ru | native-procedure | instructions-adapted |  |
| skill | marketing-loops-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | marketing-masterminds-ru | native-procedure | instructions-adapted |  |
| skill | marketing-orchestrator | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | marketing-psychology-ru | native-procedure | instructions-adapted |  |
| skill | marketing-team-builder-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | marp-presentations | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | mcp-builder | native-procedure | requires-runtime-review | bundled-reference-code, dependency-manifest-not-installed, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | media-planning-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | meeting-analyzer | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | memory-agent | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | meta-ads-analyzer | native-procedure | instructions-adapted |  |
| skill | meta-ads-launch-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | metrics-tracking | native-procedure | instructions-adapted |  |
| skill | microinteractions | native-procedure | instructions-adapted |  |
| skill | miro | connection-required | requires-runtime-review | claude_runtime, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | mobile-overlays | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | moodboard | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | multi-model-gateway | connection-required | requires-runtime-review | credential_or_session, legacy_tool |
| skill | n8n | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, dependency-manifest-not-installed, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | nano-banana-pro | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference |
| skill | notebooklm | connection-required | requires-runtime-review | credential_or_session, runtime_script |
| skill | ocr-restore | native-helper | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | offers-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | onboarding-cro-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | onboarding-ux | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | openai-dalle | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | openwiki | native-procedure | requires-runtime-review | credential_or_session |
| skill | osint-recon | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | page-cro-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | parse-git-status | native-helper | instructions-adapted |  |
| skill | paywall-cro-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | pdf | native-procedure | instructions-adapted |  |
| skill | perf-audit | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | performance-analytics | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | perplexity | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | pgvector-rag | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| skill | pinecone | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | placeholders | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | playwright-automation | native-procedure | requires-runtime-review | bundled-reference-code, claude_runtime, legacy_tool, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | popup-cro-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | postiz | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | pptx-editable-extractor | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | pptx-import | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | pptx | native-procedure | instructions-adapted |  |
| skill | pr-outreach-ru | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | pricelist-latin-check | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, upstream_home |
| skill | pricing-strategy-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | print-styles | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | privacy-filter | native-helper | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | prompt-engineering | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, unresolved-or-illustrative-local-reference |
| skill | senior-prompt-engineer | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | proto-smoketest | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, unresolved-or-illustrative-local-reference |
| skill | publora-post | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | bluesky-post | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | instagram-post | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | linkedin-analytics | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | linkedin-post | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | social-post | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | telegram-post | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | threads-post | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | tiktok-post | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | x-post | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | pwa-shell | native-procedure | instructions-adapted |  |
| skill | python-fullstack-dev | native-procedure | instructions-adapted |  |
| skill | questions-protocol | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | rbc-post | native-procedure | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | react-pinning | native-procedure | requires-runtime-review | runtime_script |
| skill | real-data | native-procedure | requires-runtime-review | runtime_script, unresolved-or-illustrative-local-reference |
| skill | reddit-hn | native-procedure | instructions-adapted |  |
| skill | referrals-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | replicate | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | research-docs | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | review-animations | native-procedure | instructions-adapted |  |
| skill | revops-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | roadmap-management | native-procedure | instructions-adapted |  |
| skill | rollback-changes | native-procedure | instructions-adapted |  |
| skill | romance-novel-pipeline | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| skill | ru-text | native-procedure | instructions-adapted |  |
| skill | run-quality-gate | native-procedure | instructions-adapted |  |
| skill | sales-enablement-ru | native-procedure | requires-runtime-review | runtime_script, upstream_home |
| skill | sales-team-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | save-knowledge-base | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | scaling-stage | native-procedure | instructions-adapted |  |
| skill | schema-markup-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | screen-labels | native-procedure | instructions-adapted |  |
| skill | screenshot-test | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | sdat | connection-required | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | security-audit | native-procedure | requires-runtime-review | credential_or_session, runtime_script |
| skill | self-reflect | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | seo-machine-ru | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | serpapi | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, unresolved-or-illustrative-local-reference, upstream_home |
| skill | session-mentor | native-procedure | requires-runtime-review | bundled-reference-code, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | sharing-skills | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference, upstream_home |
| skill | shorts-pipeline | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, dependency-manifest-not-installed, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | similarweb-analytics | connection-required | requires-runtime-review | credential_or_session, runtime_script, unresolved-or-illustrative-local-reference |
| skill | sketch-to-html | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | skill-audit | native-procedure | requires-runtime-review | reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | skill-creator | native-procedure | requires-runtime-review | bundled-reference-code, claude_runtime, legacy_tool, reference-code-not-adapted, runtime_script |
| skill | slack-gif-creator | native-helper | requires-runtime-review | bundled-reference-code, dependency-manifest-not-installed, reference-code-not-adapted |
| skill | slides | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted |
| skill | sms-twilio | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | social-intel | native-procedure | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | stakeholder-comms | native-procedure | instructions-adapted |  |
| skill | standalone-html | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | states-checklist | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | sticker-pack-generator | native-helper | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | stock-analysis | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, upstream_home |
| skill | storybook-bridge | native-procedure | instructions-adapted |  |
| skill | submagic | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | tapestry | native-procedure | instructions-adapted |  |
| skill | telegram-ads-pro-ru | native-procedure | instructions-adapted |  |
| skill | telegram-bot-toolkit | native-procedure | requires-runtime-review | runtime_script |
| skill | tender-search-ru | native-procedure | instructions-adapted |  |
| skill | text-to-lottie | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | tg-bot-publish | connection-required | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | tg-channel-buyout-ru | native-procedure | requires-runtime-review | upstream_home |
| skill | tg-post | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | theme-factory | native-procedure | instructions-adapted |  |
| skill | thinking-frameworks | native-procedure | instructions-adapted |  |
| skill | threat-hunting | native-procedure | requires-runtime-review | runtime_script |
| skill | tiktok-intel | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | tilda-bitrix-e2e-test | connection-required | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | tilda | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | tool-search-protocol | native-procedure | requires-runtime-review | credential_or_session, unresolved-or-illustrative-local-reference, upstream_home |
| skill | trend-engine | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | tweaks-panel | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | type-scale | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | user-research-synthesis | native-procedure | instructions-adapted |  |
| skill | validate-plan-file | native-procedure | requires-runtime-review | upstream_home |
| skill | vc-post | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | verifier | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | version-snapshots | native-helper | requires-runtime-review | bundled-reference-code, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | video-downloader | native-procedure | instructions-adapted |  |
| skill | video-editor | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | video-export | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | video-factory-pipeline | native-procedure | requires-runtime-review | credential_or_session, legacy_tool, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | video-generation | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, dependency-manifest-not-installed, parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | video-montage | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, legacy_tool, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | video-shotcraft | native-procedure | requires-runtime-review | bundled-reference-code, dependency-manifest-not-installed, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | viral-shorts-playbook | native-procedure | instructions-adapted |  |
| skill | visual-edit | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | vk-ads-pro-ru | native-procedure | instructions-adapted |  |
| skill | void-video | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, upstream_home |
| skill | watch-video | native-procedure | instructions-adapted |  |
| skill | web-artifacts-builder | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | web-assets-generator | native-helper | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference |
| skill | webapp-testing | native-procedure | requires-runtime-review | bundled-reference-code, reference-code-not-adapted, runtime_script |
| skill | webhook-receiver | native-procedure | requires-runtime-review | credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | webinar-to-pdf | native-procedure | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | website-creation | native-procedure | instructions-adapted |  |
| skill | wireframe | native-procedure | requires-runtime-review | unresolved-or-illustrative-local-reference |
| skill | xlsx | native-procedure | instructions-adapted |  |
| skill | yandex-direct-pro-ru | native-procedure | requires-runtime-review | credential_or_session |
| skill | yandex | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | year-review | native-procedure | requires-runtime-review | parameterized-or-external-local-reference, reference-code-not-adapted, runtime_script, upstream_home |
| skill | youtube-analytics | connection-required | requires-runtime-review | bundled-reference-code, credential_or_session, reference-code-not-adapted, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
| skill | youtube-transcript | connection-required | instructions-adapted |  |
| skill | zoom | connection-required | requires-runtime-review | credential_or_session, runtime_script, unresolved-or-illustrative-local-reference, upstream_home |
