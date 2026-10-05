/**
 * Skills Section — Categorías con barras de progreso + marquee ticker
 */
import { useReveal, useRevealGroup } from "../../hooks/useReveal";
import { SKILLS_CATEGORIES, TECH_TICKER } from "../../data/content";
import "./Skills.css";

/* ─── Skill Card ───────────────────────────────────────────────────────── */
function SkillCard({ skill }) {
  const ref = useReveal({ threshold: 0.4 });

  return (
    <div 
      className="skill-card" 
      ref={ref}
      style={{ "--skill-color": skill.color }}
    >
      <div className="skill-card__bg"></div>
      <div className="skill-card__content">
        <div className="skill-card__icon-wrapper">
          <span className="skill-card__icon" aria-hidden="true">{skill.icon}</span>
        </div>
        <div className="skill-card__info">
          <span className="skill-card__name">{skill.name}</span>
        </div>
      </div>
    </div>
  );
}

/* ─── Main ──────────────────────────────────────────────────────────────── */
export default function Skills() {
  const headingRef  = useReveal({ threshold: 0.3 });
  const panelRef    = useRevealGroup({ threshold: 0.05 });

  // Aplanar todas las habilidades
  const allSkills = SKILLS_CATEGORIES.flatMap(cat => cat.skills);

  // Duplica el ticker para loop continuo — patrón §5.4
  const ticker = [...TECH_TICKER, ...TECH_TICKER];

  return (
    <section id="skills" className="skills section">
      <div className="container">

        {/* Heading */}
        <div className="section-heading" ref={headingRef}>
          <div className="kicker">Tecnologías</div>
          <h2>Stack Tecnológico</h2>
          <p>Herramientas y lenguajes que domino para crear soluciones de alto impacto</p>
        </div>

        {/* Skills Panel */}
        <div className="skills__panel" ref={panelRef}>
          {allSkills.map((skill) => (
            <SkillCard key={skill.name} skill={skill} />
          ))}
        </div>

      </div>

      {/* Tech Ticker Marquee — patrón §5.4 */}
      <div className="skills__ticker-wrapper" aria-hidden="true">
        <div className="skills__ticker">
          <div className="marquee-track">
            {ticker.map((tech, i) => (
              <span key={`${tech}-${i}`} className="skills__ticker-item">
                {tech}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
