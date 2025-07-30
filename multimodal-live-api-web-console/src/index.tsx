/**
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import EmbedApp from './EmbedApp';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

// Check if we're in embed mode
const isEmbedMode = (window as any).EMBED_MODE ||
                    window.location.pathname === '/embed' || 
                    window.location.pathname.includes('embed.html') ||
                    window.location.search.includes('embed=true') ||
                    window.location.hash.includes('embed');

console.log('🔍 Checking embed mode:', {
  pathname: window.location.pathname,
  search: window.location.search,
  hash: window.location.hash,
  EMBED_MODE: (window as any).EMBED_MODE,
  isEmbedMode
});

root.render(
  <React.StrictMode>
    {isEmbedMode ? <EmbedApp /> : <App />}
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
