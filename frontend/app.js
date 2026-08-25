/* =========================================================
   app.js — GenoPredict AD v4 · Enhanced UX
   ========================================================= */

// ── State ─────────────────────────────────────────────────
let fatherData = null, motherData = null;
let gaugeChart = null, histChart = null;

const PAGE_TITLES = {1:'Accueil',2:'Importation ADN',3:'Paramètres Cliniques',4:'Résultats'};
const CRITICAL_SNPS = ['rs429358','rs7412','rs3851179'];

// ══════════════════════════════════════════════════════════
//  TOAST NOTIFICATION SYSTEM
// ══════════════════════════════════════════════════════════
function showToast(message, type='info', duration=4000) {
  const container = document.getElementById('toast-container');
  const icons = {success:'✅', warning:'⚠️', info:'ℹ️'};
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span class="toast-icon">${icons[type]||'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('hide');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// ══════════════════════════════════════════════════════════
//  ANIMATED NUMBER COUNTER
// ══════════════════════════════════════════════════════════
function animateNumber(el, endVal, duration=800, suffix='') {
  const start = parseFloat(el.textContent) || 0;
  const diff = endVal - start;
  const startTime = performance.now();
  function tick(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // ease out quad
    const ease = 1 - (1 - progress) * (1 - progress);
    const current = start + diff * ease;
    if(Number.isInteger(endVal)) el.textContent = Math.round(current) + suffix;
    else el.textContent = current.toFixed(1) + suffix;
    if(progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// ══════════════════════════════════════════════════════════
//  CONFETTI CELEBRATION
// ══════════════════════════════════════════════════════════
function launchConfetti() {
  const container = document.getElementById('confetti');
  container.innerHTML = '';
  const colors = ['#10b981','#34d399','#3b82f6','#60a5fa','#f59e0b','#fbbf24','#8b5cf6','#a78bfa','#ef4444','#f87171'];
  for(let i = 0; i < 60; i++) {
    const piece = document.createElement('div');
    piece.className = 'confetti-piece';
    piece.style.left = Math.random() * 100 + '%';
    piece.style.background = colors[Math.floor(Math.random() * colors.length)];
    piece.style.width  = (6 + Math.random() * 8) + 'px';
    piece.style.height = (6 + Math.random() * 8) + 'px';
    piece.style.animationDuration = (2 + Math.random() * 3) + 's';
    piece.style.animationDelay    = (Math.random() * 1.5) + 's';
    piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
    container.appendChild(piece);
  }
  setTimeout(() => container.innerHTML = '', 6000);
}

// ══════════════════════════════════════════════════════════
//  SLIDER TRACK FILL
// ══════════════════════════════════════════════════════════
function updateSliderTrack(slider) {
  const min = parseFloat(slider.min), max = parseFloat(slider.max), val = parseFloat(slider.value);
  const pct = ((val - min) / (max - min)) * 100;
  slider.style.setProperty('--val', pct + '%');
}

// ══════════════════════════════════════════════════════════
//  NAVIGATION
// ══════════════════════════════════════════════════════════
let currentStep = 1;

function goToStep(n) {
  if(n === currentStep) return;
  currentStep = n;

  // Scroll to top of content
  document.getElementById('content')?.scrollTo({top:0, behavior:'smooth'});
  window.scrollTo({top:0, behavior:'smooth'});

  // Hide all, show target with slide animation
  document.querySelectorAll('.step-page').forEach(p => {
    p.classList.add('hidden');
    p.style.animation = 'none';
  });
  const target = document.getElementById(`step-${n}`);
  if(target) {
    target.classList.remove('hidden');
    // Force reflow to restart animation
    void target.offsetWidth;
    target.style.animation = 'slideIn .35s cubic-bezier(.22,1,.36,1) forwards';
  }

  // Topbar
  document.getElementById('page-title').textContent = PAGE_TITLES[n];
  document.getElementById('breadcrumb-page').textContent = PAGE_TITLES[n];

  // Step tracker (topbar)
  document.querySelectorAll('.step-track-item').forEach((el, i) => {
    el.classList.remove('active','done-track');
    const circle = el.querySelector('.track-circle');
    if(i+1 < n)  { el.classList.add('done-track'); circle.innerHTML = '<svg viewBox="0 0 16 16" fill="currentColor" width="12"><path d="M13.485 3.929a.75.75 0 010 1.06l-6.75 6.75a.75.75 0 01-1.06 0l-3.375-3.375a.75.75 0 011.06-1.06L6.2 10.108l6.22-6.22a.75.75 0 011.06 0z"/></svg>'; }
    if(i+1 === n){ el.classList.add('active'); circle.innerHTML = `<span>${i+1}</span>`; }
    if(i+1 > n)  { circle.innerHTML = `<span>${i+1}</span>`; }
  });
  document.querySelectorAll('.track-line').forEach((l, i) => {
    l.classList.toggle('done', i+1 < n);
  });

  // Sidebar nav
  document.querySelectorAll('.nav-btn').forEach((b, i) => {
    b.classList.toggle('active', i+1 === n);
  });
}

// ══════════════════════════════════════════════════════════
//  AGE SLIDER
// ══════════════════════════════════════════════════════════
const ageRange = document.getElementById('age-range');
const ageBig   = document.getElementById('age-big');
const noteBar  = document.getElementById('risk-note-bar');
const noteText = document.getElementById('risk-note-text');
const sumAge   = document.getElementById('sum-age');
const noteWrap = document.querySelector('.risk-age-note');

function updateAge(v) {
  ageBig.textContent = v;
  if(sumAge) {
    sumAge.textContent = v + ' ans';
    sumAge.classList.add('flash');
    setTimeout(() => sumAge.classList.remove('flash'), 400);
  }

  // Dynamic risk note
  if(v < 65) {
    noteBar.style.cssText = 'width:8px;height:8px;border-radius:50%;background:#10b981';
    noteText.textContent  = 'Risque faible — horizon temporel court.';
    noteWrap.style.cssText = 'padding:10px 14px;border-radius:8px;border:1px solid;display:flex;align-items:center;gap:10px;font-size:12px;background:#ecfdf5;border-color:#a7f3d0;color:#047857';
  } else if(v < 80) {
    noteBar.style.cssText = 'width:8px;height:8px;border-radius:50%;background:#f59e0b';
    noteText.textContent  = 'Risque modéré — surveillance médicale recommandée.';
    noteWrap.style.cssText = 'padding:10px 14px;border-radius:8px;border:1px solid;display:flex;align-items:center;gap:10px;font-size:12px;background:#fffbeb;border-color:#fef3c7;color:#92400e';
  } else {
    noteBar.style.cssText = 'width:8px;height:8px;border-radius:50%;background:#ef4444';
    noteText.textContent  = 'Risque élevé — âge avancé, vigilance accrue nécessaire.';
    noteWrap.style.cssText = 'padding:10px 14px;border-radius:8px;border:1px solid;display:flex;align-items:center;gap:10px;font-size:12px;background:#fef2f2;border-color:#fee2e2;color:#991b1b';
  }

  // Update slider track fill
  updateSliderTrack(ageRange);
}

if(ageRange) {
  ageRange.addEventListener('input', e => updateAge(parseInt(e.target.value)));
  updateAge(75);
  updateSliderTrack(ageRange);
}

// ══════════════════════════════════════════════════════════
//  SEX SELECTOR → LIVE SUMMARY
// ══════════════════════════════════════════════════════════
const sumSex = document.getElementById('sum-sex');
document.querySelectorAll('input[name="sex"]').forEach(r => {
  r.addEventListener('change', e => {
    const map = {mixed:'Mixte', female:'Filles', male:'Garçons'};
    if(sumSex) {
      sumSex.textContent = map[e.target.value];
      sumSex.classList.add('flash');
      setTimeout(() => sumSex.classList.remove('flash'), 400);
    }
    showToast(`Sexe sélectionné : <strong>${map[e.target.value]}</strong>`, 'info', 2000);
  });
});

// ══════════════════════════════════════════════════════════
//  FAMILY HISTORY TOGGLE
// ══════════════════════════════════════════════════════════
const fhToggle = document.getElementById('fh-toggle');
const fhImpact = document.getElementById('fh-impact');
const sumFh    = document.getElementById('sum-fh');
if(fhToggle) {
  fhToggle.addEventListener('change', e => {
    fhImpact?.classList.toggle('hidden', !e.target.checked);
    if(sumFh) {
      sumFh.textContent = e.target.checked ? 'Oui (+15 pts)' : 'Non';
      sumFh.classList.add('flash');
      setTimeout(() => sumFh.classList.remove('flash'), 400);
    }
    if(e.target.checked) {
      showToast('Antécédents familiaux activés : +15 points de risque', 'warning', 3500);
    }
  });
}

// ══════════════════════════════════════════════════════════
//  FILE UPLOAD
// ══════════════════════════════════════════════════════════
function processParsedData(rows, fileName, isFather) {
  const dot  = document.getElementById(isFather ? 'dot-father'  : 'dot-mother');
  const idle = document.getElementById(isFather ? 'drop-idle-father' : 'drop-idle-mother');
  const ok   = document.getElementById(isFather ? 'drop-ok-father'   : 'drop-ok-mother');
  const fnEl = document.getElementById(isFather ? 'fname-father'     : 'fname-mother');
  const fcEl = document.getElementById(isFather ? 'fcount-father'    : 'fcount-mother');
  const mkEl = document.getElementById(isFather ? 'markers-father'   : 'markers-mother');
  const chips= document.getElementById(isFather ? 'chips-father'     : 'chips-mother');
  const box  = document.getElementById(isFather ? 'box-father'       : 'box-mother');

  const valid = rows.length>0 && 'rsID' in rows[0] && 'GT' in rows[0];
  if(valid) {
    if(isFather) fatherData = rows; else motherData = rows;
    
    // Visual success
    dot.className = 'box-status-dot ready';
    idle.classList.add('hidden');
    ok.classList.remove('hidden');
    ok.style.display = 'flex';
    fnEl.textContent = fileName;
    fcEl.textContent = rows.length + ' variants chargés';

    // Subtle border glow on the box
    box.style.borderColor = '#10b981';
    box.style.boxShadow = '0 0 0 3px rgba(16,185,129,.08), 0 4px 20px rgba(16,185,129,.1)';

    // Show detected markers
    const rsIds = rows.map(r => r.rsID);
    mkEl.style.display = 'block';
    chips.innerHTML = CRITICAL_SNPS.map(s =>
      `<span class="mc-chip ${rsIds.includes(s)?'found':'missing'}">${rsIds.includes(s)?'✓ ':'✗ '}${s}</span>`
    ).join('');

    // Toast
    const who = isFather ? 'Père' : 'Mère';
    const found = CRITICAL_SNPS.filter(s => rsIds.includes(s)).length;
    showToast(`Profil ${who} chargé — ${rows.length} variants, ${found}/3 marqueurs détectés`, 'success', 3500);

    checkBothUploaded();
  } else {
    showToast('Format invalide — colonnes rsID et GT requises.', 'warning', 4000);
  }
}

function setupUpload(dzId, inputId, isFather) {
  const dz   = document.getElementById(dzId);
  const inp  = document.getElementById(inputId);

  ['dragenter','dragover'].forEach(e => dz.addEventListener(e, ev => { ev.preventDefault(); dz.classList.add('dragging'); }));
  ['dragleave','drop'].forEach(e => dz.addEventListener(e, ev => { ev.preventDefault(); dz.classList.remove('dragging'); }));
  dz.addEventListener('drop', ev => { const f = ev.dataTransfer.files[0]; if(f) parseFile(f); });
  inp.addEventListener('change', ev => { const f = ev.target.files[0]; if(f) parseFile(f); });

  function parseFile(file) {
    Papa.parse(file, {
      header:true, skipEmptyLines:true,
      complete(res) {
        processParsedData(res.data, file.name, isFather);
      }
    });
  }
}

function checkBothUploaded() {
  const btn   = document.getElementById('btn-upload-next');
  const alert = document.getElementById('apoe-alert');
  const ready = fatherData && motherData;
  if(btn) btn.disabled = !ready;
  if(ready && alert) {
    const fRs = fatherData.map(r => r.rsID);
    const hasAPOE = fRs.includes('rs429358') && fRs.includes('rs7412');
    alert.classList.toggle('hidden', !hasAPOE);
    if(hasAPOE) {
      showToast('Les deux profils contiennent les marqueurs APOE — analyse haute précision activée.', 'success', 4000);
    }
  }
}

setupUpload('da-father','in-father', true);
setupUpload('da-mother','in-mother', false);

async function loadDemoFiles() {
  try {
    const [fatherRes, motherRes] = await Promise.all([
      fetch('/demo_data/father_genotype.csv'),
      fetch('/demo_data/mother_genotype.csv')
    ]);
    if(!fatherRes.ok || !motherRes.ok) throw new Error("Fichiers introuvables");

    const fatherCsv = await fatherRes.text();
    const motherCsv = await motherRes.text();

    Papa.parse(fatherCsv, { header:true, skipEmptyLines:true, complete(res) { processParsedData(res.data, "father_genotype_test.csv", true); } });
    Papa.parse(motherCsv, { header:true, skipEmptyLines:true, complete(res) { processParsedData(res.data, "mother_genotype_test.csv", false); } });

    showToast("Fichiers de test prêts.", "success");
  } catch (err) {
    showToast("Erreur lors du chargement des fichiers de test.", "warning");
    console.error(err);
  }
}

// ══════════════════════════════════════════════════════════
//  SIMULATION
// ══════════════════════════════════════════════════════════
async function runSimulation() {
  goToStep(4);
  document.getElementById('loading-view').style.display  = 'flex';
  document.getElementById('results-view').classList.add('hidden');

  // Reset load steps
  document.querySelectorAll('.load-step').forEach(s => {
    s.classList.remove('done');
    s.querySelector('.ls-check').textContent = '○';
  });

  const steps = [
    [10, 'Initialisation du moteur mendélien…', 'ls-1'],
    [35, 'Génération de 1 000 enfants virtuels…', 'ls-2'],
    [70, 'Inférence par le modèle Random Forest…', 'ls-3'],
    [95, 'Compilation du rapport final…', 'ls-4'],
  ];

  const setProgress = pct => { document.getElementById('load-bar').style.width = pct+'%'; };
  const setMsg      = msg => { document.getElementById('load-msg').textContent = msg; };
  const completeLs  = id  => {
    const el = document.getElementById(id);
    if(el) { el.classList.add('done'); el.querySelector('.ls-check').textContent = '✓'; }
  };

  let delay = 0;
  steps.forEach(([pct, msg, lsId]) => {
    delay += 1200;
    setTimeout(() => { setProgress(pct); setMsg(msg); completeLs(lsId); }, delay);
  });

  const sexVal  = document.querySelector('input[name="sex"]:checked')?.value || 'mixed';
  const sexOpts = sexVal==='mixed'?[0,1]:sexVal==='male'?[1]:[0];

  const body = {
    father_data:    fatherData,
    mother_data:    motherData,
    age:            parseInt(document.getElementById('age-range')?.value || 75),
    sex_opts:       sexOpts,
    family_history: document.getElementById('fh-toggle')?.checked ? 1 : 0
  };

  try {
    const res  = await fetch('/api/simulate', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(body)
    });
    if(!res.ok) throw new Error('Erreur serveur ' + res.status);
    const data = await res.json();

    setTimeout(() => {
      setProgress(100);
      setMsg('Analyse terminée !');
      setTimeout(() => {
        renderResults(data);
        launchConfetti();
        showToast('Analyse génomique complète — les résultats sont prêts.', 'success', 5000);
      }, 600);
    }, delay + 300);

  } catch(err) {
    setMsg('❌ ' + err.message);
    document.getElementById('load-msg').style.color = '#ef4444';
    showToast(err.message, 'warning', 6000);
    console.error(err);
  }
}

// ══════════════════════════════════════════════════════════
//  RESULTS RENDERING
// ══════════════════════════════════════════════════════════
function renderResults(data) {
  document.getElementById('loading-view').style.display = 'none';
  const rv = document.getElementById('results-view');
  rv.classList.remove('hidden');

  const score = data.global_score;

  // Risk level
  let level, bannerCls, pillColor, pillText, interpHTML, gaugeGlow;
  if(score < 30) {
    level='Faible'; bannerCls='low'; gaugeGlow='glow-green';
    pillColor='background:#d1fae5;color:#047857'; pillText='Faible';
    interpHTML=`<p>Le score de risque polygénique moyen calculé sur <strong>1 000 simulations</strong> est de <strong>${score.toFixed(1)}%</strong>.</p><br>
    <p>La combinaison génétique simulée pour la descendance de ce couple est <strong style="color:#047857">globalement favorable</strong>. Le risque est inférieur à la moyenne de la population pour cet âge de référence. Une surveillance de routine et un mode de vie sain restent toutefois conseillés.</p>`;
  } else if(score < 60) {
    level='Modéré'; bannerCls='mod'; gaugeGlow='glow-amber';
    pillColor='background:#fef3c7;color:#92400e'; pillText='Modéré';
    interpHTML=`<p>Le score de risque polygénique moyen est de <strong>${score.toFixed(1)}%</strong>.</p><br>
    <p>Certains variants génétiques à risque sont présents dans la descendance simulée. Une <strong style="color:#92400e">surveillance médicale régulière</strong> et l'adoption d'un mode de vie préventif (alimentation, exercice, stimulation cognitive) sont fortement conseillés.</p>`;
  } else {
    level='Élevé'; bannerCls='high'; gaugeGlow='glow-red';
    pillColor='background:#fee2e2;color:#991b1b'; pillText='Élevé';
    interpHTML=`<p>Le score de risque polygénique moyen est de <strong>${score.toFixed(1)}%</strong>.</p><br>
    <p>Les simulations révèlent une <strong style="color:#991b1b">forte pénétrance des variants à risque</strong> (notamment l'allèle APOE ε4). Une consultation auprès d'un <strong>généticien médical</strong> est fortement recommandée. Des mesures préventives intensives peuvent significativement retarder l'apparition des symptômes.</p>`;
  }

  // Risk banner
  const banner = document.getElementById('risk-banner');
  banner.className = 'risk-banner ' + bannerCls;
  document.getElementById('rb-label').textContent = 'Score de risque moyen · ' + level;
  document.getElementById('rb-interpretation').innerHTML = interpHTML;

  // Animated score on banner
  animateNumber(document.getElementById('rb-score'), score, 1000, '%');

  // Gauge card glow
  const gaugeCard = document.querySelector('.card-gauge');
  gaugeCard.className = 'dash-card card-gauge ' + gaugeGlow;

  // Gauge pill
  const gPill = document.getElementById('gauge-pill');
  gPill.textContent = pillText;
  gPill.setAttribute('style', pillColor + ';padding:3px 10px;border-radius:99px;font-size:11px;font-weight:700');

  // Animated numbers
  animateNumber(document.getElementById('g-score'), score, 1000, '%');
  document.getElementById('g-level').textContent = level.toUpperCase();

  // Metrics with animated counters
  const high     = data.high_risk_count;
  const apoe_pct = data.p_apoe_cc;
  const pi_pct   = data.p_picalm_cc;

  animateNumber(document.getElementById('rb-high'), high, 800, '');
  animateNumber(document.getElementById('m-high'), high, 800, '');
  animateNumber(document.getElementById('m-apoe'), apoe_pct, 900, '%');
  animateNumber(document.getElementById('m-picalm'), pi_pct, 900, '%');

  // Metric bars (delayed for smooth animation)
  setTimeout(() => {
    document.getElementById('bar-high').style.width   = Math.min(high/10, 100) + '%';
    document.getElementById('bar-apoe').style.width   = Math.min(apoe_pct, 100) + '%';
    document.getElementById('bar-picalm').style.width = Math.min(pi_pct, 100) + '%';
  }, 200);

  // Interpretation
  document.getElementById('interp-content').innerHTML = interpHTML;

  // Subtitle
  document.getElementById('results-subtitle').textContent =
    `Basé sur 1 000 simulations mendéliennes · Risque ${level.toLowerCase()} détecté (${score.toFixed(1)}%)`;

  renderGauge(score);
  renderHist(data.histogram);
}

// ══════════════════════════════════════════════════════════
//  CHARTS
// ══════════════════════════════════════════════════════════
function renderGauge(score) {
  const ctx = document.getElementById('cGauge').getContext('2d');
  if(gaugeChart) gaugeChart.destroy();

  let col = '#10b981';
  if(score >= 30) col = '#f59e0b';
  if(score >= 60) col = '#ef4444';

  gaugeChart = new Chart(ctx, {
    type:'doughnut',
    data:{ datasets:[{
      data:[score, 100-score],
      backgroundColor:[col,'#f3f4f6'],
      borderWidth:0,
      circumference:180,
      rotation:-90,
      hoverOffset:0,
    }]},
    options:{
      responsive:true, maintainAspectRatio:false,
      cutout:'78%',
      animation:{duration:1200, easing:'easeInOutQuart'},
      plugins:{ tooltip:{enabled:false}, legend:{display:false} }
    }
  });
}

function renderHist(hist) {
  const ctx = document.getElementById('cHist').getContext('2d');
  if(histChart) histChart.destroy();

  const colors = hist.bins.map(b => {
    const p = b*100;
    if(p < 30) return 'rgba(16,185,129,.75)';
    if(p < 60) return 'rgba(245,158,11,.75)';
    return 'rgba(239,68,68,.75)';
  });
  const hoverColors = hist.bins.map(b => {
    const p = b*100;
    if(p < 30) return 'rgba(16,185,129,.95)';
    if(p < 60) return 'rgba(245,158,11,.95)';
    return 'rgba(239,68,68,.95)';
  });

  histChart = new Chart(ctx, {
    type:'bar',
    data:{
      labels: hist.bins.map(b => (b*100).toFixed(0)+'%'),
      datasets:[{
        label:'Enfants virtuels',
        data: hist.counts,
        backgroundColor: colors,
        hoverBackgroundColor: hoverColors,
        borderRadius:6,
        borderSkipped:false,
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false,
      animation:{duration:900, easing:'easeOutQuart'},
      plugins:{
        legend:{display:false},
        tooltip:{
          backgroundColor:'#1f2937',
          titleFont:{family:'Inter', weight:600},
          bodyFont:{family:'Inter'},
          padding:12,
          cornerRadius:8,
          callbacks:{
            title: ctx => 'Risque ~ ' + ctx[0].label,
            label: ctx => '  ' + ctx.parsed.y + ' enfants virtuels',
          }
        }
      },
      scales:{
        x:{
          grid:{display:false},
          ticks:{font:{size:11,family:'Inter',weight:500},color:'#9ca3af',maxRotation:0}
        },
        y:{
          grid:{color:'#f3f4f6',drawBorder:false},
          ticks:{font:{size:11,family:'Inter'},color:'#9ca3af'},
          beginAtZero:true
        }
      }
    }
  });
}

// ══════════════════════════════════════════════════════════
//  SMOOTH SCROLL for "Comment ça marche"
// ══════════════════════════════════════════════════════════
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if(target) {
      e.preventDefault();
      target.scrollIntoView({behavior:'smooth', block:'start'});
    }
  });
});

// ══════════════════════════════════════════════════════════
//  KEYBOARD SHORTCUTS
// ══════════════════════════════════════════════════════════
document.addEventListener('keydown', e => {
  // Alt+1..4 to navigate steps
  if(e.altKey && e.key >= '1' && e.key <= '4') {
    e.preventDefault();
    goToStep(parseInt(e.key));
  }
});

// ══════════════════════════════════════════════════════════
//  INIT
// ══════════════════════════════════════════════════════════
goToStep(1);
// Welcome toast after 800ms
setTimeout(() => {
  showToast('Bienvenue sur GenoPredict AD — votre outil d\'analyse génomique.', 'info', 4000);
}, 800);
