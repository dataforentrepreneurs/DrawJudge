import './App.css'

function App() {
  const go = (path: string) => {
    // Chromecast / Android TV remotes sometimes don't "activate" <a> on DPAD_CENTER.
    // Doing a direct location change makes selection reliable across TV webviews.
    window.location.assign(path)
  }

  const onCardKeyDown = (e: React.KeyboardEvent, path: string) => {
    // Support OK/Enter and Space-to-activate patterns.
    if (e.key === 'Enter' || e.key === 'NumpadEnter' || e.key === ' ') {
      e.preventDefault()
      go(path)
    }
  }

  return (
    <div className="launcher-container">
      <header>
        <h1>PartyGames Hub</h1>
        <p>Select a game to start playing on the TV</p>
      </header>

      <main className="cards-grid">
        <a
          href="/drawjudge/"
          className="game-card"
          tabIndex={0}
          onClick={(e) => {
            e.preventDefault()
            go('/drawjudge/')
          }}
          onKeyDown={(e) => onCardKeyDown(e, '/drawjudge/')}
        >
          <div className="card-image drawjudge-img">
            <span>🎨</span>
          </div>
          <div className="card-content">
            <h2>Draw Judge</h2>
            <p>An AI-powered drawing competition!</p>
          </div>
        </a>

        <a href="/tambola/" className="game-card empty-card">
          <div className="card-image tambola-img">
            <span>🎱</span>
          </div>
          <div className="card-content">
            <h2>Tambola</h2>
            <p>Coming Soon...</p>
          </div>
        </a>
      </main>
    </div>
  )
}

export default App
