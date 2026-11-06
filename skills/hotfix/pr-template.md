# Hotfix / Revert PR — Template de description

Les descriptions sont intentionnellement minimalistes.
Elles référencent l'issue et la PR d'origine, rien de plus.

## Hotfix

```
- #<ISSUE_NUMBER>
- hotfix of #<MAIN_PR_NUMBER>
```

### Titre
```
hotfix(ISSUE_NUMBER): <titre exact de la PR principale>
```

### Exemples réels
```
- #22094
- hotfix of #22095
```

## Revert

```
- #<ISSUE_NUMBER>
- revert of #<MAIN_PR_NUMBER>
```

### Titre
```
revert(ISSUE_NUMBER): <titre exact de la PR principale>
```

### Exemples réels
```
- #22172
- revert of #22310
```

## Règles

- Ne pas réécrire la description de la PR principale — les reviewers ont déjà le contexte via le lien
- Ne pas ajouter de section "Is this covered by automated tests"
- Pas de labels spécifiques — les omettre
