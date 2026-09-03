/* ============================================================
   HTML Learning Hub — shared application script
   Features: signup / login / logout, per-user progress that is
   saved on logout, and live HTML editors for every demo.
   NOTE: This is a client-side demo — localStorage auth is NOT
   secure for real-world use. Fine for a learning sandbox.
   ============================================================ */
(function () {
  'use strict';

  var LS_KEY = 'htmlHubData_v1';
  var TOTAL_LESSONS = 20;

  /* ---------------- Data layer (localStorage) ---------------- */

  function defaultData() {
    return { users: {}, guest: [], currentUser: null };
  }

  function load() {
    try {
      var d = JSON.parse(localStorage.getItem(LS_KEY));
      return d && typeof d === 'object' ? d : defaultData();
    } catch (e) {
      return defaultData();
    }
  }

  function save() {
    try {
      localStorage.setItem(LS_KEY, JSON.stringify(data));
    } catch (e) { /* storage unavailable (private mode) */ }
  }

  var data = load();

  function hash(str) {
    var h = 5381;
    for (var i = 0; i < str.length; i++) {
      h = ((h << 5) + h + str.charCodeAt(i)) >>> 0;
    }
    return 'h' + h.toString(36);
  }

  /* ---------------- Auth ---------------- */

  function signup(username, password) {
    username = (username || '').trim();
    if (!username) return { ok: false, error: 'Please enter a username.' };
    if (!password || password.length < 4) {
      return { ok: false, error: 'Password must be at least 4 characters.' };
    }
    if (data.users[username]) return { ok: false, error: 'That username is already taken.' };
    data.users[username] = { pass: hash(password), progress: [] };
    data.currentUser = username;
    save();
    return { ok: true };
  }

  function login(username, password) {
    username = (username || '').trim();
    var user = data.users[username];
    if (!user || user.pass !== hash(password || '')) {
      return { ok: false, error: 'Invalid username or password.' };
    }
    data.currentUser = username;
    save();
    return { ok: true };
  }

  /* Logout explicitly persists the current user's progress
     before switching to the guest session. */
  function logout() {
    if (data.currentUser) save();
    data.currentUser = null;
    save();
  }

  function currentUser() { return data.currentUser; }

  /* ---------------- Progress ---------------- */

  function currentProgress() {
    return data.currentUser ? data.users[data.currentUser].progress : data.guest;
  }

  function setCurrentProgress(list) {
    if (data.currentUser) data.users[data.currentUser].progress = list;
    else data.guest = list;
  }

  function isComplete(n) { return currentProgress().indexOf(n) !== -1; }

  function toggleLesson(n) {
    var p = currentProgress();
    var i = p.indexOf(n);
    if (i === -1) p.push(n); else p.splice(i, 1);
    setCurrentProgress(p);
    save();
  }

  function completedCount() { return currentProgress().length; }

  /* ---------------- Small DOM helpers ---------------- */

  function byId(id) { return document.getElementById(id); }
  function debounce(fn, ms) {
    var t;
    return function () {
      clearTimeout(t);
      t = setTimeout(fn, ms);
    };
  }

  /* ---------------- Auth area + modal UI ---------------- */

  var modalHTML =
    '<div class="modal-overlay" id="auth-modal" hidden>' +
      '<div class="modal">' +
        '<button type="button" class="modal-close" id="auth-close" aria-label="Close">&times;</button>' +
        '<div class="modal-brand">&lt;/&gt; HTML Learning Hub</div>' +
        '<h2 id="auth-title">Welcome back</h2>' +
        '<p class="auth-sub" id="auth-sub">Login to keep your lesson progress in sync.</p>' +
        '<form id="auth-form" novalidate>' +
          '<label class="field"><span>Username</span>' +
          '<input id="auth-username" type="text" autocomplete="username" required></label>' +
          '<label class="field"><span>Password</span>' +
          '<input id="auth-password" type="password" autocomplete="current-password" required></label>' +
          '<p class="auth-error" id="auth-error" hidden></p>' +
          '<button type="submit" class="btn btn-primary btn-block" id="auth-submit">Login</button>' +
        '</form>' +
        '<p class="auth-switch" id="auth-switch">New here? ' +
          '<a href="#" id="auth-switch-link">Create a free account</a></p>' +
        '<p class="auth-note">Demo mode: accounts &amp; progress live only in this browser (localStorage).</p>' +
      '</div>' +
    '</div>';

  var authMode = 'login'; // 'login' | 'signup'

  function renderAuthArea() {
    var area = byId('auth-area');
    if (!area) return;
    var user = currentUser();
    if (user) {
      area.innerHTML =
        '<span class="user-chip" title="Signed in as ' + user + '">👤 <b>' + user + '</b></span>' +
        '<button type="button" class="btn btn-ghost btn-sm" id="auth-logout-btn">Logout</button>';
      byId('auth-logout-btn').addEventListener('click', function () {
        logout();
        renderAuthArea();
        refreshProgressUI();
        refreshLessonPage();
      });
    } else {
      area.innerHTML =
        '<span class="guest-chip">Guest · progress saved locally</span>' +
        '<button type="button" class="btn btn-ghost btn-sm" id="auth-login-btn">Login</button>' +
        '<button type="button" class="btn btn-primary btn-sm" id="auth-signup-btn">Sign up</button>';
      byId('auth-login-btn').addEventListener('click', function () { openAuthModal('login'); });
      byId('auth-signup-btn').addEventListener('click', function () { openAuthModal('signup'); });
    }
  }


  function openAuthModal(mode) {
    authMode = mode;
    var overlay = byId('auth-modal');
    if (!overlay) return;
    byId('auth-title').textContent = mode === 'signup' ? 'Create your account' : 'Welcome back';
    byId('auth-sub').textContent = mode === 'signup'
      ? 'Sign up and your progress will be saved to your account.'
      : 'Login to keep your lesson progress in sync.';
    byId('auth-submit').textContent = mode === 'signup' ? 'Create account' : 'Login';
    byId('auth-switch-link').textContent = mode === 'signup' ? 'I already have an account' : 'Create a free account';
    byId('auth-username').value = '';
    byId('auth-password').value = '';
    byId('auth-error').hidden = true;
    overlay.hidden = false;
    setTimeout(function () { byId('auth-username').focus(); }, 50);
    byId('auth-form').onsubmit = onAuthSubmit;
    byId('auth-switch-link').onclick = function (e) {
      e.preventDefault();
      openAuthModal(authMode === 'signup' ? 'login' : 'signup');
    };
  }

  function closeAuthModal() {
    var overlay = byId('auth-modal');
    if (overlay) overlay.hidden = true;
  }

  function onAuthSubmit(e) {
    e.preventDefault();
    var result = authMode === 'signup'
      ? signup(byId('auth-username').value, byId('auth-password').value)
      : login(byId('auth-username').value, byId('auth-password').value);
    if (!result.ok) {
      var err = byId('auth-error');
      err.textContent = result.error;
      err.hidden = false;
      return;
    }
    closeAuthModal();
    renderAuthArea();
    refreshProgressUI();
    refreshLessonPage();
  }

  /* ---------------- Home page progress UI ---------------- */

  function refreshProgressUI() {
    var count = byId('progress-count');
    var fill = byId('progress-fill');
    var note = byId('progress-note');
    var badge = byId('badge-progress');
    var done = completedCount();
    var pct = Math.round((done / TOTAL_LESSONS) * 100);
    if (count) count.textContent = done + ' / ' + TOTAL_LESSONS + ' lessons complete';
    if (fill) fill.style.width = pct + '%';
    if (note) {
      note.textContent = done === 0
        ? 'Welcome! Progress lives per-account — create a free account and start ticking lessons off.'
        : done === TOTAL_LESSONS
        ? 'You finished the whole course — amazing! 🎉'
        : 'You have completed ' + done + ' of ' + TOTAL_LESSONS + ' lessons so far.';
    }
    if (badge) badge.textContent = pct + '% Complete';

    document.querySelectorAll('.card[data-lesson]').forEach(function (card) {
      var n = parseInt(card.getAttribute('data-lesson'), 10);
      var doneFlag = isComplete(n);
      card.classList.toggle('is-complete', doneFlag);
      var state = card.querySelector('.card-state');
      if (state) {
        state.textContent = doneFlag ? '✔ Complete' : 'Not started';
        state.classList.toggle('done', doneFlag);
      }
    });
  }

  /* ---------------- Lesson page completion button ---------------- */

  function refreshLessonPage() {
    var header = document.querySelector('.lesson-header[data-lesson]');
    if (!header) return;
    var n = parseInt(header.getAttribute('data-lesson'), 10);
    var btn = byId('toggle-complete');
    var status = byId('lesson-status');
    var done = isComplete(n);
    if (btn) {
      btn.textContent = done ? 'Completed ✓' : 'Mark as Complete';
      btn.classList.toggle('is-done', done);
    }
    if (status) {
      status.textContent = done ? 'Completed ✓' : 'Not completed yet';
      status.classList.toggle('is-done', done);
    }
    if (btn && !btn._bound) {
      btn._bound = true;
      btn.addEventListener('click', function () {
        toggleLesson(n);
        refreshLessonPage();
      });
    }
  }

  /* ---------------- Live HTML editor (demo boxes) ---------------- */

  function initLiveEditors() {
    document.querySelectorAll('.demo-box').forEach(function (box) {
      if (box._leInit) return;
      box._leInit = true;

      var label = box.querySelector('.demo-label');
      var labelHtml = label ? label.outerHTML : '';

      // Everything except the label becomes the editable source.
      var parts = [];
      Array.prototype.forEach.call(box.childNodes, function (node) {
        if (label && node === label) return;
        if (node.nodeType === 3 && node.textContent.trim() === '') return;
        parts.push(node.nodeType === 1 ? node.outerHTML : node.textContent);
      });
      var initialCode = parts.join('\n').trim();

      box.innerHTML =
        labelHtml +
        '<div class="live-editor">' +
          '<div class="le-toolbar">' +
            '<span class="le-hint">✏️ Live editor — change the HTML below and watch the preview update</span>' +
            '<button type="button" class="le-btn" data-le-action="reset">↺ Reset</button>' +
          '</div>' +
          '<div class="le-preview" data-le-preview></div>' +
          '<textarea class="le-code" data-le-code spellcheck="false" ' +
            'aria-label="Editable HTML source of this demo"></textarea>' +
        '</div>';

      var preview = box.querySelector('[data-le-preview]');
      var code = box.querySelector('[data-le-code]');
      code.value = initialCode;

      function render() {
        preview.innerHTML = code.value;
        // Keep demo forms from actually navigating away.
        preview.querySelectorAll('form').forEach(function (f) {
          f.addEventListener('submit', function (ev) { ev.preventDefault(); });
        });
        if (window.__afterLiveRender) window.__afterLiveRender(preview);
      }

      function reset() {
        code.value = initialCode;
        render();
      }

      // Generic dialog wiring so re-rendered dialogs stay usable.
      preview.addEventListener('click', function (e) {
        var d = preview.querySelector('#demo-dialog');
        if (!d) return;
        if (e.target.id === 'open-dialog' && d.showModal) d.showModal();
        if (e.target.id === 'close-dialog' && d.close) d.close();
      });

      box.querySelector('[data-le-action="reset"]').addEventListener('click', reset);
      code.addEventListener('input', debounce(render, 350));

      render();
    });
  }

  /* ---------------- Boot ---------------- */

  function init() {
    if (!byId('auth-modal')) {
      var host = document.body;
      var holder = document.createElement('div');
      holder.innerHTML = modalHTML;
      host.appendChild(holder.firstChild);
    }
    var closeBtn = byId('auth-close');
    var overlay = byId('auth-modal');
    if (closeBtn) closeBtn.addEventListener('click', closeAuthModal);
    if (overlay) overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeAuthModal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay && !overlay.hidden) closeAuthModal();
    });

    renderAuthArea();
    refreshProgressUI();
    refreshLessonPage();
    initLiveEditors();
  }

  document.addEventListener('DOMContentLoaded', init);
})();

