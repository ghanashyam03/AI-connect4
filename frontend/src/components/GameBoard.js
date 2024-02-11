import React from 'react';

function GameBoard({ boardState, onDropPiece }) {
  const renderBoard = () => {
    return boardState.map((row, rowIndex) => (
      <div key={rowIndex} className="row">
        {row.map((cell, colIndex) => (
          <div key={colIndex} className="cell" onClick={() => handleCellClick(colIndex)}>
            {cell === 1 && <div className="piece player1"></div>}
            {cell === 2 && <div className="piece player2"></div>}
          </div>
        ))}
      </div>
    ));
  };

  const handleCellClick = (column) => {
    onDropPiece(column);
  };

  return (
    <div className="game-board">
      {renderBoard()}
    </div>
  );
}

export default GameBoard;
