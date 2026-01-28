import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';

function AppLayout() {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <calcite-shell style={{ '--calcite-ui-brand': 'var(--color-primary)' } as React.CSSProperties}>
      <calcite-navigation slot="header" label="GeoStory Navigation">
        <calcite-navigation-logo
          slot="logo"
          heading="GeoStory"
          onClick={() => navigate('/')}
          style={{ cursor: 'pointer' }}
        />
        
        <div
          slot="content-end"
          style={{
            display: 'flex',
            gap: 'var(--spacing-md)',
            alignItems: 'center',
            paddingRight: 'var(--spacing-md)',
          }}
        >
          <Link
            to="/"
            style={{
              color: location.pathname === '/' ? 'var(--color-primary)' : 'var(--color-text-primary)',
              textDecoration: 'none',
              fontWeight: location.pathname === '/' ? 'var(--font-weight-semibold)' : 'var(--font-weight-normal)',
              padding: 'var(--spacing-sm) var(--spacing-md)',
            }}
            aria-label="Navigate to home page"
          >
            Home
          </Link>
          
          <calcite-button
            appearance="solid"
            kind="brand"
            scale="m"
            onClick={() => navigate('/stories/new')}
            aria-label="Create a new story"
          >
            New Story
          </calcite-button>
        </div>
      </calcite-navigation>

      <main
        style={{
          padding: 'var(--spacing-xl)',
          maxWidth: '1200px',
          width: '100%',
          margin: '0 auto',
        }}
      >
        <Outlet />
      </main>

      <footer
        slot="footer"
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
          &copy; 2026 GeoStory. Built with React, TypeScript, and Calcite Design System.
        </div>
      </footer>
    </calcite-shell>
  );
}

export default AppLayout;
