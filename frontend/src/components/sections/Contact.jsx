/**
 * Contact Section — Formulario + info de contacto
 */
import { useState } from "react";
import {
  CheckCircle, Mail, MapPin,
  MessageCircle, Phone, Send, Loader2,
} from "lucide-react";
import { useReveal } from "../../hooks/useReveal";
import { CONTACT, PERSONAL, SOCIAL } from "../../data/content";
import "./Contact.css";

// lucide-react v1.47 — inline SVGs
const GithubIcon = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
  </svg>
);
const LinkedinIcon = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
  </svg>
);

const ICON_MAP = {
  Mail, LinkedinIcon, GithubIcon, Send, MessageCircle, Phone,
  Linkedin: LinkedinIcon,
  Github: GithubIcon,
};

/* ─── Contact Link ─────────────────────────────────────────────────────────── */
function ContactLink({ link }) {
  const Icon = ICON_MAP[link.icon] ?? Mail;
  return (
    <a
      href={link.href}
      target={link.href.startsWith("mailto:") ? undefined : "_blank"}
      rel="noopener noreferrer"
      className="contact__link"
    >
      <div className="contact__link-icon">
        <Icon size={20} aria-hidden="true" />
      </div>
      <div className="contact__link-info">
        <span className="contact__link-label">{link.label}</span>
        <span className="contact__link-value">{link.value}</span>
      </div>
    </a>
  );
}

/* ─── Form ─────────────────────────────────────────────────────────────────── */
const INITIAL = { name: "", email: "", subject: "", message: "" };

function ContactForm() {
  const [form, setForm]     = useState(INITIAL);
  const [errors, setErrors] = useState({});
  const [status, setStatus] = useState("idle"); // idle | loading | success | error

  const validate = () => {
    const e = {};
    if (!form.name.trim() || form.name.trim().length < 2)
      e.name = "El nombre debe tener al menos 2 caracteres";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email))
      e.email = "Email inválido";
    if (!form.message.trim() || form.message.trim().length < 10)
      e.message = "El mensaje debe tener al menos 10 caracteres";
    return e;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: "" }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const e_ = validate();
    if (Object.keys(e_).length > 0) { setErrors(e_); return; }

    setStatus("loading");

    try {
      // Conectará al backend POST /api/v1/messages/
      const apiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";
      const res = await fetch(`${apiUrl}/messages/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Error al enviar el mensaje. Intenta nuevamente.");
      }

      setStatus("success");
      setForm(INITIAL);
    } catch (err) {
      setStatus("error");
      setErrors((prev) => ({
        ...prev,
        submit: err.message || "No se pudo conectar con el servidor. Por favor intenta más tarde."
      }));
    }
  };

  if (status === "success") {
    return (
      <div className="contact__success">
        <CheckCircle size={48} className="contact__success-icon" />
        <h3>¡Mensaje enviado!</h3>
        <p>Gracias por contactarme. Te responderé en menos de 24 horas.</p>
        <button className="btn btn-ghost" onClick={() => setStatus("idle")}>
          Enviar otro mensaje
        </button>
      </div>
    );
  }

  return (
    <form className="contact__form" onSubmit={handleSubmit} noValidate>
      <div className="contact__form-row">
        <div className={`contact__field${errors.name ? " contact__field--error" : ""}`}>
          <label htmlFor="contact-name">Nombre *</label>
          <input
            id="contact-name"
            name="name"
            type="text"
            value={form.name}
            onChange={handleChange}
            placeholder="Tu nombre completo"
            aria-required="true"
            aria-describedby={errors.name ? "contact-name-error" : undefined}
          />
          {errors.name && <span id="contact-name-error" className="contact__error">{errors.name}</span>}
        </div>
        <div className={`contact__field${errors.email ? " contact__field--error" : ""}`}>
          <label htmlFor="contact-email">Email *</label>
          <input
            id="contact-email"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            placeholder="tu@email.com"
            aria-required="true"
            aria-describedby={errors.email ? "contact-email-error" : undefined}
          />
          {errors.email && <span id="contact-email-error" className="contact__error">{errors.email}</span>}
        </div>
      </div>

      <div className="contact__field">
        <label htmlFor="contact-subject">Asunto</label>
        <input
          id="contact-subject"
          name="subject"
          type="text"
          value={form.subject}
          onChange={handleChange}
          placeholder="¿De qué quieres hablar?"
        />
      </div>

      <div className={`contact__field${errors.message ? " contact__field--error" : ""}`}>
        <label htmlFor="contact-message">Mensaje *</label>
        <textarea
          id="contact-message"
          name="message"
          rows={6}
          value={form.message}
          onChange={handleChange}
          placeholder="Cuéntame sobre tu proyecto, idea u oportunidad..."
          aria-required="true"
          aria-describedby={errors.message ? "contact-message-error" : undefined}
        />
        {errors.message && <span id="contact-message-error" className="contact__error">{errors.message}</span>}
      </div>

      {errors.submit && (
        <div className="contact__error-banner" role="alert" style={{ color: "#ef4444", fontSize: "0.9rem", marginBottom: "1rem" }}>
          {errors.submit}
        </div>
      )}

      <button
        type="submit"
        className="btn btn-primary btn-shine contact__submit"
        id="contact-submit"
        disabled={status === "loading"}
      >
        {status === "loading" ? (
          <><Loader2 size={18} className="contact__spinner" /> Enviando...</>
        ) : (
          <><Send size={18} /> Enviar Mensaje</>
        )}
      </button>
    </form>
  );
}

/* ─── Main ─────────────────────────────────────────────────────────────────── */
export default function Contact() {
  const headingRef = useReveal({ threshold: 0.2 });
  const infoRef    = useReveal({ threshold: 0.15 });
  const formRef    = useReveal({ threshold: 0.1 });

  return (
    <section id="contact" className="contact section">
      <div className="container">

        <div className="section-heading" ref={headingRef}>
          <div className="kicker">{CONTACT.kicker}</div>
          <h2>{CONTACT.titulo}</h2>
          <p>{CONTACT.descripcion}</p>
        </div>

        <div className="contact__grid">
          {/* Info */}
          <div className="contact__info reveal" ref={infoRef}>
            <div className="contact__links">
              {CONTACT.links.map((link) => (
                <ContactLink key={link.label} link={link} />
              ))}
            </div>
            <div className="contact__availability">
              <div className="contact__availability-dot" aria-hidden="true" />
              <span>Disponible para proyectos freelance y oportunidades full-time</span>
            </div>
          </div>

          {/* Form */}
          <div className="contact__form-wrapper reveal" ref={formRef}>
            <ContactForm />
          </div>
        </div>

      </div>
    </section>
  );
}
