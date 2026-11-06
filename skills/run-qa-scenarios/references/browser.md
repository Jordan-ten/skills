# Piloter le navigateur

Connexion et login dev : `tnx-dev-mcp-local-dev`. Ce qui suit, c'est seulement ce qui fausse un verdict
d'UI quand on l'ignore.

## Pièges qui produisent un faux échec

**Le même élément est souvent rendu deux fois.** Une modale peut contenir un en-tête collant et un bloc
de propriétés visible qui rendent tous deux le même composant. Le snapshot d'accessibilité peut ne
montrer que la copie cachée : un clic ou un survol tombe alors sur quelque chose que l'utilisateur ne
voit pas, et rien ne se passe.

Avant d'interagir, ne garder que l'instance visible :

```js
() => [...document.querySelectorAll('<selector>')]
  .filter(el => {
    const rect = el.getBoundingClientRect()
    const style = getComputedStyle(el)
    return rect.width > 0 && rect.height > 0
      && style.visibility !== 'hidden' && style.pointerEvents !== 'none' && style.opacity !== '0'
  })
```

Une copie cachée se trouve en général sous un ancêtre avec `pointer-events: none` ou `opacity-0`, ou
n'est pas affichée (`display: none` donne une boîte de taille nulle).

**Un tooltip n'est pas dans le snapshot d'accessibilité.** Ant Design le monte au survol, en dehors du
composant. `take_snapshot` ne le montrera pas. Le lire plutôt dans le DOM :

```js
() => [...document.querySelectorAll('.ant-tooltip')]
  .filter(t => !t.classList.contains('ant-tooltip-hidden'))
  .map(t => t.innerText)
```

**Survoler par l'uid du snapshot peut rater.** Quand `mcp__chrome-devtools__hover` ne donne aucun
résultat, envoyer soi-même les événements sur l'élément choisi, puis attendre que le tooltip se monte :
`pointerover`, `mouseover`, `pointerenter`, `mouseenter`, `mousemove`, puis ~1s.

**Une boîte de dialogue vide veut dire qu'elle charge encore.** Attendre un texte attendu (`wait_for`)
avant de lire une modale. Ne pas conclure sur un snapshot pris trop tôt.

## Ce qui compte comme preuve

- Une capture d'écran pour tout ce qui est visuel (une mise en page, un tooltip, un libellé tronqué).
- Le texte lu dans le DOM pour une liste, un libellé, un tooltip.
- `list_console_messages` avec `types: ["error"]` pour un scénario sur une erreur.
- La sortie du test quand le scénario a été vérifié par un test automatique.

## Laisser l'app comme on l'a trouvée

La base de dev est celle de l'utilisateur. Ne pas envoyer de formulaire, ne pas supprimer
d'enregistrement, ne pas changer de réglage, sauf si le scénario porte sur cette action et qu'elle était
marquée comme une écriture dans la liste de l'étape 1 que l'utilisateur a acceptée. Fermer ce qu'on a
ouvert et revenir à l'écran de liste à la fin du run.
