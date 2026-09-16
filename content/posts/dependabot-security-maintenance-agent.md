---
title: "Autonomous Dependabot Security Maintenance Agent Prompt"
description: "Run a conservative, repository-by-repository workflow for investigating, fixing, validating, delivering, and reporting GitHub Dependabot security alerts."
seo_title: "Dependabot Security Agent Prompt"
keywords: "Dependabot security prompt, dependency security agent, GitHub security automation, vulnerability remediation prompt, coding agent prompt"
featured_image: /assets/images/ascii-grunge/dependabot-security-maintenance.webp
og_image: /assets/social/dependabot-security-maintenance-agent-social.png
og_image_alt: "ASCII-grunge dependency graph protected by a security shield in gold on black"
og_image_width: 1200
og_image_height: 630
custom_url: dependabot-security-maintenance-agent
date: 2026-09-16
author: Robert DeVore
categories: ["coding"]
tags: ["dependabot", "dependency security", "github", "automation", "coding agents"]
---

Use this prompt to give a capable coding agent a strict, safety-first process for resolving open Dependabot alerts across an explicit repository list. Replace the example repositories before running it, and make sure the agent has the required GitHub and repository access.

## Prompt

%%RAW_PROMPT:dependabot-security-maintenance-agent%%

## Safety Notes

Keep the repository list explicit and narrow. The prompt deliberately prioritizes minimum secure upgrades, native package-manager workflows, existing branch protections, and verified delivery over merely clearing the alert dashboard.
