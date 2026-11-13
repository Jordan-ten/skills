---
name: write-implementation-plan
description: >
  Slash uniquement. À utiliser seulement quand l'utilisateur lance explicitement
  /write-implementation-plan, avec une issue GitHub (URL ou numéro) ou une description libre de la
  tâche. Écrit le plan d'implémentation d'un package (backend ou frontend) : résultat attendu
  observable, exploration du code, tranche verticale d'abord, une preuve par étape, pre-mortem, contrôle
  de cohérence. N'écrit aucun code. Ne jamais déclencher depuis une demande en langage naturel.
disable-model-invocation: true
allowed-tools: Bash(gh issue view *), Bash(git *), Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion
---

# Écrire un plan d'implémentation

Entrée : `/write-implementation-plan <url-ou-numéro-d'issue | description libre>`.

## But

Un plan qui atteint le résultat voulu, pas seulement un plan qui liste des étapes. Il est bon quand :

- chaque critère observable est servi par une étape et couvert par un test ;
- chaque étape a une preuve exécutable ;
- un lecteur sait quoi construire et où, sans deviner.

Le plan suit `references/plan-template.md` (structure, règles du contenu, contrôle de cohérence). Ce
template sert aussi la phase 2 de `feature-implementation-workflow` : ses parties sont marquées
**(workflow)**.

## Contraintes

- **Critères.** Avec une issue, ce sont ses scénarios : lis aussi ses commentaires, les décisions tardives
  y vivent souvent. Avec une description libre, propose 2 à 5 critères observables et fais-les valider.
  Si aucun critère observable n'est possible, arrête-toi et dis pourquoi.
- **Explorer avant d'écrire.** Fonctionnalité voisine la plus proche, `docs/product/<module>/overview.md`,
  mots déjà utilisés (grep avant d'employer un mot), tests de la zone, style de code du package. Ne pose
  jamais à l'utilisateur une question dont le code connaît la réponse.
- **Tranche verticale d'abord** : le plus petit chemin de bout en bout, jusqu'à un test qui passe.
  L'enrichissement vient après.
- **N'invente aucune règle métier.** Un cas limite ou un cas d'erreur est une proposition : l'utilisateur
  décide.
- **Tests** (détails : skill `test-patterns`) : e2e d'abord, sur un scénario métier réaliste, jamais sur
  une garde d'entrée ; test unitaire seulement pour une logique métier non triviale ; aucun test pour un
  wrapper trivial. Une migration n'a jamais de test automatisé : sa preuve est manuelle.
- **Plusieurs packages** : un plan par package, backend d'abord, car le frontend a besoin de son contrat.
- **Questions non résolues** : une par une avec `AskUserQuestion`, la réponse recommandée en premier. Une
  question que seule une autre personne peut trancher met `status: not-ready` : dis-le.
- **Aucun effet de bord** : pas de code, pas de branche, aucune écriture sur GitHub. Préviens l'utilisateur
  avant d'écraser un plan existant.
- Réponds en français, le plan aussi. Le produit s'appelle Tennaxia (règle de nommage de `AGENTS.md`).

## Conditions de sortie

- [ ] Le contrôle de cohérence du template passe. Montre chaque ligne (✅ ou ❌), et corrige un ❌ avant de
      montrer le plan.
- [ ] Les questions non résolues sont closes, ou `status: not-ready` le dit.
- [ ] L'utilisateur a validé le plan, sauvegardé à l'emplacement du template (section « Fichier »).

Termine par la suite : compacter, puis implémenter en suivant le plan.
