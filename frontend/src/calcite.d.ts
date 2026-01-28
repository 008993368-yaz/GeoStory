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
    'calcite-card': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
    'calcite-panel': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      heading?: string;
      description?: string;
      loading?: boolean;
      closable?: boolean;
      closed?: boolean;
      disabled?: boolean;
    }, HTMLElement>;
    'calcite-label': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      for?: string;
      scale?: 's' | 'm' | 'l';
      layout?: 'default' | 'inline' | 'inline-space-between';
      alignment?: 'start' | 'end';
      disabled?: boolean;
      required?: boolean;
    }, HTMLElement>;
    'calcite-input': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      value?: string | number;
      type?: 'text' | 'number' | 'email' | 'password' | 'tel' | 'url' | 'date' | 'time' | 'datetime-local';
      name?: string;
      placeholder?: string;
      disabled?: boolean;
      required?: boolean;
      scale?: 's' | 'm' | 'l';
      status?: 'idle' | 'valid' | 'invalid';
      min?: string | number;
      max?: string | number;
      step?: string | number;
      minLength?: number;
      maxLength?: number;
      readOnly?: boolean;
      loading?: boolean;
      clearable?: boolean;
      icon?: string;
      prefixText?: string;
      suffixText?: string;
      onCalciteInputInput?: (event: CustomEvent) => void;
      onCalciteInputChange?: (event: CustomEvent) => void;
    }, HTMLElement>;
    'calcite-text-area': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      value?: string;
      name?: string;
      placeholder?: string;
      disabled?: boolean;
      required?: boolean;
      scale?: 's' | 'm' | 'l';
      status?: 'idle' | 'valid' | 'invalid';
      maxLength?: number;
      minLength?: number;
      rows?: number;
      resize?: 'none' | 'vertical' | 'horizontal' | 'both';
      readOnly?: boolean;
      onCalciteTextAreaInput?: (event: CustomEvent) => void;
      onCalciteTextAreaChange?: (event: CustomEvent) => void;
    }, HTMLElement>;
    'calcite-select': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      value?: string;
      name?: string;
      disabled?: boolean;
      required?: boolean;
      scale?: 's' | 'm' | 'l';
      width?: 'auto' | 'half' | 'full';
      label?: string;
      onCalciteSelectChange?: (event: CustomEvent) => void;
    }, HTMLElement>;
    'calcite-option': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      value?: string;
      label?: string;
      disabled?: boolean;
      selected?: boolean;
    }, HTMLElement>;
    'calcite-notice': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      kind?: 'brand' | 'danger' | 'info' | 'success' | 'warning';
      open?: boolean;
      closable?: boolean;
      icon?: string | boolean;
      scale?: 's' | 'm' | 'l';
      width?: 'auto' | 'half' | 'full';
    }, HTMLElement>;
    'calcite-input-message': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
      status?: 'idle' | 'valid' | 'invalid';
      icon?: string | boolean;
      scale?: 's' | 'm' | 'l';
    }, HTMLElement>;
  }
}
