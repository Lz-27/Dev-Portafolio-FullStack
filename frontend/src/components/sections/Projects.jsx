/**
 * Projects Section — Galería filtrable y Modal de Detalles
 */
import { useState } from "react";
import { ArrowUpRight, Code2, ExternalLink, X } from "lucide-react";

// lucide-react v1.47 — SVG inline
const GithubIcon = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
  </svg>
);
import { useReveal, useRevealGroup } from "../../hooks/useReveal";
import { useApi } from "../../hooks/useApi";
import { PROJECTS } from "../../data/content";
import "./Projects.css";

/* ─── Project Modal ────────────────────────────────────────────────────────── */
function ProjectModal({ project, onClose }) {
  if (!project) return null;

  return (
    <div className="project-modal-backdrop" onClick={onClose}>
      <div className="project-modal" onClick={(e) => e.stopPropagation()}>
        <button className="project-modal__close" onClick={onClose} aria-label="Cerrar modal">
          <X size={24} />
        </button>
        <div className="project-modal__layout">
          <div className="project-modal__left">
            {project.imagen ? (
              <img src={project.imagen} alt={project.titulo} className="project-modal__img" />
            ) : (
              <div className="project-modal__img-placeholder">
                <Code2 size={64} aria-hidden="true" />
              </div>
            )}
          </div>
          <div className="project-modal__right">
            <span className="project-card__category">{project.categoriaLabel}</span>
            <h2 className="project-modal__title">{project.titulo}</h2>
            <p className="project-modal__details">{project.detalles || project.descripcion}</p>
            
            <div className="project-modal__tags">
              {project.tecnologias.map((tech) => (
                <span key={tech} className="badge">{tech}</span>
              ))}
            </div>

            <div className="project-modal__actions">
              {project.github && (
                <a href={project.github} target="_blank" rel="noopener noreferrer" className="project-modal__btn project-modal__btn--outline">
                  <GithubIcon size={18} /> Ver Código
                </a>
              )}
              {project.demo && (
                <a href={project.demo} target="_blank" rel="noopener noreferrer" className="project-modal__btn project-modal__btn--primary">
                  Ver Demo <ArrowUpRight size={18} />
                </a>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─── Project Card ─────────────────────────────────────────────────────────── */
function ProjectCard({ project, index, onClick }) {
  return (
    <article
      className={`project-card reveal reveal-delay-${(index % 3) + 1}`}
      aria-label={project.titulo}
      onClick={() => onClick(project)}
    >
      {/* Image / Placeholder */}
      <div className="project-card__image">
        <div className="project-card__image-placeholder">
          <Code2 size={40} aria-hidden="true" />
        </div>
        {project.destacado && (
          <span className="project-card__featured-badge">⭐ Destacado</span>
        )}
        {/* Overlay on hover */}
        <div className="project-card__overlay" aria-hidden="true">
          <div className="project-card__overlay-links" onClick={(e) => e.stopPropagation()}>
            {project.github && (
              <a
                href={project.github}
                target="_blank"
                rel="noopener noreferrer"
                className="project-card__icon-link"
                aria-label={`Ver código de ${project.titulo}`}
              >
                <GithubIcon size={20} />
              </a>
            )}
            {project.demo && (
              <a
                href={project.demo}
                target="_blank"
                rel="noopener noreferrer"
                className="project-card__icon-link"
                aria-label={`Ver demo de ${project.titulo}`}
              >
                <ExternalLink size={20} />
              </a>
            )}
          </div>
        </div>
      </div>

      {/* Body */}
      <div className="project-card__body">
        <span className="project-card__category">{project.categoriaLabel}</span>
        <h3 className="project-card__title">{project.titulo}</h3>
        <p className="project-card__description">{project.descripcion}</p>

        {/* Tech stack */}
        <div className="project-card__tags">
          {project.tecnologias.slice(0, 4).map((tech) => (
            <span key={tech} className="badge">{tech}</span>
          ))}
        </div>

        {/* Footer links */}
        <div className="project-card__footer" onClick={(e) => e.stopPropagation()}>
          {project.github && (
            <a href={project.github} target="_blank" rel="noopener noreferrer" className="project-card__link">
              <GithubIcon size={15} /> Código
            </a>
          )}
          {project.demo && (
            <a href={project.demo} target="_blank" rel="noopener noreferrer" className="project-card__link project-card__link--primary">
              Demo <ArrowUpRight size={15} />
            </a>
          )}
        </div>
      </div>
    </article>
  );
}

/* ─── Main ─────────────────────────────────────────────────────────────────── */
export default function Projects() {
  const [selectedProject, setSelectedProject] = useState(null);
  
  const headingRef = useReveal({ threshold: 0.2 });
  const gridRef    = useRevealGroup({ threshold: 0.05 });

  return (
    <section id="projects" className="projects section">
      <div className="container">

        {/* Heading */}
        <div className="section-heading" ref={headingRef}>
          <div className="kicker">Portafolio</div>
          <h2>Proyectos Destacados</h2>
          <p>Soluciones innovadoras que he construido con arquitecturas escalables y código limpio</p>
        </div>

        {/* Grid */}
        <div className="projects__grid" ref={gridRef}>
          {PROJECTS.length > 0 ? (
            PROJECTS.map((project, i) => (
              <ProjectCard 
                key={project.id} 
                project={project} 
                index={i} 
                onClick={setSelectedProject} 
              />
            ))
          ) : (
            <div className="projects__empty">
              <Code2 size={40} aria-hidden="true" />
              <p>No hay proyectos en esta categoría</p>
            </div>
          )}
        </div>

      </div>

      {/* Modal Overlay */}
      <ProjectModal project={selectedProject} onClose={() => setSelectedProject(null)} />
    </section>
  );
}
