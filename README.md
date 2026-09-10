# The Bot Shop

A self-contained GitHub Pages prototype of a passive pixel-art shop populated by 10 bot characters.

## Publish on GitHub Pages

1. Create a repository, e.g. `the-bot-shop`.
2. Upload **all files and the entire `assets` folder** from this package to the repository root.
3. Go to **Settings → Pages**.
4. Choose **Deploy from a branch**.
5. Select `main` and `/(root)`.
6. Save.

Your repository root should look like:

```
index.html
style.css
script.js
README.md
assets/
  shop_bg.png
  bots/
  items/
  decor/
```

## How it works

- The shop is a real original pixel-art PNG background.
- Each bot is a separate transparent pixel sprite placed over that background.
- Bots move between predefined store zones on a timer.
- Objects have a hidden `peculiarity` value. Viewers never see it, but it influences bot choices.
- Each bot has its own preferences and permanent collection.
- New items appear automatically when an item is taken.
- State is stored in `localStorage`, so this prototype runs entirely on GitHub Pages with no backend.

## Important limitation

Each browser currently has its own simulation. The next architectural upgrade would be moving state to a shared backend so every viewer watches the same world and the bots continue shopping when nobody has the page open.
