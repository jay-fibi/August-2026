/**
 * jay-app.js
 * Jay Task 1 - Basic JavaScript entry point for the Jay web demo.
 */

import { jayCapitalize, jaySlugify, jayTruncate } from './jay-assets/js/utils/jay-string-utils.js';

const JAY_CONFIG_PATH = './jay-config.json';

/**
 * Load the Jay JSON configuration file.
 * @returns {Promise<Object>} parsed configuration object
 */
async function jayLoadConfig() {
  const response = await fetch(JAY_CONFIG_PATH);
  if (!response.ok) {
    throw new Error(`Jay config request failed with status ${response.status}`);
  }
  return response.json();
}

/**
 * Render the loaded configuration into the page.
 * @param {Object} config - the Jay configuration object
 */
function jayRenderConfig(config) {
  const titleEl = document.querySelector('#jay-app-title');
  const listEl = document.querySelector('#jay-feature-list');
  const statusEl = document.querySelector('#jay-status');

  if (titleEl) {
    titleEl.textContent = jayCapitalize(config.appName);
  }

  if (listEl) {
    listEl.innerHTML = '';
    config.features.forEach((feature) => {
      const item = document.createElement('li');
      item.className = 'jay-feature-item';
      item.dataset.jaySlug = jaySlugify(feature.name);
      item.textContent = `${feature.name} - ${jayTruncate(feature.description, 60)}`;
      listEl.appendChild(item);
    });
  }

  if (statusEl) {
    statusEl.textContent = `Jay loaded v${config.version} (${config.features.length} features)`;
    statusEl.classList.add('jay-status--ok');
  }
}

/**
 * Wire up the click counter button.
 */
function jayInitCounter() {
  const button = document.querySelector('#jay-counter-button');
  const output = document.querySelector('#jay-counter-output');
  let jayClickCount = 0;

  if (!button || !output) {
    return;
  }

  button.addEventListener('click', () => {
    jayClickCount += 1;
    output.textContent = `Jay clicks: ${jayClickCount}`;
  });
}

/**
 * Bootstrap the Jay application.
 */
async function jayMain() {
  jayInitCounter();

  try {
    const config = await jayLoadConfig();
    jayRenderConfig(config);
    console.log('Jay app initialised', config);
  } catch (error) {
    const statusEl = document.querySelector('#jay-status');
    if (statusEl) {
      statusEl.textContent = `Jay error: ${error.message}`;
      statusEl.classList.add('jay-status--error');
    }
    console.error('Jay app failed to initialise', error);
  }
}

document.addEventListener('DOMContentLoaded', jayMain);

export { jayLoadConfig, jayRenderConfig, jayInitCounter, jayMain };
