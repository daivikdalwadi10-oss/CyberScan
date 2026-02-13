import api from "./api.js";

export const login = async (payload) => {
  const { data } = await api.post("/auth/login", payload);
  return data;
};

export const logout = async () => {
  const { data } = await api.post("/auth/logout");
  return data;
};

export const refresh = async (payload) => {
  const { data } = await api.post("/auth/refresh", payload);
  return data;
};
