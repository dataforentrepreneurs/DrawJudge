const getDynamicHost = () => {
  const envUrl = import.meta.env.VITE_BACKEND_URL;
  if (envUrl) return envUrl;
  const currentHost = window.location.host;
  if (currentHost && !currentHost.includes('localhost') && !currentHost.startsWith('127.0.0.1')) {
    return currentHost;
  }
  if (currentHost && (currentHost.includes('localhost:5173') || currentHost.includes('127.0.0.1:5173'))) {
    return 'localhost:8000';
  }
  return 'play.d4e.ai';
};

export const setupTelemetry = (gameName: string) => {
  const host = getDynamicHost();
  const isSecure = !host.includes('localhost') && !host.startsWith('127.0.0.1');
  const protocol = isSecure ? 'https' : 'http';
  const endpoint = `${protocol}://${host}/api/telemetry/frontend-error`;

  const reportError = async (message: string, stackTrace?: string) => {
    try {
      const params = new URLSearchParams(window.location.search);
      const roomCode = params.get('room') || '';
      
      // Attempt to safely grab player ID
      let playerId = '';
      try {
        playerId = localStorage.getItem('dj_player_id') || localStorage.getItem('cc_player_id') || '';
      } catch (e) {
        // Ignored
      }

      await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          stack_trace: stackTrace,
          url: window.location.href,
          browser_info: navigator.userAgent,
          room_code: roomCode,
          player_id: playerId,
          game: gameName
        })
      });
    } catch (e) {
      console.error("Failed to send telemetry", e);
    }
  };

  window.addEventListener('error', (event) => {
    reportError(`Uncaught Error: ${event.message}`, event.error?.stack);
  });

  window.addEventListener('unhandledrejection', (event) => {
    const reason = event.reason;
    reportError(`Unhandled Promise Rejection: ${reason?.message || reason}`, reason?.stack);
  });
};
