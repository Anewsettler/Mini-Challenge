const BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

export const fetchInitialQuestion = async (url) => {
  const response = await fetch(`${BASE_URL}/initial-question`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch initial question');
  }

  return response.json();
};

export const submitAnswer = async (answerData) => {
  const response = await fetch(`${BASE_URL}/classify-user-response`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(answerData)
  });
  
  if (!response.ok) {
    throw new Error('Failed to submit answer');
  }

  return response.json();
};
