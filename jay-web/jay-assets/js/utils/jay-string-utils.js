/**
 * jay-string-utils.js
 * Jay Task 5 - Utility module inside a nested directory structure
 * (jay-web/jay-assets/js/utils/).
 */

/**
 * Capitalize the first letter of every word in a string.
 * @param {string} value
 * @returns {string}
 */
export function jayCapitalize(value) {
  if (typeof value !== 'string' || value.length === 0) {
    return '';
  }
  return value
    .split(' ')
    .map((word) => (word ? word.charAt(0).toUpperCase() + word.slice(1) : word))
    .join(' ');
}

/**
 * Convert a string into a URL-friendly slug.
 * @param {string} value
 * @returns {string}
 */
export function jaySlugify(value) {
  if (typeof value !== 'string') {
    return '';
  }
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

/**
 * Truncate a string to a maximum length, appending an ellipsis when cut.
 * @param {string} value
 * @param {number} [maxLength=40]
 * @returns {string}
 */
export function jayTruncate(value, maxLength = 40) {
  if (typeof value !== 'string') {
    return '';
  }
  if (value.length <= maxLength) {
    return value;
  }
  return `${value.slice(0, Math.max(0, maxLength - 3)).trimEnd()}...`;
}

/**
 * Reverse the characters of a string.
 * @param {string} value
 * @returns {string}
 */
export function jayReverse(value) {
  if (typeof value !== 'string') {
    return '';
  }
  return [...value].reverse().join('');
}

export default { jayCapitalize, jaySlugify, jayTruncate, jayReverse };
