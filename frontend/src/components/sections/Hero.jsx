/**
 * Hero Section — Impactante con cursor glow, parallax y typing effect
 * Patrón: TECHNICAL_REFERENCE.md §5.3 Hero.jsx + §4.3 cursor-glow
 */
import { useEffect, useRef } from "react";
import { ArrowDown, ChevronRight, Download, Sparkles } from "lucide-react";
import { useReveal } from "../../hooks/useReveal";
import { useCountUpOnReveal } from "../../hooks/useCountUp";
import { PERSONAL, SOCIAL, STATS } from "../../data/content";
import "./Hero.css";

/* ─── Stat Counter ────────────────────────────────────────────────────────── */
function StatItem({ value, suffix, label }) {
  const { count, ref } = useCountUpOnReveal(value, 1800);
  return (
    <div className="hero__stat" ref={ref}>
      <span className="hero__stat-number">
        {count}<span className="hero__stat-suffix">{suffix}</span>
      </span>
      <span className="hero__stat-label">{label}</span>
    </div>
  );
}

/* ─── Code Window ─────────────────────────────────────────────────────────── */
function CodeWindow() {
  return (
    <div className="hero__code-window float-anim">
      <div className="hero__code-header">
        <span className="hero__dot hero__dot--red"   />
        <span className="hero__dot hero__dot--yellow"/>
        <span className="hero__dot hero__dot--green" />
        <span className="hero__code-filename">developer.py</span>
      </div>
      <div className="hero__code-body">
        <pre aria-hidden="true"><code>
{`\x1b[35mclass\x1b[0m `}
        </code></pre>
        <div className="hero__code-content">
          <div className="hero__code-line">
            <span className="kw">class</span>{" "}
            <span className="cls">MLEngineer</span>:
          </div>
          <div className="hero__code-line indent">
            <span className="kw">def</span>{" "}
            <span className="fn">__init__</span>(self):
          </div>
          <div className="hero__code-line indent2">
            self.skills = [
          </div>
          {["Python", "React", "TensorFlow", "FastAPI"].map((s) => (
            <div key={s} className="hero__code-line indent3">
              <span className="str">&apos;{s}&apos;</span>,
            </div>
          ))}
          <div className="hero__code-line indent2">]</div>
          <div className="hero__code-line" />
          <div className="hero__code-line indent">
            <span className="kw">def</span>{" "}
            <span className="fn">create_solution</span>(self, problem):
          </div>
          <div className="hero__code-line indent2">
            <span className="kw">return</span>{" "}
            <span className="fn">self.innovate</span>(problem)
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─── Hero Main ───────────────────────────────────────────────────────────── */
export default function Hero() {
  const heroRef = useRef(null);
  const glowRef = useRef(null);

  const tagRef    = useReveal({ threshold: 0.5 });
  const titleRef  = useReveal({ threshold: 0.3 });
  const descRef   = useReveal({ threshold: 0.3 });
  const btnsRef   = useReveal({ threshold: 0.3 });
  const statsRef  = useReveal({ threshold: 0.2 });
  const visualRef = useReveal({ threshold: 0.2 });

  // Cursor glow — patrón TECHNICAL_REFERENCE §4.1
  useEffect(() => {
    const hero = heroRef.current;
    if (!hero) return;

    const onMouseMove = (e) => {
      const rect = hero.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top)  / rect.height) * 100;
      hero.style.setProperty("--mouse-x", `${x}%`);
      hero.style.setProperty("--mouse-y", `${y}%`);
    };

    hero.addEventListener("mousemove", onMouseMove, { passive: true });
    return () => hero.removeEventListener("mousemove", onMouseMove);
  }, []);

  const handleScrollToProjects = () => {
    document.getElementById("projects")?.scrollIntoView({ behavior: "smooth" });
  };

  const handleScrollDown = () => {
    document.getElementById("about")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section id="home" className="hero" ref={heroRef}>
      {/* Background gradient + cursor glow */}
      <div className="hero__bg" aria-hidden="true">
        <div className="hero__gradient" />
        <div className="hero__glow" ref={glowRef} />
        <div className="hero__grid" />
      </div>

      <div className="container hero__container">
        {/* ── Content ── */}
        <div className="hero__content">
          {/* Tag */}
          <div className="hero__tag reveal" ref={tagRef}>
            <Sparkles size={14} aria-hidden="true" />
            <span>{PERSONAL.subtitulo}</span>
          </div>

          {/* Title */}
          <h1 className="hero__title reveal" ref={titleRef}>
            Transformando{" "}
            <span className="gradient-text">Datos</span>{" "}
            en{" "}
            <span className="gradient-text">Soluciones</span>{" "}
            Inteligentes
          </h1>

          {/* Description */}
          <p className="hero__description reveal" ref={descRef}>
            {PERSONAL.descripcion}
          </p>

          {/* CTAs */}
          <div className="hero__ctas reveal" ref={btnsRef}>
            <button
              className="btn btn-primary btn-shine"
              onClick={handleScrollToProjects}
              id="hero-cta-projects"
            >
              Ver Proyectos
              <ChevronRight size={16} aria-hidden="true" />
            </button>
            <a
              href={PERSONAL.cv}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-ghost"
              id="hero-cta-cv"
            >
              <Download size={16} aria-hidden="true" />
              Descargar CV
            </a>
          </div>

          {/* Stats */}
          <div className="hero__stats reveal" ref={statsRef}>
            {STATS.map((s) => (
              <StatItem key={s.label} {...s} />
            ))}
          </div>
        </div>

        {/* ── Visual ── */}
        <div className="hero__visual reveal" ref={visualRef}>
          <CodeWindow />
          {/* Decoration rings */}
          <div className="hero__ring hero__ring--1" aria-hidden="true" />
          <div className="hero__ring hero__ring--2" aria-hidden="true" />
        </div>
      </div>

      {/* Scroll Indicator */}
      <button
        className="hero__scroll-indicator"
        onClick={handleScrollDown}
        aria-label="Ir a la siguiente sección"
      >
        <ArrowDown size={20} aria-hidden="true" />
      </button>
    </section>
  );
}
