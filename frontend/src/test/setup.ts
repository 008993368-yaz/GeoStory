/**
 * Vitest test setup
 * 
 * This file runs before each test file to set up the test environment.
 */

import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

// Stub Calcite web components so they don't crash React Testing Library.
// We only need the DOM elements to exist - we don't need the actual Calcite runtime.
const calciteElements = [
  'calcite-shell',
  'calcite-shell-panel',
  'calcite-panel',
  'calcite-button',
  'calcite-input',
  'calcite-input-message',
  'calcite-label',
  'calcite-loader',
  'calcite-notice',
  'calcite-select',
  'calcite-option',
  'calcite-text-area',
  'calcite-icon',
  'calcite-action',
  'calcite-navigation',
  'calcite-navigation-logo',
];

// Register empty custom elements for calcite components
// This prevents "unknown element" errors in jsdom
calciteElements.forEach((tagName) => {
  if (!customElements.get(tagName)) {
    customElements.define(
      tagName,
      class extends HTMLElement {
        connectedCallback() {
          // Render slot content so children are visible
          if (!this.shadowRoot) {
            this.attachShadow({ mode: 'open' });
            this.shadowRoot!.innerHTML = '<slot></slot>';
          }
        }
      }
    );
  }
});

// Mock window.matchMedia for components that use media queries
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

