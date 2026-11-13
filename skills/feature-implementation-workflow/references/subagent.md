# Sous-agents (phases 3 et 4)

But : le travail lourd tourne hors de la session principale. Le sous-agent lit les fichiers, fait le
travail et renvoie un rapport court. La session principale ne garde que le rapport.

Type : `general-purpose`, jamais `fork`. Un sous-agent à la fois : les PR et leurs vérifications
dépendent les unes des autres.

## Brief (ce que la session principale donne)

Seulement des chemins et des numéros. Ne colle ni l'issue, ni le plan : le sous-agent les lit.

- Le numéro et l'URL de l'issue.
- Le chemin du plan du package, et celui du plan de l'autre package.
- La PR à faire : son numéro dans `## Pull requests`, sa branche, ses étapes (phase 3), ou la liste des
  PR à vérifier (phase 4).
- Le chemin absolu du fichier de phase à lire et à appliquer (`references/phases/3-implement.md` ou
  `4-verify.md`).
- Les environnements qui tournent (`test` port 3007, `dev`), démarrés par la session principale.
- Les règles dures : ne pousse pas, n'écris rien sur GitHub, ne démarre ni n'arrête aucun serveur, ne pose
  aucune question à l'utilisateur.
- Le format du rapport (ci-dessous).

## Règles du sous-agent

- Lis le fichier de phase, le plan, l'issue et le style de code du package. Applique-les.
- Redirige toute sortie longue dans un fichier du scratchpad et lis la fin (`tail`) ou un `grep`.
- Phase 3 : après chaque commit, mets à jour la colonne `Avancement` de la PR dans le plan.
- Arrête-toi et rapporte, sans deviner, quand : une décision revient à l'utilisateur ; le même échec
  revient 3 fois ; un serveur ou un outil n'est pas disponible ; le plan et le code se contredisent.

## Rapport (30 lignes au plus)

- Une ligne par condition de sortie du fichier de phase : ✅ ou ❌, avec la commande et le résultat en
  quelques mots.
- Les commits : SHA et message, une ligne chacun.
- Les écarts avec le plan, et pourquoi, une ligne chacun.
- Les questions pour l'utilisateur, si le sous-agent s'est arrêté sur une décision.

Pas de log, pas de diff, pas de contenu de fichier.

## Côté session principale

- Avant d'afficher un ✅, vérifie toi-même ce qui se vérifie en une commande : `git status --short`,
  `git log` de la branche, présence des fichiers. Un rapport ne remplace pas une vérification.
- Une question dans le rapport : pose-la à l'utilisateur avec `AskUserQuestion`, puis envoie la réponse
  au même sous-agent avec `SendMessage`.
- Un ❌ ou un rapport incomplet : corrige avec `SendMessage` au même sous-agent. Lance un nouveau
  sous-agent seulement quand le premier est bloqué.
- Un outil indisponible dans le sous-agent (serveur, navigateur) : la session principale fait cette
  étape elle-même.
