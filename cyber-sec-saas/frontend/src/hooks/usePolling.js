import { useEffect, useRef } from "react";

export const usePolling = (callback, delay) => {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (!delay && delay !== 0) return undefined;

    const tick = () => savedCallback.current();
    tick();
    const id = setInterval(tick, delay);
    return () => clearInterval(id);
  }, [delay]);
};
