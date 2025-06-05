import { useState } from 'react';

function App() {
  const [message, setMessage] = useState('Not connected');

  const checkConnection = async () => {
    try {
      const res = await fetch('http://localhost:8000/ping');
      const data = await res.json();
      setMessage(`Server says: ${data.status}`);
    } catch {
      setMessage('❌ Could not connect to backend');
    }
  };

  return (
    <div className="bg-bg text-text min-h-screen flex flex-col">
      {/* ─── TOP MENU BAR ───────────────────────────────────────────────────── */}
      <header className="w-full bg-secondary border-b border-border shadow-md">
        <nav className="max-w-5xl mx-auto px-6 py-4 flex justify-center space-x-12">
          <NavButton text="Ascend" href="#" />
          <NavButton text="Method" href="#" />
        </nav>
      </header>

      {/* ─── MAIN CONTENT (VERTICALLY & HORIZONTALLY CENTERED) ──────────────── */}
      <main className="flex-grow flex items-center justify-center px-6">
        <div className="text-center animate-fade-in">
          <h1 className="text-5xl font-extrabold text-primary mb-4">
            Welcome to ex0dus
          </h1>
          <p className="text-lg text-text/80 max-w-xl">
            Begin your path to digital freedom. Choose your level. Learn the method.
          </p>
        </div>
      </main>

      {/* ─── CHECK CONNECTION (BOTTOM-LEFT FIXED) ───────────────────────────── */}
      <div className="absolute bottom-4 left-4 flex flex-col items-start space-y-1">
        <button
          onClick={checkConnection}
          className="bg-border hover:bg-primary text-bg px-3 py-1.5 rounded shadow-sm transition-colors duration-200"
        >
          Check Connection
        </button>
        <p className="text-xs text-text/70">{message}</p>
      </div>
    </div>
  );
}

function NavButton({ text, href }) {
  return (
    <a
      href={href}
      className="
        text-text 
        hover:text-primary 
        transition-colors duration-200 
        font-semibold text-lg tracking-wide 
        pb-1
        border-b-2 border-transparent 
        hover:border-primary
      "
    >
      {text}
    </a>
  );
}

export default App;
