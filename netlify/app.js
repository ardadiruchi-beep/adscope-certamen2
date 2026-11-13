/* ADScope · Estación de trabajo (cliente de la API local) */

const $ = id => document.getElementById(id);
const state = {
  cases: [],            // worklist (GET /api/images)
  current: null,        // { filename, analysis }
  showHeat: true,
  showFoci: true,
  dsFilter: 'all',
  dsClass: '',
  osd: null,            // visor piramidal OpenSeadragon (para WSI)
  wsiHeatEl: null,
  fociEls: [],
  user: null,           // sesión actual ({username, name, role})
};

/* ==================== utilidades ==================== */
function toast(msg) {
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

async function api(url, opts = {}) {
  const r = await fetch(url, opts);
  if (r.status === 401) {
    const err = new Error('Autenticación requerida');
    err.status = 401;
    if (state.user) openLogin();  // sesión expirada: pedir re-login
    throw err;
  }
  if (!r.ok) {
    let detail = r.statusText;
    try { detail = (await r.json()).detail || (await r.json()).error || detail; } catch (e) {}
    throw new Error(detail);
  }
  return r.json();
}

function fmtPct(v) {
  return v == null ? '<span style="color:var(--dim);">—</span>' : (v * 100).toFixed(0) + '%';
}

/* ==================== autenticación ==================== */
function openLogin() { $('authModal').classList.add('open'); }
function closeLogin() { $('authModal').classList.remove('open'); }
$('authBtn').onclick = openLogin;
$('cancelLoginBtn').onclick = closeLogin;
$('loginBtn').onclick = doLogin;
$('loginPass').onkeydown = e => { if (e.key === 'Enter') doLogin(); };

async function doLogin() {
  try {
    const j = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: $('loginUser').value, password: $('loginPass').value }),
    });
    if (!j.ok) {
      let d = 'Credenciales inválidas';
      try { d = (await j.json()).detail || d; } catch (e) {}
      toast(d);
      return;
    }
    const data = await j.json();
    state.user = data.user;
    $('loginPass').value = '';
    closeLogin();
    renderAuth();
    toast('Sesión iniciada: ' + data.user.name);
    loadWorklist();
    loadDataset();
    loadAdmin();
  } catch (e) { toast(e.message); }
}

$('logoutBtn').onclick = async () => {
  try { await fetch('/api/auth/logout', { method: 'POST' }); } catch (e) {}
  state.user = null;
  window.location.href = 'login.html';
};

$('passBtn').onclick = async () => {
  const np = window.prompt('Nueva contraseña (mínimo 8 caracteres):');
  if (!np) return;
  try {
    await api('/api/auth/password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_password: np }),
    });
    toast('Contraseña actualizada');
  } catch (e) { toast('Error: ' + e.message); }
};

function renderAuth() {
  const logged = !!state.user;
  $('authBtn').classList.toggle('hidden', logged);
  $('userChip').classList.toggle('hidden', !logged);
  if (state.user) {
    $('userBadge').textContent = `${state.user.name} · ${state.user.role}`;
  }
  const isAdmin = state.user && state.user.role === 'admin';
  $('btnRetrain').classList.toggle('hidden', !isAdmin);
  $('adminPanel').style.display = isAdmin ? 'block' : 'none';
  loadDataset();
  renderWorklist();
}

async function loadAuth() {
  try {
    const r = await fetch('/api/auth/me');
    if (r.ok) {
      const j = await r.json();
      state.user = j.user;
      renderAuth();
      loadWorklist();
      loadAdmin();
      return;
    }
  } catch (e) {}
  // Sin sesión → landing de login
  window.location.href = 'login.html';
}

/* -- panel de administración (solo admin) -- */
async function loadAdmin() {
  if (!state.user || state.user.role !== 'admin') return;
  try {
    const users = await api('/api/users');
    $('usersList').innerHTML = '<b>Usuarios:</b><br>' + users.users.map(u =>
      `· ${u.username} (${u.name}) — ${u.role}`).join('<br>');
    const audit = await api('/api/audit');
    $('auditList').innerHTML = audit.events.length ? audit.events.map(e =>
      `<div style="margin-bottom:4px;">${e.ts.slice(0, 16).replace('T', ' ')} · <b>${e.username || '—'}</b> · ${e.action} · <span style="color:var(--dim);">${e.detail || ''}</span></div>`
    ).join('') : 'Sin eventos.';
  } catch (e) { /* silencio: panel solo si hay permisos */ }
}

$('btnCreateUser').onclick = async () => {
  try {
    await api('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: $('nuName').value,
        username: $('nuUser').value,
        password: $('nuPass').value,
        role: $('nuRole').value,
      }),
    });
    toast('Usuario creado');
    $('nuName').value = $('nuUser').value = $('nuPass').value = '';
    loadAdmin();
  } catch (e) { toast('Error: ' + e.message); }
};

$('exportLink').addEventListener('click', e => {
  if (!state.user) { e.preventDefault(); openLogin(); }
});
function go(section) {
  document.querySelectorAll('section.section').forEach(s => s.classList.remove('active'));
  $('section-' + section).classList.add('active');
  document.querySelectorAll('nav a').forEach(a => a.classList.toggle('active', a.dataset.nav === section));
  if (section === 'dataset') loadDataset();
  if (section === 'visor') loadWorklist();
  if (section === 'modelo') { loadHeadStatus(); }
  window.scrollTo({ top: 0 });
}
document.querySelectorAll('nav a').forEach(a => a.addEventListener('click', () => go(a.dataset.nav)));

/* ==================== worklist ==================== */
async function loadWorklist() {
  try {
    const j = await api('/api/images');
    state.cases = j.images;
    renderWorklist();
  } catch (e) {
    if (!state.user) {
      $('worklist').innerHTML = '<div class="viewer-empty" style="min-height:120px;">🔐 Inicia sesión para ver los casos.</div>';
    } else {
      toast('Error cargando worklist: ' + e.message);
    }
  }
}

function renderWorklist() {
  const wl = $('worklist');
  wl.innerHTML = '';
  if (!state.cases.length) {
    wl.innerHTML = '<div class="viewer-empty" style="min-height:120px;">Sin casos aún.<br>Sube la primera imagen.</div>';
    return;
  }
  state.cases.forEach(c => {
    const div = document.createElement('div');
    div.className = 'case' + (state.current && state.current.filename === c.filename ? ' selected' : '');
    const last = c.labels.length ? c.labels[c.labels.length - 1] : null;
    div.innerHTML = `
      <img src="/api/images/${c.filename}/thumb" alt="">
      <div class="case-info">
        <div class="case-name" title="${c.filename}">${c.filename}</div>
        <div class="case-meta">${last ? 'Último: ' + last.final_label : 'Sin etiqueta'} · ${c.labels.length} etiqueta${c.labels.length === 1 ? '' : 's'}</div>
        <span class="badge ${last ? (last.agreed ? 'b-green' : 'b-amber') : 'b-blue'}" style="margin-top:3px;">
          ${last ? (last.agreed ? '✓ concordante' : '✏️ corregida') : 'sin etiqueta'}
        </span>
      </div>`;
    div.onclick = () => selectCase(c.filename);
    wl.appendChild(div);
  });
}

/* ==================== carga / selección de caso ==================== */
async function selectCase(filename) {
  state.current = { filename, analysis: null };
  renderWorklist();
  resetViewer();
  $('caseLabels').innerHTML = '—';

  // etiquetas previas del caso
  const c = state.cases.find(x => x.filename === filename);
  if (c && c.labels.length) {
    $('caseLabels').innerHTML = c.labels.map(l =>
      `<div style="margin-bottom:6px;"><span style="color:${l.agreed ? 'var(--success)' : 'var(--warning)'};">
      ${l.agreed ? '✓' : '✏️'}</span> <b>${l.final_label}</b> · ${l.evaluator}<br>
      <span style="color:var(--dim);">${l.created_at || ''} · IA: ${l.ai_label || '—'}</span></div>`
    ).join('');
  }

  // análisis cacheado
  try {
    const a = await api('/api/analysis/' + encodeURIComponent(filename));
    showAnalysis(a);
  } catch (e) {
    $('viewerEmpty').classList.remove('hidden');
    $('viewerEmpty').innerHTML = `Caso <b>${filename}</b> sin análisis todavía.<br><br>
      <button class="btn btn-primary" onclick="reanalyze()">🔬 Analizar ahora</button>`;
  }
}

function resetViewer() {
  destroyOSD();
  $('baseImg').classList.add('hidden');
  $('heatImg').classList.add('hidden');
  $('fociLayer').innerHTML = '';
  $('aiLabel').textContent = '—';
  $('aiProb').textContent = '';
  $('fociList').innerHTML = '<li style="color:var(--dim);">Sin análisis.</li>';
  $('fociCount').textContent = '0';
  $('staleBadge').classList.add('hidden');
}

function destroyOSD() {
  if (state.osd) {
    try { state.osd.destroy(); } catch (e) {}
    state.osd = null;
    state.wsiHeatEl = null;
    state.fociEls = [];
  }
}

async function showAnalysis(a) {
  state.current.analysis = a;
  $('viewerEmpty').classList.add('hidden');

  if (a.wsi) showWSI(a); else showPlain(a);

  $('aiLabel').textContent = a.label || (a.head_trained ? '—' : '(sin cabeza entrenada)');
  let meta = 'confianza ' + ((a.prob ?? 0) * 100).toFixed(1) + '% · ' +
    (a.head_trained ? 'cabeza re-entrenada (3 clases)' : 'backbone placeholder (ImageNet)') +
    ' · analizado ' + (a.analyzed_at || '—');
  if (a.wsi) {
    meta = 'WSI ' + a.width + '×' + a.height + 'px · ' + (a.tile_count || 0) +
      ' tiles · ' + (a.mil_trained ? 'MIL con atención ✓' : 'MIL sin entrenar (media por tile)') +
      '<br>' + (a.magnification_note || '') + '<br>' + meta;
  }
  $('aiProb').innerHTML = meta;
  renderFociList(a);

  if (a.note) toast(a.note);

  // ¿análisis desactualizado respecto a la cabeza?
  let trainedAt = null;
  try { trainedAt = (await api('/api/model')).head?.trained_at || null; } catch (e) {}
  if (a.head_trained && trainedAt && a.analyzed_at && a.analyzed_at < trainedAt) {
    $('staleBadge').classList.remove('hidden');
  } else {
    $('staleBadge').classList.add('hidden');
  }
}

function showPlain(a) {
  destroyOSD();
  $('baseImg').src = a.image_url;
  $('baseImg').onload = buildFoci;
  $('baseImg').classList.remove('hidden');
  $('heatImg').src = 'data:image/png;base64,' + a.heatmap_overlay_png_base64;
  applyOverlayState();
}

function showWSI(a) {
  $('baseImg').classList.add('hidden');
  $('heatImg').classList.add('hidden');
  if (!state.osd) {
    state.osd = OpenSeadragon({
      id: 'viewer',
      prefixUrl: 'vendor/images/',
      showNavigator: false,
    });
  }
  state.osd.open(a.dzi);
  state.osd.clearOverlays();

  // heatmap: PNG RGBA estirado sobre toda la lámina (coordenadas en píxeles reales)
  if (a.heatmap_overlay_png_base64) {
    const img = document.createElement('img');
    img.src = 'data:image/png;base64,' + a.heatmap_overlay_png_base64;
    img.style.opacity = '0.55';
    state.osd.addOverlay({
      element: img,
      location: new OpenSeadragon.Rect(0, 0, a.width, a.height),
      placement: OpenSeadragon.Placement.TOP_LEFT,
    });
    state.wsiHeatEl = img;
  }

  // focos: anillos anclados a coordenadas de píxel real
  state.fociEls = [];
  const colors = ['#f6e05e', '#f6ad55', '#fc8181', '#9f7aea', '#68d391'];
  (a.foci || []).forEach((f, i) => {
    const div = document.createElement('div');
    div.className = 'foci-dot';
    div.style.borderColor = colors[i % 5];
    div.style.color = colors[i % 5];
    div.textContent = i + 1;
    state.osd.addOverlay({
      element: div,
      location: new OpenSeadragon.Rect(f.x - 15, f.y - 15, 30, 30),
    });
    state.fociEls.push(div);
  });
  state.osd.viewport.goHome(true);
  applyOverlayState();
}

function renderFociList(a) {
  const list = $('fociList');
  list.innerHTML = '';
  const colors = ['#f6e05e', '#f6ad55', '#fc8181', '#9f7aea', '#68d391'];
  if (!a.foci || !a.foci.length) {
    list.innerHTML = '<li style="color:var(--dim);">Sin focos.</li>';
    $('fociCount').textContent = '0';
    return;
  }
  a.foci.forEach((f, i) => {
    const li = document.createElement('li');
    li.innerHTML = `<span class="dot" style="background:${colors[i % 5]};"></span>
      <b>Foco ${i + 1}</b> score ${f.score} · (${f.x}, ${f.y}px)`;
    list.appendChild(li);
  });
  $('fociCount').textContent = a.foci.length;
}

async function reanalyze() {
  if (!state.current) return;
  try {
    const a = await api('/api/analyze/' + encodeURIComponent(state.current.filename), { method: 'POST' });
    showAnalysis(a);
    toast('Análisis actualizado');
  } catch (e) { toast('Error re-analizando: ' + e.message); }
}

/* ==================== focos / overlays ==================== */
function buildFoci() {
  const a = state.current && state.current.analysis;
  if (!a || !$('baseImg').naturalWidth) return;
  const list = $('fociList');
  list.innerHTML = '';
  const layer = $('fociLayer');
  layer.innerHTML = '';
  const colors = ['#f6e05e', '#f6ad55', '#fc8181', '#9f7aea', '#68d391'];
  a.foci.forEach((f, i) => {
    const li = document.createElement('li');
    li.innerHTML = `<span class="dot" style="background:${colors[i % 5]};"></span>
      <b>Foco ${i + 1}</b> score ${f.score} · (${f.x}, ${f.y}px)`;
    list.appendChild(li);
    const dot = document.createElement('div');
    dot.className = 'foci-dot';
    dot.style.left = (f.x / a.width * 100) + '%';
    dot.style.top = (f.y / a.height * 100) + '%';
    dot.style.borderColor = colors[i % 5];
    dot.style.color = colors[i % 5];
    dot.textContent = i + 1;
    layer.appendChild(dot);
  });
  $('fociCount').textContent = a.foci.length;
  $('fociLayer').classList.toggle('hidden', !state.showFoci);
}
window.addEventListener('resize', buildFoci);

$('btnHeat').onclick = () => {
  state.showHeat = !state.showHeat;
  applyOverlayState();
};
$('btnFoci').onclick = () => {
  state.showFoci = !state.showFoci;
  applyOverlayState();
};
$('btnReanalyze').onclick = reanalyze;

function applyOverlayState() {
  const a = state.current && state.current.analysis;
  if (!a) return;
  if (a.wsi) {
    if (state.wsiHeatEl) state.wsiHeatEl.style.display = state.showHeat ? '' : 'none';
    (state.fociEls || []).forEach(el => el.style.display = state.showFoci ? '' : 'none');
  } else {
    $('heatImg').classList.toggle('hidden', !state.showHeat);
    $('fociLayer').classList.toggle('hidden', !state.showFoci);
  }
  $('btnHeat').textContent = state.showHeat ? '🔥 Ocultar heatmap' : '🔥 Mostrar heatmap';
  $('btnFoci').textContent = state.showFoci ? '🎯 Ocultar focos' : '🎯 Mostrar focos';
}

/* ==================== upload ==================== */
const dz = $('dropzone');
dz.onclick = () => $('fileInput').click();
$('btnUpload').onclick = () => $('fileInput').click();
dz.ondragover = e => { e.preventDefault(); dz.classList.add('on'); };
dz.ondragleave = () => dz.classList.remove('on');
dz.ondrop = e => {
  e.preventDefault(); dz.classList.remove('on');
  uploadFiles([...e.dataTransfer.files]);
};
$('fileInput').onchange = e => uploadFiles([...e.target.files]);

async function uploadFiles(files) {
  if (!files.length) return;
  let last = null;
  for (const f of files) {
    const fd = new FormData();
    fd.append('imagen', f);
    dz.textContent = '⏳ Analizando ' + f.name + '…';
    try {
      const j = await api('/api/analizar', { method: 'POST', body: fd });
      last = j.image_id;
    } catch (e) { toast('Error con ' + f.name + ': ' + e.message); }
  }
  dz.textContent = 'o arrastra imágenes aquí (PNG/JPG/TIFF · WSI: SVS/NDPI/MRXS)';
  await loadWorklist();
  if (last) { selectCase(last); toast('Imagen(es) analizada(s)'); }
}

/* ==================== etiquetado ==================== */
async function guardar(agreed) {
  const a = state.current && state.current.analysis;
  if (!a) { toast('Analiza primero la imagen'); return; }
  const body = {
    image_id: a.image_id,
    ai_label: a.label || '(sin cabeza entrenada)',
    ai_prob: a.prob ?? 0,
    final_label: agreed ? (a.label || $('finalLabel').value) : $('finalLabel').value,
    agreed: agreed,
    evaluator: $('evaluator').value || 'Anónimo',
    role: 'Patólogo',
    turn: 'Turno 1 · Mañana',
    notes: '',
    foci: a.foci,
  };
  try {
    await api('/api/etiqueta', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    toast(agreed ? 'Diagnóstico confirmado · etiqueta añadida' : 'Corrección guardada · la IA aprenderá de este caso');
    await loadWorklist();
    selectCase(a.image_id);
  } catch (e) { toast('Error guardando: ' + e.message); }
}
$('btnConfirm').onclick = () => guardar(true);
$('btnCorrect').onclick = () => guardar(false);

/* ==================== dataset ==================== */
async function loadDataset() {
  try {
    const j = await api('/api/dataset');
    $('dsTotal').textContent = j.stats.total;
    $('dsConc').textContent = j.stats.concordancia_pct === null ? '—' : j.stats.concordancia_pct + '%';
    $('dsCorr').textContent = j.stats.correcciones;
    renderDataset(j.labels);
  } catch (e) {
    if (!state.user) {
      $('dsTable').innerHTML = '<tr><td colspan="8" style="color:var(--dim);">🔐 Inicia sesión para ver el dataset.</td></tr>';
    }
  }
}

function renderDataset(labels) {
  const tb = $('dsTable');
  let rows = [...labels].reverse();
  if (state.dsFilter === 'agreed') rows = rows.filter(l => l.agreed);
  if (state.dsFilter === 'corrected') rows = rows.filter(l => !l.agreed);
  if (state.dsClass) rows = rows.filter(l => l.final_label === state.dsClass);
  if (!rows.length) {
    tb.innerHTML = '<tr><td colspan="8" style="color:var(--dim);">Sin etiquetas con este filtro.</td></tr>';
    return;
  }
  tb.innerHTML = '';
  const isAdmin = state.user && state.user.role === 'admin';
  rows.forEach(l => {
    const tr = document.createElement('tr');
    tr.className = 'row';
    tr.innerHTML = `
      <td><b>${l.id}</b></td>
      <td>${l.image_id.slice(0, 10)}…</td>
      <td>${l.ai_label}${l.ai_prob != null ? ' (' + (l.ai_prob * 100).toFixed(0) + '%)' : ''}</td>
      <td><b>${l.final_label}</b></td>
      <td>${l.agreed ? '<span style="color:var(--success);">✓</span>' : '<span style="color:var(--warning);">✏️</span>'}</td>
      <td>${l.evaluator}</td>
      <td>${(l.created_at || '').slice(0, 10)}</td>
      <td>${isAdmin ? `<button class="btn btn-sm btn-danger" data-del="${l.id}">🗑</button>` : ''}</td>`;
    const delBtn = tr.querySelector('[data-del]');
    if (delBtn) {
      delBtn.onclick = async e => {
        e.stopPropagation();
        if (!confirm('¿Borrar esta etiqueta del dataset?')) return;
        try {
          await api('/api/dataset/' + l.id, { method: 'DELETE' });
          toast('Etiqueta borrada');
          loadDataset();
          loadWorklist();
        } catch (err) { toast('Error: ' + err.message); }
      };
    }
    tb.appendChild(tr);
  });
}

document.querySelectorAll('.filter-row [data-filter]').forEach(btn => {
  btn.onclick = () => {
    state.dsFilter = btn.dataset.filter;
    loadDataset();
  };
});
$('filterClass').onchange = e => { state.dsClass = e.target.value; loadDataset(); };

/* ==================== modelo ==================== */
async function loadHeadStatus() {
  try {
    const j = await api('/api/model');
    if (j.head && j.head.trained) {
      $('headStatus').textContent = 'Cabeza entrenada ✓';
      $('headStatus').className = 'badge b-green';
      if (j.head.evaluacion) renderEval(j.head.evaluacion);
    } else {
      $('headStatus').textContent = 'Cabeza sin entrenar (≥2 clases)';
      $('headStatus').className = 'badge b-amber';
    }
  } catch (e) {
    $('headStatus').textContent = 'sin conexión con el backend';
    $('headStatus').className = 'badge b-red';
  }
}

$('btnRetrain').onclick = async () => {
  const btn = $('btnRetrain');
  btn.disabled = true;
  btn.textContent = 'Re-entrenando…';
  try {
    const j = await api('/api/model/retrain', { method: 'POST' });
    if (j.ok) {
      $('headStatus').textContent = `Cabeza lista: ${j.samples} muestras · loss ${j.final_loss}`;
      $('headStatus').className = 'badge b-green';
      renderEval(j.evaluacion);
      toast('Cabeza re-entrenada');
    } else {
      $('headStatus').textContent = 'No re-entrenado: ' + (j.error || '');
      $('headStatus').className = 'badge b-red';
    }
  } catch (e) { toast('Error: ' + e.message); }
  btn.disabled = false;
  btn.textContent = '🔁 Re-entrenar cabeza con el dataset';
};

function renderEval(ev) {
  const panel = $('evalPanel');
  if (!ev || !ev.test) {
    panel.style.display = 'block';
    $('evalBody').innerHTML = '<span style="color:var(--warning); font-size:13px;">⚠️ ' +
      ((ev && ev.motivo) || 'Sin evaluación: datos insuficientes.') + '</span>';
    return;
  }
  const t = ev.test;
  const gap = (ev.train && t.accuracy != null) ? (ev.train.accuracy - t.accuracy) : null;
  let html = '<div style="font-size:13px; margin-bottom:10px;">' +
    '<b>Test:</b> n=' + t.n + ' · exactitud <b style="color:var(--success);">' +
    (t.accuracy != null ? (t.accuracy * 100).toFixed(0) + '%' : '—') + '</b>' +
    ' · train ' + (ev.train ? (ev.train.accuracy * 100).toFixed(0) + '% (n=' + ev.train.n + ')' : '—');
  if (gap != null && gap > 0.15) {
    html += ' · <b style="color:var(--danger);">posible sobreajuste (gap +' + (gap * 100).toFixed(0) + 'pp)</b>';
  }
  html += '<br><small style="color:var(--dim);">' + ev.metodo + '</small></div>';
  html += '<table><thead><tr><th>Clase</th><th>Precisión</th><th>Sensibilidad</th><th>F1</th><th>TP/FP/FN</th></tr></thead><tbody>';
  t.per_class.forEach(p => {
    html += '<tr><td><b>' + p.class + '</b></td><td>' + fmtPct(p.precision) + '</td><td>' +
      fmtPct(p.sensibilidad_recall) + '</td><td>' + fmtPct(p.f1) + '</td>' +
      '<td style="color:var(--dim);">' + p.tp + '/' + p.fp + '/' + p.fn + '</td></tr>';
  });
  html += '</tbody></table>';
  $('evalBody').innerHTML = html;
  panel.style.display = 'block';
}

/* ==================== init ==================== */
(async function init() {
  try {
    const h = await api('/api/health');
    $('apiStatus').textContent = 'API OK ✓ (' + h.backend + ')';
    $('apiStatus').className = 'badge b-green';
  } catch (e) {
    $('apiStatus').textContent = 'API sin conexión';
    $('apiStatus').className = 'badge b-red';
  }
  loadAuth();
  loadHeadStatus();
})();
