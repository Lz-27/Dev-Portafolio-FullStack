/**
 * About Section — Presentación personal con highlights y soft skills
 */
import {
  BrainCircuit, Code2, Download, Layers, MapPin, Zap,
} from "lucide-react";
import { useReveal, useRevealGroup } from "../../hooks/useReveal";
import { ABOUT, PERSONAL, SOCIAL } from "../../data/content";
import "./About.css";

const ICON_MAP = { Code2, BrainCircuit, Layers, Zap };

export default function About() {
  const headingRef = useReveal({ threshold: 0.2 });
  const textRef    = useReveal({ threshold: 0.15 });
  const imageRef   = useReveal({ threshold: 0.1 });
  const skillsRef  = useRevealGroup({ threshold: 0.1 });

  return (
    <section id="about" className="about section">
      <div className="container">

        {/* ── Section Heading ── */}
        <div className="about__heading section-heading" ref={headingRef}>
          <div className="kicker">¿Quién soy?</div>
          <h2>{ABOUT.titulo}</h2>
        </div>

        <div className="about__grid">
          {/* ── Image / Avatar ── */}
          <div className="about__image-col reveal" ref={imageRef}>
            <div className="about__avatar-wrapper">
              <div className="about__avatar-ring" aria-hidden="true" />
              <div className="about__avatar-ring about__avatar-ring--2" aria-hidden="true" />
              <div className="about__avatar">
                <div className="about__avatar-placeholder" aria-hidden="true">
                  <Code2 size={64} />
                </div>
              </div>
              {/* Floating badges */}
              <div className="about__badge-float about__badge-float--tl">
                <span>🐍</span> Python
              </div>
              <div className="about__badge-float about__badge-float--br">
                <span>⚛️</span> React
              </div>
            </div>
          </div>

          {/* ── Text ── */}
          <div className="about__text reveal" ref={textRef}>
            {ABOUT.parrafos.map((p, i) => (
              <p key={i} className="about__paragraph">{p}</p>
            ))}

            {/* Strengths */}
            <div className="about__strengths">
              {ABOUT.fortalezas.map(({ icon, label }) => {
                const Icon = ICON_MAP[icon] ?? Code2;
                return (
                  <div key={label} className="about__strength">
                    <Icon size={20} aria-hidden="true" />
                    <span>{label}</span>
                  </div>
                );
              })}
            </div>

            {/* Location + CTA */}
            <div className="about__footer">
              <span className="about__location">
                <MapPin size={16} aria-hidden="true" />
                {PERSONAL.ubicacion}
              </span>
              <a
                href={PERSONAL.cv}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary btn-shine"
                id="about-cv-download"
              >
                <Download size={16} aria-hidden="true" />
                Descargar CV
              </a>
            </div>
          </div>
        </div>

        {/* ── Soft Skills ── */}
        <div className="about__soft" ref={skillsRef}>
          <div className="about__soft-heading kicker">Habilidades blandas</div>
          <div className="about__soft-grid">
            {ABOUT.softSkills.map((skill, i) => (
              <span
                key={skill}
                className={`about__soft-item reveal reveal-delay-${(i % 6) + 1}`}
              >
                {skill}
              </span>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}
