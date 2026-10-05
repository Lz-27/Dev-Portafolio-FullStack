/**
 * ThemeContext — Sistema de 3 temas
 * Patrón: TECHNICAL_GUIDE.md §3.4
 *
 * Temas: dark | light | navy
 * Mecanismo: document.documentElement.setAttribute("data-theme", theme)
 * Persistencia: localStorage "pf-theme"
 */
import { createContext, useContext, useEffect, useState } from "react";

const THEMES = ["dark", "light", "navy"];
const STORAGE_KEY = "pf-theme";

const ThemeContext = createContext(null);

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return THEMES.includes(stored) ? stored : "dark";
    } catch {
      return "dark";
    }
  });

  // Aplica el atributo al DOM y persiste — patrón §3.4
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }, [theme]);

  // Cicla entre temas: dark → light → navy → dark
  const cycleTheme = () => {
    setTheme((prev) => {
      const idx = THEMES.indexOf(prev);
      return THEMES[(idx + 1) % THEMES.length];
    });
  };

  const value = { theme, setTheme, cycleTheme, themes: THEMES };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
}
