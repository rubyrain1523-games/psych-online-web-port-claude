(function() {
  // ---------- tiny store-only zip writer ----------
  var crcT = (function() { var t = [], c, n, k; for (n = 0; n < 256; n++) { c = n; for (k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  function crc32(u) { var c = 0xFFFFFFFF; for (var i = 0; i < u.length; i++) c = crcT[(c ^ u[i]) & 255] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }
  function makeZip(files) {
    var enc = new TextEncoder(), parts = [], central = [], off = 0;
    files.forEach(function(f) {
      var nm = enc.encode(f.name), crc = crc32(f.data), h = new DataView(new ArrayBuffer(30));
      h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint16(6, 0x0800, true); h.setUint16(8, 0, true);
      h.setUint16(10, 0, true); h.setUint16(12, 0x21, true); h.setUint32(14, crc, true);
      h.setUint32(18, f.data.length, true); h.setUint32(22, f.data.length, true); h.setUint16(26, nm.length, true); h.setUint16(28, 0, true);
      parts.push(new Uint8Array(h.buffer), nm, f.data);
      var c = new DataView(new ArrayBuffer(46));
      c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint16(8, 0x0800, true);
      c.setUint16(12, 0, true); c.setUint16(14, 0x21, true); c.setUint32(16, crc, true);
      c.setUint32(20, f.data.length, true); c.setUint32(24, f.data.length, true); c.setUint16(28, nm.length, true); c.setUint32(42, off, true);
      central.push(new Uint8Array(c.buffer), nm);
      off += 30 + nm.length + f.data.length;
    });
    var csize = 0; central.forEach(function(x) { csize += x.length; });
    var e = new DataView(new ArrayBuffer(22));
    e.setUint32(0, 0x06054b50, true); e.setUint16(8, files.length, true); e.setUint16(10, files.length, true);
    e.setUint32(12, csize, true); e.setUint32(16, off, true);
    return new Blob(parts.concat(central, [new Uint8Array(e.buffer)]), { type: 'application/zip' });
  }
  function slug(s) { return (s || '').trim().replace(/[^A-Za-z0-9 _-]/g, '').replace(/\s+/g, '-').toLowerCase(); }
  function bytes(file) { return file.arrayBuffer().then(function(b) { return new Uint8Array(b); }); }
  function ext(f) { var m = /\.([A-Za-z0-9]+)$/.exec(f.name); return m ? m[1].toLowerCase() : ''; }

  var STEP_H = 20, LANES = 8, LANE_W = 46, GUTTER = 56;
  var CSS = '#mm{position:fixed;inset:0;z-index:100000;background:#0b0b10;color:#fff;font:14px system-ui,sans-serif;display:flex;flex-direction:column;touch-action:pan-y;-webkit-user-select:text;user-select:text}' +
    '#mm *{box-sizing:border-box}#mm .bar{display:flex;gap:8px;align-items:center;padding:8px 12px;background:#16161f;border-bottom:1px solid #33334a;flex-wrap:wrap}' +
    '#mm .tabs button,#mm button.b{display:inline-block;width:auto;margin:0;padding:7px 12px;border-radius:8px;border:1px solid #33334a;background:#1d1d2b;color:#fff;cursor:pointer;font-size:14px}' +
    '#mm .tabs button.on{border-color:#7b6cff;background:#2a2550}#mm input,#mm select{background:#0f0f17;color:#fff;border:1px solid #33334a;border-radius:6px;padding:6px 8px;font-size:14px;max-width:100%}' +
    '#mm label{display:flex;flex-direction:column;font-size:12px;color:#a8a8b8;gap:3px}#mm .pane{flex:1;overflow:auto;padding:12px;display:none}#mm .pane.on{display:block}' +
    '#mm .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin-bottom:12px}' +
    '#mm .note{color:#ffb86b;font-size:13px;margin:6px 0}#mm table{border-collapse:collapse;width:100%}#mm td{padding:4px;border-bottom:1px solid #222}' +
    '#mm .ed{position:relative;overflow:auto;background:#0f0f17}#mm .ed canvas{position:sticky;top:0;left:0;display:block;touch-action:none}';
  var st = null;

  function open() {
    if (document.getElementById('mm')) return;
    var style = document.createElement('style'); style.id = 'mm-style'; style.textContent = CSS; document.head.appendChild(style);
    var root = document.createElement('div'); root.id = 'mm';
    root.innerHTML =
      '<div class="bar"><b>Mod Maker</b><span class="tabs"><button data-t="song" class="on">Song</button> <button data-t="skin">Re-skin / Assets</button> <button data-t="out">Save</button></span>' +
      '<span style="flex:1"></span><button class="b" id="mm-close">Close</button></div>' +
      '<div class="pane on" id="mm-song">' +
        '<div class="grid">' +
          '<label>Mod / song name<input id="mm-name" value="My Song"></label>' +
          '<label>BPM<input id="mm-bpm" type="number" value="120" min="40" max="300"></label>' +
          '<label>Scroll speed<input id="mm-speed" type="number" value="2" step="0.1" min="0.5" max="5"></label>' +
          '<label>Opponent<input id="mm-opp" value="dad"></label>' +
          '<label>Player<input id="mm-pl" value="bf"></label>' +
          '<label>Girlfriend<input id="mm-gf" value="gf"></label>' +
          '<label>Stage<input id="mm-stage" value="stage"></label>' +
          '<label>Instrumental (mp3/ogg/wav)<input id="mm-inst" type="file" accept="audio/*"></label>' +
          '<label>Vocals (optional)<input id="mm-voc" type="file" accept="audio/*"></label>' +
        '</div>' +
        '<div class="note">Chart: click a lane to add a note, click it again to remove, drag down to make a hold. The right 4 lanes are yours (player), the left 4 are the opponent\'s. Pick the instrumental first.</div>' +
        '<div class="bar" style="border:1px solid #33334a;border-radius:8px"><button class="b" id="mm-play">Play</button><label>Snap<select id="mm-snap"><option value="4">1/4 beat</option><option value="2" selected>1/2 beat</option><option value="1">1 beat</option></select></label>' +
          '<button class="b" id="mm-beats">Fill every beat</button><button class="b" id="mm-clear">Clear notes</button><span id="mm-info" style="color:#a8a8b8"></span></div>' +
        '<div class="ed" id="mm-ed" style="height:55vh;margin-top:8px"><canvas id="mm-cv"></canvas><div id="mm-sp"></div></div>' +
      '</div>' +
      '<div class="pane" id="mm-skin"><div class="note">Replace or add game files. Choose a file, then where it goes inside the mod (for sprite sheets upload the .png and its .xml with the same name). Examples: images/menuBG.png, images/NOTE_assets.png, images/characters/BOYFRIEND.png.</div>' +
        '<datalist id="mm-targets"><option value="images/menuBG.png"><option value="images/menuDesat.png"><option value="images/NOTE_assets.png"><option value="images/NOTE_assets.xml"><option value="images/characters/BOYFRIEND.png"><option value="images/characters/BOYFRIEND.xml"><option value="images/gfDanceTitle.png"><option value="images/logoBumpin.png"><option value="sounds/scrollMenu.ogg"><option value="music/freakyMenu.ogg"></datalist>' +
        '<table id="mm-rows"></table><button class="b" id="mm-addrow" style="margin-top:8px">+ Add file</button></div>' +
      '<div class="pane" id="mm-out"><div class="grid"><label>Description<input id="mm-desc" value="Made with the in-game Mod Maker"></label></div>' +
        '<button class="b" id="mm-dl">Download mod zip</button> <button class="b" id="mm-inst-btn">Install into the game now</button><div class="note" id="mm-msg"></div></div>';
    document.body.appendChild(root);
    var $ = function(i) { return root.querySelector('#' + i); };
    st = { notes: {}, dur: 0, audio: null, url: null };

    Array.prototype.forEach.call(root.querySelectorAll('.tabs button'), function(b) {
      b.onclick = function() {
        Array.prototype.forEach.call(root.querySelectorAll('.tabs button'), function(x) { x.classList.toggle('on', x === b); });
        ['song', 'skin', 'out'].forEach(function(t) { $('mm-' + t).classList.toggle('on', t === b.getAttribute('data-t')); });
        if (b.getAttribute('data-t') === 'song') layout();
      };
    });
    function close() { if (st.audio) st.audio.pause(); window.removeEventListener('resize', layout); root.remove(); style.remove(); st = null; }
    $('mm-close').onclick = function() { if (Object.keys(st.notes).length === 0 || confirm('Close the Mod Maker? Unsaved work will be lost.')) close(); };

    var ed = $('mm-ed'), cv = $('mm-cv'), sp = $('mm-sp'), ctx = cv.getContext('2d');
    function bpm() { return Math.max(40, parseFloat($('mm-bpm').value) || 120); }
    function stepMs() { return 60000 / bpm() / 4; }
    function totalSteps() { return Math.max(64, Math.ceil(st.dur * 1000 / stepMs()) + 16); }
    function layout() {
      if (!st || !ed.clientWidth) return;
      cv.width = Math.max(ed.clientWidth, GUTTER + LANES * LANE_W + 10); cv.height = ed.clientHeight;
      sp.style.height = (totalSteps() * STEP_H) + 'px'; sp.style.width = '1px'; sp.style.marginTop = (-cv.height) + 'px';
      draw();
    }
    function draw() {
      if (!st || !cv.width) return;
      var top = ed.scrollTop, h = cv.height, c = ctx;
      c.fillStyle = '#0f0f17'; c.fillRect(0, 0, cv.width, h);
      var s0 = Math.floor(top / STEP_H), s1 = Math.ceil((top + h) / STEP_H);
      for (var s = s0; s <= s1; s++) {
        var y = s * STEP_H - top;
        c.strokeStyle = s % 16 === 0 ? '#7b6cff' : s % 4 === 0 ? '#3a3a55' : '#1a1a28'; c.beginPath(); c.moveTo(GUTTER, y); c.lineTo(GUTTER + LANES * LANE_W, y); c.stroke();
        if (s % 4 === 0) { c.fillStyle = '#8a8aa0'; c.font = '11px system-ui'; c.fillText((s * stepMs() / 1000).toFixed(1) + 's', 4, y + 12); }
      }
      for (var l = 0; l <= LANES; l++) { c.strokeStyle = l === 4 ? '#7b6cff' : '#2a2a3a'; c.beginPath(); c.moveTo(GUTTER + l * LANE_W, 0); c.lineTo(GUTTER + l * LANE_W, h); c.stroke(); }
      var cols = ['#c24b99', '#00ffff', '#12fa05', '#f9393f'];
      Object.keys(st.notes).forEach(function(k) {
        var p = k.split('_'), s = +p[0], l = +p[1], len = st.notes[k], y = s * STEP_H - top;
        if (y < -STEP_H * (len + 1) || y > h) return;
        c.fillStyle = cols[l % 4];
        if (len > 0) { c.globalAlpha = .5; c.fillRect(GUTTER + l * LANE_W + LANE_W / 2 - 5, y + STEP_H / 2, 10, len * STEP_H); c.globalAlpha = 1; }
        c.fillRect(GUTTER + l * LANE_W + 3, y + 1, LANE_W - 6, STEP_H - 2);
      });
      if (st.audio) { var py = (st.audio.currentTime * 1000 / stepMs()) * STEP_H - top; c.strokeStyle = '#fff'; c.beginPath(); c.moveTo(GUTTER - 6, py); c.lineTo(GUTTER + LANES * LANE_W + 6, py); c.stroke(); }
      $('mm-info').textContent = Object.keys(st.notes).length + ' notes, ' + st.dur.toFixed(1) + 's';
    }
    ed.addEventListener('scroll', function() { requestAnimationFrame(draw); });
    $('mm-bpm').onchange = layout; $('mm-snap').onchange = layout;
    window.addEventListener('resize', layout);
    $('mm-inst').onchange = function() {
      var f = this.files[0]; if (!f) return;
      if (st.url) URL.revokeObjectURL(st.url);
      st.url = URL.createObjectURL(f); st.audio = new Audio(st.url);
      st.audio.onloadedmetadata = function() { st.dur = st.audio.duration || 0; layout(); };
      if ($('mm-name').value === 'My Song') $('mm-name').value = f.name.replace(/\.[^.]+$/, '');
    };
    $('mm-play').onclick = function() {
      var btn = this;
      if (!st.audio) { alert('Pick an instrumental first.'); return; }
      if (st.audio.paused) {
        st.audio.currentTime = Math.max(0, ed.scrollTop / STEP_H * stepMs() / 1000);
        st.audio.play(); btn.textContent = 'Pause';
        (function tick() { if (!st || st.audio.paused) { btn.textContent = 'Play'; return; } ed.scrollTop = Math.max(0, (st.audio.currentTime * 1000 / stepMs()) * STEP_H - cv.height / 2); draw(); requestAnimationFrame(tick); })();
      } else { st.audio.pause(); btn.textContent = 'Play'; }
    };
    $('mm-clear').onclick = function() { if (confirm('Remove all notes?')) { st.notes = {}; draw(); } };
    $('mm-beats').onclick = function() {
      var n = Math.floor(st.dur * 1000 / (stepMs() * 4));
      for (var b = 4; b < n; b++) st.notes[(b * 4) + '_' + (4 + (b % 4))] = 0;
      draw();
    };
    var drag = null;
    function pos(e) {
      var r = cv.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top + ed.scrollTop;
      var per = 4 / parseInt($('mm-snap').value);
      var s = Math.floor(y / STEP_H / per) * per, l = Math.floor((x - GUTTER) / LANE_W);
      return (l < 0 || l >= LANES || s < 0) ? null : { s: s, l: l, raw: Math.floor(y / STEP_H) };
    }
    cv.addEventListener('pointerdown', function(e) {
      var p = pos(e); if (!p) return; e.preventDefault();
      var k = p.s + '_' + p.l;
      if (st.notes[k] !== undefined) { delete st.notes[k]; draw(); return; }
      st.notes[k] = 0; drag = { k: k, s: p.s }; cv.setPointerCapture(e.pointerId); draw();
    });
    cv.addEventListener('pointermove', function(e) {
      if (!drag) return; var p = pos(e) || { raw: drag.s };
      st.notes[drag.k] = Math.max(0, p.raw - drag.s); draw();
    });
    cv.addEventListener('pointerup', function() { drag = null; });

    var rows = [];
    function addRow() {
      var tr = document.createElement('tr'), obj = { file: null };
      tr.innerHTML = '<td><input type="file"></td><td><input list="mm-targets" placeholder="images/menuBG.png" style="width:100%"></td><td><button class="b">x</button></td>';
      var ins = tr.querySelectorAll('input');
      ins[0].onchange = function() {
        obj.file = this.files[0] || null;
        if (obj.file && !ins[1].value) ins[1].value = (/\.(png|xml)$/i.test(obj.file.name) ? 'images/' : /\.(ogg|mp3|wav)$/i.test(obj.file.name) ? 'sounds/' : '') + obj.file.name;
      };
      obj.target = ins[1];
      tr.querySelector('button').onclick = function() { tr.remove(); rows.splice(rows.indexOf(obj), 1); };
      rows.push(obj); $('mm-rows').appendChild(tr);
    }
    $('mm-addrow').onclick = addRow; addRow();

    function build() {
      var name = $('mm-name').value.trim() || 'My Song', id = slug(name) || 'my-song';
      var files = [], enc = new TextEncoder(), top = id + '/', jobs = [];
      function add(p, d) { files.push({ name: top + p, data: d }); }
      var b = bpm(), sm = stepMs(), n = Object.keys(st.notes).length;
      var instF = $('mm-inst').files[0], vocF = $('mm-voc').files[0];
      if (n > 0 && !instF) return Promise.reject('Pick an instrumental for the song, or remove its notes.');
      if (instF) {
        var secs = Math.ceil(totalSteps() / 16), sections = [];
        for (var i = 0; i < secs; i++) sections.push({ sectionNotes: [], sectionBeats: 4, lengthInSteps: 16, mustHitSection: true, gfSection: false, bpm: b, changeBPM: false, altAnim: false });
        Object.keys(st.notes).forEach(function(k) {
          var p = k.split('_'), s = +p[0], l = +p[1];
          sections[Math.floor(s / 16)].sectionNotes.push([Math.round(s * sm), l, Math.round(st.notes[k] * sm)]);
        });
        sections.forEach(function(x) { x.sectionNotes.sort(function(a, c) { return a[0] - c[0]; }); });
        var opp = $('mm-opp').value || 'dad', pl = $('mm-pl').value || 'bf', gf = $('mm-gf').value || 'gf', stg = $('mm-stage').value || 'stage';
        var chart = { song: { song: name, notes: sections, events: [], bpm: b, needsVoices: !!vocF, speed: parseFloat($('mm-speed').value) || 2, player1: pl, player2: opp, gfVersion: gf, stage: stg, validScore: true } };
        add('data/' + id + '/' + id + '.json', enc.encode(JSON.stringify(chart)));
        add('weeks/' + id + '.json', enc.encode(JSON.stringify({ songs: [[name, opp, [146, 113, 253]]], weekCharacters: [opp, pl, gf], weekBackground: stg, storyName: name, weekBefore: 'tutorial', weekName: name, startUnlocked: true, hideStoryMode: true, hideFreeplay: false, difficulties: '' })));
        jobs.push(bytes(instF).then(function(d) { add('songs/' + id + '/Inst.' + ext(instF), d); }));
        if (vocF) jobs.push(bytes(vocF).then(function(d) { add('songs/' + id + '/Voices.' + ext(vocF), d); }));
      }
      rows.forEach(function(r) {
        if (!r.file) return;
        var t = r.target.value.trim().replace(/^\/+/, '').replace(/\.\./g, '');
        if (!t) return;
        jobs.push(bytes(r.file).then(function(d) { add(t, d); }));
      });
      return Promise.all(jobs).then(function() {
        if (!files.length) throw 'Nothing to save yet. Add a song with notes or at least one file.';
        add('pack.json', enc.encode(JSON.stringify({ name: name, description: $('mm-desc').value, restart: false, runsGlobally: false, color: [170, 0, 255] })));
        return { id: id, blob: makeZip(files) };
      });
    }
    $('mm-dl').onclick = function() {
      build().then(function(r) {
        var a = document.createElement('a'); a.href = URL.createObjectURL(r.blob); a.download = r.id + '.zip'; document.body.appendChild(a); a.click(); a.remove();
        $('mm-msg').textContent = 'Saved ' + r.id + '.zip. You can share it or load it with the Import mod button.';
      }, function(e) { $('mm-msg').textContent = String(e); });
    };
    $('mm-inst-btn').onclick = function() {
      if (!window.psychImportZip) { $('mm-msg').textContent = 'Installing works once the game has loaded in a Modded mode. Use Download instead.'; return; }
      build().then(function(r) { return bytes(r.blob).then(function(d) { window.psychImportZip(r.id + '.zip', d); $('mm-msg').textContent = 'Installed. Go back to the main menu and open Freeplay to find your song.'; }); },
        function(e) { $('mm-msg').textContent = String(e); });
    };
    layout();
  }
  window.psychOpenMaker = open;
})();
