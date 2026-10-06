'use strict';

function el(tag, cls, text) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined) n.textContent = text;
  return n;
}

function card(t) {
  const c = el('article', 'card');

  const shots = el('div', 'shots');
  for (const [shot, alt] of [['wps', 'Now Playing screen'], ['menu', 'menu screen']]) {
    const img = el('img');
    img.loading = 'lazy';
    img.src = 'shots/' + t.dir + '-' + shot + '.png';
    img.alt = t.name + ' \u2014 ' + alt;
    img.width = 375; img.height = 320;
    shots.append(img);
  }
  c.append(shots);

  const body = el('div', 'card-body');
  body.append(el('div', 'name', t.name));
  body.append(el('div', 'byline', t.author));
  if (t.licence) body.append(el('div', 'licence', t.licence));

  const links = el('div', 'links');
  const dl = el('a', null, 'Download .zip');
  dl.href = 'zips/' + t.dir + '.zip';
  links.append(dl);
  if (t.source) {
    const src = el('a', null, 'Original theme');
    src.href = t.source;
    src.rel = 'noopener';
    links.append(src);
  }
  body.append(links);
  c.append(body);
  return c;
}

function matches(t, q) {
  return [t.name, t.dir, t.author, t.licence].join(' ').toLowerCase().includes(q);
}

fetch('themes.json')
  .then(r => r.json())
  .then(themes => {
    const grid = document.getElementById('grid');
    const count = document.getElementById('count');
    const search = document.getElementById('search');
    const all = themes.slice().sort((a, b) => a.name.localeCompare(b.name));

    function render() {
      const q = search.value.trim().toLowerCase();
      const shown = q ? all.filter(t => matches(t, q)) : all;
      grid.replaceChildren(...shown.map(card));
      if (!shown.length) grid.append(el('p', 'empty', 'No themes match.'));
      count.textContent = shown.length + ' of ' + all.length + ' themes';
    }
    search.addEventListener('input', render);
    render();
  });
