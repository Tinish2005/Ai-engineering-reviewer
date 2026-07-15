import axios from "axios";

const API = "http://127.0.0.1:5000";

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