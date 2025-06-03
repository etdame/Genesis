import { useState } from 'react';

function App() {
  const [message, setMessage] = useState('Not connected');

  const checkConnection = async () => {
    try {
      const res = await fetch('http://localhost:8000/ping');
      const data = await res.json();
      setMessage(`Server says: ${data.status}`);
    } catch (err) {
      setMessage('❌ Could not connect to backend');
    }
  };

  return (
    <main className="p-4">
      <button
        onClick={checkConnection}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Check Connection
      </button>
      <p className="mt-4">{message}</p>
    </main>
  );
}

export default App;
