/**
 * Timeline Section — Experiencia y Educación
 */
import { Briefcase, GraduationCap } from "lucide-react";
import { useReveal, useRevealGroup } from "../../hooks/useReveal";
import { TIMELINE } from "../../data/content";
import "./Timeline.css";

function TimelineItem({ item, index }) {
  const isLeft = index % 2 === 0;
  const Icon = item.tipo === "trabajo" ? Briefcase : GraduationCap;

  return (
    <div className={`timeline__item${isLeft ? " timeline__item--left" : " timeline__item--right"} reveal reveal-delay-${(index % 4) + 1}`}>
      {/* Node */}
      <div className="timeline__node" aria-hidden="true">
        <div className="timeline__node-icon">
          <Icon size={18} />
        </div>
        <div className="timeline__node-pulse" />
      </div>

      {/* Card */}
      <article className="timeline__card">
        <div className="timeline__card-header">
          <div className="timeline__type-badge">
            <Icon size={12} aria-hidden="true" />
            {item.tipo === "trabajo" ? "Trabajo" : "Educación"}
          </div>
          <span className="timeline__period">{item.periodo}</span>
        </div>
        <h3 className="timeline__title">{item.titulo}</h3>
        <p className="timeline__company">{item.empresa}</p>
        <p className="timeline__description">{item.descripcion}</p>
        <div className="timeline__techs">
          {item.tecnologias.map((t) => (
            <span key={t} className="badge">{t}</span>
          ))}
        </div>
      </article>
    </div>
  );
}

export default function Timeline() {
  const headingRef = useReveal({ threshold: 0.2 });
  const listRef    = useRevealGroup({ threshold: 0.05 });

  return (
    <section id="timeline" className="timeline section">
      <div className="container">

        <div className="section-heading" ref={headingRef}>
          <div className="kicker">Trayectoria</div>
          <h2>Experiencia & Educación</h2>
          <p>Mi camino profesional y académico en el mundo del software y los datos</p>
        </div>

        <div className="timeline__list" ref={listRef}>
          {/* Center line */}
          <div className="timeline__line" aria-hidden="true" />

          {TIMELINE.map((item, i) => (
            <TimelineItem key={item.id} item={item} index={i} />
          ))}
        </div>

      </div>
    </section>
  );
}
