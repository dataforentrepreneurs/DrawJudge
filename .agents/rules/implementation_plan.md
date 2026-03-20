# Goal Description
Complete the UI/UX polish and ensure the multiplayer game is stable. The previous session successfully implemented graceful disconnects and frontend micro-animations. This stage focuses on adding the final audio cues, safeguarding against round-start race conditions, and verifying the CI/CD pipeline functionality.

## Proposed Changes

### Backend ([backend/routers/game.py](file:///d:/DataForEntrepreneurs/PartyGames/DrawJudge/backend/routers/game.py))
#### [MODIFY] game.py(file:///d:/DataForEntrepreneurs/PartyGames/DrawJudge/backend/routers/game.py)
- **Start Round Sync**: Add a guard clause in the `start_round` event handler so that the round only starts if `room.status` is `"waiting"` or `"results"`. This prevents duplicate timer launches and overlapping rounds if the host double-clicks the "Start Round" button.

### Frontend ([frontend/src/App.tsx](file:///d:/DataForEntrepreneurs/PartyGames/DrawJudge/frontend/src/App.tsx))
#### [MODIFY] App.tsx(file:///d:/DataForEntrepreneurs/PartyGames/DrawJudge/frontend/src/App.tsx)
- **Audio Cues**: Implement synthesized audio cues using the browser's native `AudioContext` (no external MP3 assets needed).
- Play a "tick" sound whenever the timer ticks down from 10 to 1.
- Play a "success/tada" chord immediately when the `results_ready` event is received and the AI Judge reveals the winner.

## Verification Plan

### Automated Tests
- Verify [.github/workflows/ci.yml](file:///d:/DataForEntrepreneurs/PartyGames/DrawJudge/.github/workflows/ci.yml) (or similar) executes backend pytest and frontend `npm run build` steps properly.

### Manual Verification
- **Double-click Test:** Start the local server, join as host, and rapidly click "Start Round" multiple times to verify only ONE round initializes.
- **Audio Test:** Play a 15-second Speed Sketch round. Verify that at 10 seconds remaining, the tick-tock sounds play. Verify that after drawing submission, the results screen triggers the "Tada" sound cue.
