---
name: audit-skills
description: Slash-only. À utiliser uniquement quand l'utilisateur lance explicitement /audit-skills. Audite les skills du repo de plugin personnel selon les conventions actuelles de Claude Code et les changements récents, puis propose et applique des corrections après accord de l'utilisateur. Ne jamais déclencher depuis une demande en langage naturel.
disable-model-invocation: true
argument-hint: "[repo path, default ~/code/skills]"
allowed-tools: Bash(python3 *), Bash(git *), Bash(claude --version), Read, Edit, Write, Glob, Grep, WebFetch, WebSearch, Agent, AskUserQuestion
---

# Audit Skills

Garde les skills du repo de plugin personnel à jour avec la doc de Claude Code.

`REPO` est `$ARGUMENTS`, ou `~/code/skills`. Travaille seulement dans `REPO`. Ne modifie jamais les skills d'un repo de projet.

## Étapes

1. **Lancer les vérifications mécaniques.**
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/audit-skills/scripts/check_skills.py REPO`
   Les lignes sont `LEVEL<TAB>skill<TAB>message`. Les lignes `INFO` listent les clés de front matter utilisées.
   Certains avertissements sont des faux positifs (un fichier qui appartient à un autre skill, par exemple). Lis le
   skill avant de garder un constat.

2. **Lire les règles actuelles.** Ne te fie pas à ta mémoire : les conventions changent.
   - Lis la doc en ligne : `https://code.claude.com/docs/en/skills` et `https://code.claude.com/docs/en/plugins`
     (et la page du marketplace de plugins). Utilise l'agent `claude-code-guide`, ou `WebFetch`.
   - Lis `REPO/.last-audit.json` s'il existe (`date`, `claudeVersion`). Regarde les notes de version ou le changelog
     de Claude Code depuis cette date. Sans le fichier, regarde les trois derniers mois.
   - Récupère la version installée avec `claude --version`.

3. **Comparer les skills avec la doc.** Cherche :
   - des clés de front matter utilisées qui sont renommées, dépréciées ou inconnues ;
   - des clés ou fonctions nouvelles qui valent la peine d'être adoptées (nomme chacune et dis pourquoi) ;
   - les règles sur les descriptions (longueur, formulation, quand l'utiliser) ;
   - les règles sur le corps (taille, découpage en `references/`, chemins de scripts, `${CLAUDE_PLUGIN_ROOT}`) ;
   - le format des fichiers de plugin et de marketplace (`plugin.json`, `marketplace.json`, `version`) ;
   - les dépendances à des fichiers ou des skills qui n'existent que dans un repo de projet.
   Chaque constat qui ne vient pas du script cite la page de la doc. Si tu ne peux pas le confirmer dans la
   doc, marque-le « à vérifier ». N'invente pas de règle.

4. **Rapporter dans le chat, en français.** Un seul tableau : gravité, skill, constat, correction proposée. Groupe
   les constats du script et les constats de la doc. Termine par les corrections que tu recommandes.
   N'écris aucun fichier de rapport.

5. **Demander quelles corrections appliquer** (`AskUserQuestion`). Ne supprime jamais un skill sans un oui explicite.

6. **Appliquer les corrections choisies.**
   - Modifie les fichiers du skill. Garde les noms en `kebab-case`, verbe en premier, sans préfixe `tnx-`.
   - Garde le glossaire du README synchronisé : une ligne par skill, mêmes groupes.
   - Relance le script. Aucun nouveau `ERROR`.
   - Incrémente le numéro de patch de `version` dans `.claude-plugin/plugin.json`.
   - Écris `REPO/.last-audit.json` avec la date du jour et la valeur de `claude --version`.

7. **Commit, sans push.** Un commit par changement logique, message en anglais simple. Dis à l'utilisateur de
   pousser et de lancer `/plugin marketplace update <marketplace-name>`.
