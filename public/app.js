// Seventh OS — site : liste des applis (lue dans apps.json du hub, comme Seventh OS lui-même) et infos de la dernière version.
const REPO = 'se7enclaude/seventh-os';
const RAW = `https://raw.githubusercontent.com/${REPO}/main`;

// Copie de secours si GitHub ne répond pas (mêmes champs que apps.json).
const FALLBACK = [
  { id: "se7en-ia", name: "se7en IA", subtitle: "se7en studio · After Effects", accent: "#E9A19A", tagline: "Tes edits d'anime dans After Effects, en un clic." },
  { id: "se7en-download", name: "se7en Download", subtitle: "Télécharger · IA · Convertir · Découper · Lire", accent: "#F2564B", tagline: "Télécharge, améliore et convertis tes vidéos." },
  { id: "se7en-dualsense", name: "se7en DualSense", subtitle: "Ta manette PS5 sur PC", accent: "#D7F23A", tagline: "Ta DualSense dans tous tes jeux PC." },
  { id: "se7en-voice", name: "se7en Voice", subtitle: "Voix · Mixeur · Soundboard", accent: "#E6E7EB", tagline: "Change ta voix et gère tout le son de ton PC, au même endroit." },
  { id: "se7en-vision", name: "se7en Vision", subtitle: "Ton PC depuis ton iPhone", accent: "#7A64F0", tagline: "Contrôle ton PC depuis ton téléphone, où que tu sois." },
  { id: "se7en-clip", name: "se7en Clip", subtitle: "Clip farm · TikTok · Shorts · Reels", accent: "#22D3E6", tagline: "Une rediff de stream → tes meilleurs clips TikTok, tout seul." },
  { id: "se7en-autoclick", name: "se7en Autoclick", subtitle: "Autoclic · Macros", accent: "#3DFF8C", tagline: "Clique et rejoue tes gestes en boucle pour farmer." },
  { id: "se7en-censored", name: "se7en Censored", subtitle: "Floutage auto · Twitch", accent: "#F28B96", tagline: "Floute tout seul les parties intimes d'un film, uniquement là où il faut." },
];

const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };

function icon(app) {
  const img = el('img');
  img.alt = ''; img.loading = 'lazy'; img.width = 64; img.height = 64;
  img.src = `/assets/icons/${app.id}.png`;
  img.onerror = () => { img.onerror = null; img.src = `${RAW}/ui/icons/${app.id}.png`; }; // appli ajoutée après le site
  return img;
}

function card(app, isNew) {
  const c = el('article', 'app glass reveal');
  c.style.setProperty('--accent', app.accent || '#fff');
  if (isNew) c.append(el('span', 'badge', 'NOUVEAU'));
  const top = el('div', 'app-top');
  const names = el('div');
  names.append(el('h3', null, app.name), el('div', 'sub2', app.subtitle || ''));
  top.append(icon(app), names);
  c.append(top, el('p', 'tag', app.tagline || ''));
  if (app.features?.length) {
    const ul = el('ul');
    for (const f of app.features.slice(0, 4)) ul.append(el('li', null, f));
    c.append(ul);
  }
  if (app.requires) c.append(el('div', 'req', app.requires));
  return c;
}

function mock(apps) {
  const grid = document.getElementById('mock-grid');
  grid.replaceChildren();
  apps.slice(0, 6).forEach((app, i) => {
    const m = el('div', 'mock-card');
    const img = icon(app); img.width = img.height = 34; img.loading = 'eager';
    const [cls, txt] = i === 1 ? ['up', 'Mise à jour'] : i < 4 ? ['', 'Installé'] : ['off', 'Installer'];
    const state = el('i', cls, txt);
    m.append(img, el('b', null, app.name), state);
    grid.append(m);
  });
}

function render(apps) {
  // les plus récentes en premier dans le catalogue (fin de apps.json = dernière ajoutée)
  const ordered = [...apps].reverse();
  const box = document.getElementById('apps');
  box.replaceChildren(...ordered.map((a, i) => card(a, i === 0)));
  mock(ordered);
  document.querySelectorAll('[data-count]').forEach((n) => { n.textContent = apps.length; });
  observe();
}

async function loadApps() {
  try {
    const r = await fetch(`${RAW}/apps.json`, { cache: 'no-cache' });
    if (!r.ok) throw new Error(r.status);
    const data = await r.json();
    if (Array.isArray(data.apps) && data.apps.length) render(data.apps);
  } catch { /* la copie de secours reste affichée */ }
}

async function loadRelease() {
  try {
    const r = await fetch('/api/latest');
    if (!r.ok) throw new Error(r.status);
    const { version, size, url } = await r.json();
    const mo = Math.round(size / 1048576);
    document.querySelectorAll('[data-dlmeta]').forEach((n) => { n.textContent = `Version ${version} · ${mo} Mo · Windows 10/11`; });
    if (url) document.querySelectorAll('.dl-link').forEach((a) => { a.href = url; });
  } catch { /* /download redirige quand même vers la dernière version */ }
}

// apparition au défilement
let io;
function observe() {
  if (!('IntersectionObserver' in window)) { document.querySelectorAll('.reveal').forEach((n) => n.classList.add('in')); return; }
  io ??= new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal:not(.in)').forEach((n) => io.observe(n));
}

const nav = document.querySelector('.nav');
addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 10), { passive: true });
document.getElementById('year').textContent = new Date().getFullYear();
document.querySelectorAll('.steps li, .perk, .faq details, .final, .section-head').forEach((n) => n.classList.add('reveal'));

render(FALLBACK);
loadApps();
loadRelease();
