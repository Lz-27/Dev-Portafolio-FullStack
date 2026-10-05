/**
 * useCountUp — Contador animado con requestAnimationFrame
 * Patrón: TECHNICAL_REFERENCE.md §4.2 — useCountUp.js
 */
import { useEffect, useRef, useState } from "react";

/**
 * @param {number} target - Valor final del contador
 * @param {number} duration - Duración en ms (default 2000)
 * @param {boolean} triggered - Inicia la animación cuando es true
 */
export function useCountUp(target, duration = 2000, triggered = false) {
  const [count, setCount] = useState(0);
  const rafRef = useRef(null);
  const startRef = useRef(null);

  useEffect(() => {
    if (!triggered) return;

    startRef.current = null;

    const step = (timestamp) => {
      if (!startRef.current) startRef.current = timestamp;
      const elapsed = timestamp - startRef.current;
      const progress = Math.min(elapsed / duration, 1);
      // Easing: ease-out cubic
      const eased = 1 - (1 - progress) ** 3;
      setCount(Math.round(eased * target));

      if (progress < 1) {
        rafRef.current = requestAnimationFrame(step);
      }
    };

    rafRef.current = requestAnimationFrame(step);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [target, duration, triggered]);

  return count;
}

/**
 * useCountUpOnReveal — Combina useCountUp con IntersectionObserver
 * El contador arranca cuando el elemento entra al viewport.
 */
export function useCountUpOnReveal(target, duration = 2000) {
  const [triggered, setTriggered] = useState(false);
  const ref = useRef(null);
  const count = useCountUp(target, duration, triggered);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setTriggered(true);
          observer.unobserve(el);
        }
      },
      { threshold: 0.5 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return { count, ref };
}
