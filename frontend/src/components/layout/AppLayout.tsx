import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';

interface AppLayoutProps {
  children: ReactNode;
}

function AppLayout({ children }: AppLayoutProps) {
  const location = useLocation();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <header
        style={{
          backgroundColor: 'var(--color-primary)',
          color: 'var(--color-text-on-primary)',
          padding: 'var(--spacing-md) var(--spacing-xl)',
          boxShadow: 'var(--shadow-md)',
        }}
      >
        <nav
          style={{
            maxWidth: '1200px',
            margin: '0 auto',
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--spacing-xl)',
          }}
        >
          <Link
            to="/"
            style={{
              fontSize: 'var(--font-size-xl)',
              fontWeight: 'var(--font-weight-bold)',
              color: 'var(--color-text-on-primary)',
              textDecoration: 'none',
            }}
          >
            GeoStory
          </Link>

          <div style={{ display: 'flex', gap: 'var(--spacing-lg)' }}>
            <Link
              to="/"
              style={{
                color: 'var(--color-text-on-primary)',
                textDecoration: 'none',
                fontWeight:
                  location.pathname === '/'
                    ? 'var(--font-weight-semibold)'
                    : 'var(--font-weight-normal)',
                opacity: location.pathname === '/' ? 1 : 0.8,
              }}
            >
              Home
            </Link>
            <Link
              to="/stories/new"
              style={{
                color: 'var(--color-text-on-primary)',
                textDecoration: 'none',
                fontWeight:
                  location.pathname === '/stories/new'
                    ? 'var(--font-weight-semibold)'
                    : 'var(--font-weight-normal)',
                opacity: location.pathname === '/stories/new' ? 1 : 0.8,
              }}
            >
              Create Story
            </Link>
          </div>
        </nav>
      </header>

      <main
        style={{
          flex: 1,
          maxWidth: '1200px',
          width: '100%',
          margin: '0 auto',
          padding: 'var(--spacing-xl)',
        }}
      >
        {children}
      </main>

      <footer
        style={{
          backgroundColor: 'var(--color-surface)',
          borderTop: '1px solid var(--color-border)',
          padding: 'var(--spacing-lg) var(--spacing-xl)',
          textAlign: 'center',
          color: 'var(--color-text-secondary)',
          fontSize: 'var(--font-size-sm)',
        }}
      >
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          &copy; 2026 GeoStory. Built with React, TypeScript, and Vite.
        </div>
      </footer>
    </div>
  );
}

export default AppLayout;
