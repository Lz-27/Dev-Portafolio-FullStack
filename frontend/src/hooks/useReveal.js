/**
 * useReveal — Scroll Reveal via IntersectionObserver
 * Patrón: TECHNICAL_REFERENCE.md §4.2 — useReveal.js
 *
 * Añade la clase "is-visible" al elemento cuando entra al viewport.
 * Funciona con las clases .reveal y .reveal-mask de animations.css
 */
import { useEffect, useRef } from "react";

/**
 * @param {Object} options
 * @param {number} options.threshold - Fracción visible para trigger (default 0.12)
 * @param {string} options.rootMargin - Margen del observer (default "0px 0px -60px 0px")
 * @param {boolean} options.once - Trigger solo una vez (default true)
 */
export function useReveal({
  threshold = 0.12,
  rootMargin = "0px 0px -60px 0px",
  once = true,
} = {}) {
  const ref = useRef(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          el.classList.add("is-visible");
          if (once) observer.unobserve(el);
        } else if (!once) {
          el.classList.remove("is-visible");
        }
      },
      { threshold, rootMargin }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold, rootMargin, once]);

  return ref;
}

/**
 * useRevealGroup — Aplica reveal escalonado a múltiples elementos
 * Retorna un ref para el contenedor y aplica .is-visible a los hijos
 * con clase .reveal en orden.
 */
export function useRevealGroup({ threshold = 0.08, rootMargin = "0px 0px -40px 0px" } = {}) {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const items = container.querySelectorAll(".reveal");

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold, rootMargin }
    );

    items.forEach((item) => observer.observe(item));
    return () => observer.disconnect();
  }, [threshold, rootMargin]);

  return containerRef;
}
