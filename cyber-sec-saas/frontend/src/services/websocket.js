const getBaseUrl = () => import.meta.env.VITE_API_URL;

export const getWebSocketUrl = (token) => {
  if (!token) return "";
  const base = getBaseUrl();
  const wsBase = base.replace("https://", "wss://").replace("http://", "ws://");
  return `${wsBase}/ws/alerts?token=${token}`;
};
