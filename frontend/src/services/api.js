async function getAIMove(boardState, player) {
  try {
    const response = await fetch('http://localhost:5000/get_ai_move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ board_state: boardState, player: player })
    });
    return response;
  } catch (error) {
    console.error('Error getting AI move:', error);
    throw error; // Rethrow the error for handling in the calling code
  }
}

export { getAIMove };

  