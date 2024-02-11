  import React, { useState, useEffect } from 'react';
  import './App.css';
  import GameBoard from './components/GameBoard';
  import { getAIMove } from './services/api';

  function App() {
    const [boardState, setBoardState] = useState(Array.from({ length: 6 }, () => Array(7).fill(null)));
    const [playerTurn, setPlayerTurn] = useState(1);

    useEffect(() => {
      if (playerTurn === 2) {
        console.log('Requesting AI move from backend...');
        makeAIMove();
      }
    }, [playerTurn]);

    const handleDropPiece = async (column) => {
      if (playerTurn === 1) {
        const newBoardState = dropPiece(boardState, column, 1);
        setBoardState(newBoardState);
        setPlayerTurn(2);
      }
    };

    const makeAIMove = async () => {
      try {
        const response = await getAIMove ( boardState, playerTurn );
        const responseData = await response.json();
        console.log('Backend response received:', responseData);
        const { column, updated_board_state } = responseData;
        if (column !== undefined && updated_board_state !== undefined) {
          const newBoardState = dropPiece(updated_board_state, column, 2);
          setBoardState(newBoardState);
          setPlayerTurn(1);
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

    return (
      <div className="App">
        <h1>Connect 4</h1>
        <GameBoard boardState={boardState} onDropPiece={handleDropPiece} />
      </div>
    );
  }

  export default App;
