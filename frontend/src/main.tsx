import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { defineCustomElements } from '@esri/calcite-components/dist/loader';
import App from './App';
import '@esri/calcite-components/dist/calcite/calcite.css';
import '@arcgis/core/assets/esri/themes/light/main.css';
import './styles/tokens.css';
import './styles/global.css';

// Register Calcite web components
defineCustomElements(window);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
