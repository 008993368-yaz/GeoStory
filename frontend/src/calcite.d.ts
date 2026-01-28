// TypeScript declarations for Calcite web components
// This allows React/TS to recognize calcite-* elements

declare namespace JSX {
  interface IntrinsicElements {
    'calcite-shell': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
    'calcite-shell-panel': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      slot?: string;
      position?: 'start' | 'end';
      resizable?: boolean;
    }, HTMLElement>;
    'calcite-navigation': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      slot?: string;
      label?: string;
    }, HTMLElement>;
    'calcite-navigation-logo': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      slot?: string;
      heading?: string;
      description?: string;
      href?: string;
      target?: string;
    }, HTMLElement>;
    'calcite-button': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      appearance?: 'solid' | 'outline' | 'outline-fill' | 'transparent';
      kind?: 'brand' | 'danger' | 'inverse' | 'neutral';
      scale?: 's' | 'm' | 'l';
      width?: 'auto' | 'half' | 'full';
      alignment?: 'start' | 'end' | 'center' | 'icon-start' | 'icon-end';
      iconStart?: string;
      iconEnd?: string;
      loading?: boolean;
      disabled?: boolean;
      href?: string;
      target?: string;
      type?: 'button' | 'submit' | 'reset';
    }, HTMLElement>;
    'calcite-action': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      text?: string;
      icon?: string;
      active?: boolean;
      disabled?: boolean;
      scale?: 's' | 'm' | 'l';
      slot?: string;
    }, HTMLElement>;
    'calcite-chip': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      appearance?: 'solid' | 'outline';
      kind?: 'brand' | 'inverse' | 'neutral';
      scale?: 's' | 'm' | 'l';
      closable?: boolean;
      disabled?: boolean;
      icon?: string;
      value?: string;
    }, HTMLElement>;
  }
}
