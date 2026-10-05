/**
 * Certifications Section — Galería filtrable con modal de detalles
 */
import { useState } from "react";
import { Award, ExternalLink, X } from "lucide-react";
import { useReveal, useRevealGroup } from "../../hooks/useReveal";
import { CERTIFICATIONS } from "../../data/content";
import "./Certifications.css";

/* ─── Cert Modal ─────────────────────────────────────────────────────────── */
function CertModal({ cert, onClose }) {
  if (!cert) return null;

  return (
    <div className="cert-modal-backdrop" onClick={onClose}>
      <div className="cert-modal" onClick={(e) => e.stopPropagation()}>
        <button className="cert-modal__close" onClick={onClose} aria-label="Cerrar">
          <X size={22} />
        </button>
        <div className="cert-modal__layout">
          {/* Izquierda: imagen o placeholder */}
          <div className="cert-modal__left">
            {cert.imagen ? (
              <img src={cert.imagen} alt={`Certificado: ${cert.titulo}`} className="cert-modal__img" />
            ) : (
              <div className="cert-modal__img-placeholder">
                <Award size={72} strokeWidth={1.2} aria-hidden="true" />
                <span className="cert-modal__placeholder-label">{cert.emisor}</span>
              </div>
            )}
          </div>

          {/* Derecha: info */}
          <div className="cert-modal__right">
            <div className="cert-modal__meta">
              <span className="cert-card__category">{cert.categoriaLabel}</span>
              <span className="cert-modal__year">{cert.fecha}</span>
            </div>
            <h2 className="cert-modal__title">{cert.titulo}</h2>
            <p className="cert-modal__emisor">Emitido por <strong>{cert.emisor}</strong></p>
            <p className="cert-modal__desc">{cert.descripcion}</p>

            <div className="cert-modal__skills">
              {cert.habilidades.map((h) => (
                <span key={h} className="badge">{h}</span>
              ))}
            </div>

            {cert.credencial && (
              <div className="cert-modal__actions">
                <a
                  href={cert.credencial}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="cert-modal__btn"
                >
                  Ver Credencial <ExternalLink size={16} />
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─── Cert Card ──────────────────────────────────────────────────────────── */
function CertCard({ cert, index, onClick }) {
  const ref = useReveal({ threshold: 0.15 });
  return (
    <article
      className={`cert-card reveal reveal-delay-${(index % 3) + 1}`}
      ref={ref}
      onClick={() => onClick(cert)}
      aria-label={cert.titulo}
    >
      {/* Thumbnail */}
      <div className="cert-card__thumb">
        {cert.imagen ? (
          <img src={cert.imagen} alt={cert.titulo} className="cert-card__thumb-img" />
        ) : (
          <div className="cert-card__thumb-placeholder">
            <Award size={36} strokeWidth={1.2} aria-hidden="true" />
          </div>
        )}
        <div className="cert-card__thumb-overlay" aria-hidden="true">
          <span className="cert-card__thumb-cta">Ver detalle</span>
        </div>
      </div>

      {/* Body */}
      <div className="cert-card__body">
        <div className="cert-card__header">
          <span className="cert-card__category">{cert.categoriaLabel}</span>
          <span className="cert-card__year">{cert.fecha}</span>
        </div>
        <h3 className="cert-card__title">{cert.titulo}</h3>
        <p className="cert-card__emisor">{cert.emisor}</p>
        <div className="cert-card__skills">
          {cert.habilidades.slice(0, 3).map((h) => (
            <span key={h} className="badge">{h}</span>
          ))}
        </div>
      </div>
    </article>
  );
}

/* ─── Main ───────────────────────────────────────────────────────────────── */
export default function Certifications() {
  const [selectedCert, setSelectedCert] = useState(null);
  const headingRef = useReveal({ threshold: 0.2 });
  const gridRef    = useRevealGroup({ threshold: 0.05 });

  return (
    <section id="certifications" className="certifications section">
      <div className="container">

        {/* Heading */}
        <div className="section-heading" ref={headingRef}>
          <div className="kicker">Formación</div>
          <h2>Certificaciones</h2>
          <p>Credenciales que validan mi conocimiento técnico y compromiso con el aprendizaje continuo</p>
        </div>

        {/* Grid */}
        <div className="certs__grid" ref={gridRef}>
          {CERTIFICATIONS.length > 0 ? (
            CERTIFICATIONS.map((cert, i) => (
              <CertCard key={cert.id} cert={cert} index={i} onClick={setSelectedCert} />
            ))
          ) : (
            <div className="certs__empty">
              <Award size={40} aria-hidden="true" />
              <p>No hay certificaciones en esta categoría</p>
            </div>
          )}
        </div>

      </div>

      {/* Modal */}
      <CertModal cert={selectedCert} onClose={() => setSelectedCert(null)} />
    </section>
  );
}
