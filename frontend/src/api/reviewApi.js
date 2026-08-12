import axios from "axios";
const API_BASE =
  "https://ai-engineering-reviewer.onrender.com";

export async function runReview(code) {
  const response = await axios.post(
    `${API}/review`,
    {
      code,
    }
  );

  return response.data;
}

export async function generateRefactor(
  code
) {
  const response = await axios.post(
    `${API}/refactor`,
    {
      code,
    }
  );

  return response.data;
}
export async function getHistory() {
  const response = await axios.get(
    `${API}/history`
  );

  return response.data;
}