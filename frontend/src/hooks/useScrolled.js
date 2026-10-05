/**
 * useScrolled — Header scroll behavior
 * Patrón: TECHNICAL_GUIDE.md §6.1 + §9.6
 *
 * Retorna { scrolled, scrolledDown } para controlar el header.
 * Usa passive: true para no bloquear el scroll del navegador.
 */
import { useEffect, useState } from "react";

export function useScrolled(threshold = 20) {
  const [scrolled, setScrolled] = useState(false);
  const [scrolledDown, setScrolledDown] = useState(false);

  useEffect(() => {
    let lastY = window.scrollY;

    const onScroll = () => {
      const currentY = window.scrollY;
      setScrolled(currentY > threshold);
      setScrolledDown(currentY > 80 && currentY > lastY);
      lastY = currentY;
    };

    // passive: true — browser optimization, no jank (patrón §6.1)
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [threshold]);

  return { scrolled, scrolledDown };
}
