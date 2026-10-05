/**
 * useApi.js
 * ──────────
 * Hook para consumo de la API FastAPI del portafolio con fallback elegante a datos locales.
 */
import { useState, useEffect } from "react";

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

export function useApi(endpoint, fallbackData = []) {
  const [data, setData] = useState(fallbackData);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchData() {
      try {
        setLoading(true);
        const res = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!res.ok) {
          throw new Error(`HTTP error ${res.status}`);
        }
        const json = await res.json();
        if (isMounted) {
          // Si es paginado { items: [...] } o directo [...]
          const items = Array.isArray(json) ? json : (json.items || fallbackData);
          setData(items);
          setError(null);
        }
      } catch (err) {
        if (isMounted) {
          // En caso de que el backend no esté activo temporalmente, mantenemos fallbackData
          setData(fallbackData);
          setError(err.message);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [endpoint]);

  return { data, loading, error };
}
