# Seventh OS — site

Le site de téléchargement de Seventh OS, hébergé gratuitement sur Cloudflare Pages : **https://seventh-os.pages.dev**

- `public/` : la page (HTML, CSS, JS), les polices et les icônes.
- `functions/download.js` : `/download` redirige vers l'installateur de la dernière release de `se7enclaude/seventh-os`.
  C'est le lien court à partager.
- `functions/api/latest.js` : `/api/latest` donne la version, la taille et le lien de l'installateur.
- La liste des applis est lue en direct dans `apps.json` du hub : une appli ajoutée à Seventh OS apparaît sur le site
  sans rien republier. Son icône vient de `public/assets/icons/`, ou à défaut de `ui/icons/` du hub.
- `tools/make_og.py` : refait l'image de partage `public/assets/og.png` (Discord, X…).

## Commandes

```
npm install
npm run dev        aperçu sur http://localhost:8788 (avec /download et /api/latest)
npm run deploy     mise en ligne sur Cloudflare Pages (projet « seventh-os »)
```

La première mise en ligne demande `npx wrangler login`, une fois, avec le compte Cloudflare.

## Mise en ligne automatique (au choix)

Dans Cloudflare : Workers & Pages › Créer › Pages › Connecter à Git, choisir ce dépôt, sans commande de build,
répertoire de sortie `public`. Chaque push sur `main` met alors le site à jour.
