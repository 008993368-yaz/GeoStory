/**
 * Test utility for rendering components with React Router context.
 * 
 * Many components use useSearchParams, Link, and other router hooks,
 * so we need to wrap them in a MemoryRouter for tests.
 */

import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { MemoryRouter, MemoryRouterProps } from 'react-router-dom';

interface RenderWithRouterOptions extends Omit<RenderOptions, 'wrapper'> {
  /** Initial route entries for MemoryRouter */
  initialEntries?: MemoryRouterProps['initialEntries'];
  /** Initial index for MemoryRouter */
  initialIndex?: number;
}

/**
 * Render a component wrapped in MemoryRouter for testing.
 * 
 * @example
 * ```tsx
 * const { getByText } = renderWithRouter(<Home />, {
 *   initialEntries: ['/?category=travel'],
 * });
 * ```
 */
export function renderWithRouter(
  ui: ReactElement,
  options: RenderWithRouterOptions = {}
) {
  const { initialEntries = ['/'], initialIndex, ...renderOptions } = options;

  return render(ui, {
    wrapper: ({ children }) => (
      <MemoryRouter initialEntries={initialEntries} initialIndex={initialIndex}>
        {children}
      </MemoryRouter>
    ),
    ...renderOptions,
  });
}

export * from '@testing-library/react';
