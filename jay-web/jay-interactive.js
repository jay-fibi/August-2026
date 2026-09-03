/**
 * jay-interactive.js
 * Jay Task 1 - Behaviour for the Jay interactive test page (jay-interactive.html).
 *
 * Wires up:
 *   - a click counter button (browser step: click)
 *   - live echo of typed input (browser step: type)
 *   - form submit handling with validation (browser step: submit)
 *   - scroll depth reporting (browser step: scroll)
 */

import { jayCapitalize, jaySlugify } from './jay-assets/js/utils/jay-string-utils.js';

/**
 * Wire up the click counter button and its reset companion.
 */
function jayInitClickButton() {
  const button = document.querySelector('#jay-action-button');
  const resetButton = document.querySelector('#jay-reset-button');
  const output = document.querySelector('#jay-click-output');
  const log = document.querySelector('#jay-click-log');
  let jayClickCount = 0;

  if (!button || !output || !log) {
    return;
  }

  button.addEventListener('click', () => {
    jayClickCount += 1;
    output.textContent = `Jay clicks: ${jayClickCount}`;
    output.dataset.jayClicks = String(jayClickCount);
    log.textContent = `Jay button clicked ${jayClickCount} time(s)`;
    log.classList.add('jay-status--ok');
  });

  if (resetButton) {
    resetButton.addEventListener('click', () => {
      jayClickCount = 0;
      output.textContent = 'Jay clicks: 0';
      output.dataset.jayClicks = '0';
      log.textContent = 'Jay button never clicked';
      log.classList.remove('jay-status--ok');
    });
  }
}

/**
 * Echo the name and email fields back to the page as the user types.
 */
function jayInitLiveEcho() {
  const nameInput = document.querySelector('#jay-name-input');
  const emailInput = document.querySelector('#jay-email-input');
  const echo = document.querySelector('#jay-live-echo');

  if (!nameInput || !emailInput || !echo) {
    return;
  }

  const jayUpdateEcho = () => {
    const name = nameInput.value.trim();
    const email = emailInput.value.trim();

    if (!name && !email) {
      echo.textContent = 'Jay typed nothing yet';
      echo.removeAttribute('data-jay-slug');
      return;
    }

    echo.textContent = `Jay typing: ${jayCapitalize(name) || '(no name)'} <${email || 'no-email'}>`;
    echo.dataset.jaySlug = jaySlugify(`${name} ${email}`);
  };

  nameInput.addEventListener('input', jayUpdateEcho);
  emailInput.addEventListener('input', jayUpdateEcho);
}

/**
 * Validate the Jay signup form.
 * @param {Object} values - collected form values
 * @returns {string[]} list of human readable problems (empty when valid)
 */
function jayValidate(values) {
  const problems = [];

  if (!values.jayName) {
    problems.push('Jay name is required');
  }
  if (!values.jayEmail.includes('@')) {
    problems.push('Jay email must contain @');
  }
  if (!values.jayRole) {
    problems.push('Jay role must be selected');
  }
  if (!values.jayTerms) {
    problems.push('Jay terms must be accepted');
  }

  return problems;
}

/**
 * Handle form submission entirely on the client (no server round trip).
 */
function jayInitFormSubmit() {
  const form = document.querySelector('#jay-signup-form');
  const result = document.querySelector('#jay-form-result');
  const message = document.querySelector('#jay-form-message');
  const valueList = document.querySelector('#jay-form-values');
  const errorEl = document.querySelector('#jay-form-error');
  let jaySubmitCount = 0;

  if (!form || !result || !message || !valueList || !errorEl) {
    return;
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const data = new FormData(form);
    const values = {
      jayName: String(data.get('jayName') || '').trim(),
      jayEmail: String(data.get('jayEmail') || '').trim(),
      jayRole: String(data.get('jayRole') || '').trim(),
      jayNotes: String(data.get('jayNotes') || '').trim(),
      jayTerms: data.get('jayTerms') === 'on',
    };

    const problems = jayValidate(values);

    if (problems.length > 0) {
      result.hidden = true;
      errorEl.hidden = false;
      errorEl.textContent = `Jay validation failed: ${problems.join('; ')}`;
      form.dataset.jaySubmitState = 'invalid';
      return;
    }

    jaySubmitCount += 1;
    errorEl.hidden = true;
    errorEl.textContent = '';

    valueList.innerHTML = '';
    Object.entries(values).forEach(([key, value]) => {
      const term = document.createElement('dt');
      term.className = 'jay-value-key';
      term.textContent = key;

      const definition = document.createElement('dd');
      definition.className = 'jay-value-item';
      definition.dataset.jayField = key;
      definition.textContent = String(value);

      valueList.append(term, definition);
    });

    message.textContent = `Jay form submitted successfully for ${jayCapitalize(values.jayName)}`;
    message.classList.add('jay-status--ok');
    result.hidden = false;
    form.dataset.jaySubmitState = 'submitted';
    form.dataset.jaySubmitCount = String(jaySubmitCount);

    console.log('Jay form submitted', values);
  });
}

/**
 * Report window scroll position and depth percentage into the page.
 */
function jayInitScrollTracker() {
  const readout = document.querySelector('#jay-scroll-readout');
  const sentinel = document.querySelector('#jay-scroll-sentinel');

  if (!readout) {
    return;
  }

  const jayUpdateScroll = () => {
    const scrollY = Math.round(window.scrollY);
    const scrollable = Math.max(
      1,
      document.documentElement.scrollHeight - window.innerHeight,
    );
    const depth = Math.min(100, Math.round((scrollY / scrollable) * 100));

    readout.textContent = `Jay scrollY: ${scrollY} (depth ${depth}%)`;
    readout.dataset.jayScrollY = String(scrollY);
    readout.dataset.jayScrollDepth = String(depth);
    document.body.dataset.jayMaxScroll = String(
      Math.max(Number(document.body.dataset.jayMaxScroll || 0), scrollY),
    );

    if (sentinel && depth >= 90) {
      sentinel.classList.add('jay-sentinel--seen');
      sentinel.dataset.jaySeen = 'true';
    }
  };

  window.addEventListener('scroll', jayUpdateScroll, { passive: true });
  jayUpdateScroll();
}

/**
 * Bootstrap the Jay interactive page.
 */
function jayMain() {
  jayInitClickButton();
  jayInitLiveEcho();
  jayInitFormSubmit();
  jayInitScrollTracker();

  document.body.dataset.jayReady = 'true';
  console.log('Jay interactive page initialised');
}

document.addEventListener('DOMContentLoaded', jayMain);

export {
  jayInitClickButton,
  jayInitLiveEcho,
  jayInitFormSubmit,
  jayInitScrollTracker,
  jayValidate,
  jayMain,
};
