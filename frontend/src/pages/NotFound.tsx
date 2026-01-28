import { Link } from 'react-router-dom';

function NotFound() {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '400px',
        textAlign: 'center',
      }}
    >
      <h1 style={{ fontSize: 'var(--font-size-3xl)', marginBottom: 'var(--spacing-md)' }}>
        404
      </h1>
      <h2 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--spacing-lg)' }}>
        Page Not Found
      </h2>
      <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-xl)' }}>
        The page you're looking for doesn't exist.
      </p>
      <Link
        to="/"
        style={{
          padding: 'var(--spacing-sm) var(--spacing-lg)',
          backgroundColor: 'var(--color-primary)',
          color: 'var(--color-text-on-primary)',
          borderRadius: 'var(--border-radius-md)',
          textDecoration: 'none',
          fontWeight: 'var(--font-weight-medium)',
        }}
      >
        Go Home
      </Link>
    </div>
  );
}

export default NotFound;
