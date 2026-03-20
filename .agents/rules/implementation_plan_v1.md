# Step 5: Multiplayer & UI/UX Polish Plan

This final step turns the functional prototype into a robust, satisfying party game.

## Proposed Changes

### Backend: Multiplayer Stability ([backend/routers/game.py](file:///d:/DataForEntrepreneurs/PartyGames/DrawJudge/backend/routers/game.py))
- **Handle Disconnects Gracefully:** Currently, if a player closes their tab, the game doesn't remove them. We will add `try/except` blocks in the WebSocket endpoint to catch `WebSocketDisconnect` exceptions, immediately remove the player from the room state, and broadcast the updated player list to everyone else so the Host screen updates in real-time.
- **Start Round Sync:** Ensure that when the host clicks "Start Round", all connected WebSocket clients are explicitly notified exactly once.

### Frontend: UI/UX Enhancements
- **Visual Timer ([frontend/src/DrawCanvas.tsx](file:///d:/DataForEntrepreneurs/PartyGames/DrawJudge/frontend/src/DrawCanvas.tsx)):** We will overlay a large, visible countdown timer onto the drawing canvas so players know exactly how much time is left.
- **Audio Cues ([frontend/src/App.tsx](file:///d:/DataForEntrepreneurs/PartyGames/DrawJudge/frontend/src/App.tsx)):** We can add simple HTML5 `<audio>` triggers for a "Tick Tock" sound during the final 10 seconds, and a "Tada/Cheer" sound when the AI Judge reveals the winner.
- **Micro-Animations ([frontend/src/index.css](file:///d:/DataForEntrepreneurs/PartyGames/DrawJudge/frontend/src/index.css)):** Introduce CSS keyframe animations (like `popIn`, `slideUp`) for when the leaderboard appears and when player names join the lobby.

## Verification Plan

### Automated Tests
- Ensure the GitHub Actions CI pipeline still builds perfectly after modifying the React components.

### Manual Verification
- **Disconnect Test:** We will join as a player, then close the tab, and verify the Host screen successfully removes us.
- **Timer Test:** Start a game and ensure the visual countdown reaches zero flawlessly.
