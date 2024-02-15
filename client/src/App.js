import React, { useState, useEffect } from 'react';
import './App.css';
import GameBoard from './components/GameBoard';
import { getAIMove } from './services/api';

function App() {
  const [boardState, setBoardState] = useState(Array.from({ length: 6 }, () => Array(7).fill(null)));
  const [playerTurn, setPlayerTurn] = useState(1);
  const [winner, setWinner] = useState(null);
  const [gameMode, setGameMode] = useState(null); // 'friend' or 'ai'

  useEffect(() => {
    if (playerTurn === 2 && gameMode === 'ai' && !winner) {
      makeAIMove();
    }
  }, [playerTurn]);

  const handleGameModeSelect = (mode) => {
    setGameMode(mode);
    setBoardState(Array.from({ length: 6 }, () => Array(7).fill(null))); // Reset the board
    setPlayerTurn(1); // Reset player turn
    setWinner(null); // Reset winner
  };

  const handleDropPiece = async (column) => {
    if (playerTurn === 1 && !winner) {
      const newBoardState = dropPiece(boardState, column, 1);
      setBoardState(newBoardState);
      setPlayerTurn(2);
      checkWinner(newBoardState);
      if (gameMode === 'ai' && !winner) {
        makeAIMove();
      }
    }
  };

  const makeAIMove = async () => {
    try {
      const response = await getAIMove(boardState, 2);
      const responseData = await response.json();
      const { column, updated_board_state, winner } = responseData;
      if (column !== undefined && updated_board_state !== undefined) {
        const newBoardState = updated_board_state;
        setBoardState(newBoardState);
        setPlayerTurn(1);
        setWinner(winner);
      } else {
        console.error('Invalid response from backend:', responseData);
      }
    } catch (error) {
      console.error('Error making AI move:', error);
    }
  };

  const dropPiece = (board, column, player) => {
    const newBoard = board.map(row => [...row]);
    for (let row = 5; row >= 0; row--) {
      if (newBoard[row][column] === null) {
        newBoard[row][column] = player;
        break;
      }
    }
    return newBoard;
  };

  const checkWinner = (board) => {
    // Implement logic to check for winner
    // Update winner state accordingly
  };

  return (
    <div className="App">
      <h1>Connect 4</h1>
      {gameMode === null && (
        <div className="mode-selection">
          <button onClick={() => handleGameModeSelect('friend')}>Play with Friend</button>
          <button onClick={() => handleGameModeSelect('ai')}>Play against AI</button>
        </div>
      )}
      {gameMode && gameMode !== null && (
        <>
          <GameBoard boardState={boardState} onDropPiece={handleDropPiece} />
          {winner !== null && (
            <h2>{winner === 1 ? 'Humanity succeeds!' : 'Artificial intelligence takes over!'}</h2>
          )}
        </>
      )}
    </div>
  );
}

export default App;
