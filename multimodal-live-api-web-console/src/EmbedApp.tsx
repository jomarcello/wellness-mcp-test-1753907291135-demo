/**
 * Embed App - Minimal version for iframe embedding
 */

import { LiveAPIProvider } from "./contexts/LiveAPIContext";
import BeautyMedEmbed from "./components/beautymed-embed/BeautyMedEmbed";
import { LiveClientOptions } from "./types";

const API_KEY = process.env.REACT_APP_GEMINI_API_KEY as string;
if (typeof API_KEY !== "string") {
  throw new Error("set REACT_APP_GEMINI_API_KEY in .env");
}

const apiOptions: LiveClientOptions = {
  apiKey: API_KEY,
};

function EmbedApp() {
  return (
    <div style={{ 
      margin: 0, 
      padding: '20px',
      minHeight: '100vh',
      background: 'transparent',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center'
    }}>
      <LiveAPIProvider options={apiOptions}>
        <BeautyMedEmbed />
      </LiveAPIProvider>
    </div>
  );
}

export default EmbedApp;