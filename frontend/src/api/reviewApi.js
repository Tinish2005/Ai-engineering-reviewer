import axios from "axios";

const API = "http://127.0.0.1:5000";

export async function runReview(code) {
  const response =
    await axios.post(
      `${API}/review`,
      {
        code,
      }
    );

  return response.data;
}