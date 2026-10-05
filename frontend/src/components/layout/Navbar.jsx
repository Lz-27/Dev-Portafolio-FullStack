/**
 * Navbar — Header inteligente con scroll, theme switcher y mobile drawer
 * Patrón: TECHNICAL_GUIDE.md §6 + §6.4
 */
import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import {
  Download, Menu, Moon, Sun, Waves, X,
} from "lucide-react";

// lucide-react v1.47 no incluye Github/Linkedin — SVGs inline
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
import { useScrolled } from "../../hooks/useScrolled";
import { useTheme } from "../../contexts/ThemeContext";
import { PERSONAL, SOCIAL } from "../../data/content";
import "./Navbar.css";

const NAV_LINKS = [
  { href: "#home",             label: "Inicio" },
  { href: "#about",            label: "Sobre Mí" },
  { href: "#skills",           label: "Habilidades" },
  { href: "#projects",         label: "Proyectos" },
  { href: "#certifications",   label: "Certificaciones" },
  { href: "#timeline",         label: "Experiencia" },
  { href: "#contact",          label: "Contacto" },
];

// Icono del tema actual — rota entre 3 temas
function ThemeIcon({ theme }) {
  if (theme === "light")  return <Sun size={18} aria-hidden="true" />;
  if (theme === "navy")   return <Waves size={18} aria-hidden="true" />;
  return <Moon size={18} aria-hidden="true" />;
}

function ThemeLabel(theme) {
  if (theme === "dark")  return "Modo oscuro";
  if (theme === "light") return "Modo claro";
  return "Modo navy";
}

export default function Navbar() {
  const { scrolled } = useScrolled(20);
  const { theme, cycleTheme } = useTheme();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [activeSection, setActiveSection] = useState("home");
  const drawerRef = useRef(null);
  const location = useLocation();

  // Cierra drawer en cambio de ruta — patrón §6.4
  useEffect(() => {
    setMobileOpen(false);
  }, [location]);

  // Bloquea scroll cuando drawer está abierto
  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [mobileOpen]);

  // Detecta sección activa en scroll
  useEffect(() => {
    const sections = NAV_LINKS.map((l) => l.href.slice(1));
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActiveSection(e.target.id);
        });
      },
      { threshold: 0.4, rootMargin: `-${PERSONAL.headerHeight ?? 80}px 0px 0px 0px` }
    );
    sections.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, []);

  // Cierra drawer al click fuera
  useEffect(() => {
    if (!mobileOpen) return;
    const handler = (e) => {
      if (drawerRef.current && !drawerRef.current.contains(e.target)) {
        setMobileOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [mobileOpen]);

  const handleNavClick = (e, href) => {
    e.preventDefault();
    const target = document.querySelector(href);
    if (target) target.scrollIntoView({ behavior: "smooth" });
    setMobileOpen(false);
  };

  return (
    <>
      <header className={`navbar${scrolled ? " navbar--scrolled" : ""}`} role="banner">
        <div className="container navbar__inner">

          {/* ── Logo ── */}
          <a
            href="#home"
            className="navbar__logo"
            onClick={(e) => handleNavClick(e, "#home")}
            aria-label="Ir al inicio"
          >
            <span className="navbar__logo-bracket">&lt;</span>
            <span className="navbar__logo-text">Dev</span>
            <span className="navbar__logo-accent">Portfolio</span>
            <span className="navbar__logo-bracket">/&gt;</span>
          </a>

          {/* ── Nav Links (desktop) ── */}
          <nav className="navbar__nav" aria-label="Navegación principal">
            <ul className="navbar__links" role="list">
              {NAV_LINKS.map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    className={`navbar__link${activeSection === link.href.slice(1) ? " navbar__link--active" : ""}`}
                    onClick={(e) => handleNavClick(e, link.href)}
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          {/* ── Actions ── */}
          <div className="navbar__actions">
            {/* Theme Switcher */}
            <button
              id="theme-toggle"
              className="navbar__theme-btn"
              onClick={cycleTheme}
              aria-label={`Cambiar tema. Tema actual: ${ThemeLabel(theme)}`}
              title={`Tema: ${theme}`}
            >
              <ThemeIcon theme={theme} />
              <span className="navbar__theme-label">{theme}</span>
            </button>

            {/* GitHub */}
            <a
              href={SOCIAL.github}
              target="_blank"
              rel="noopener noreferrer"
              className="navbar__icon-btn"
              aria-label="GitHub"
            >
              <GithubIcon size={20} />
            </a>

            {/* LinkedIn */}
            <a
              href={SOCIAL.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="navbar__icon-btn"
              aria-label="LinkedIn"
            >
              <LinkedinIcon size={20} />
            </a>

            {/* Descargar CV */}
            <a
              href={PERSONAL.cv}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary btn-shine navbar__cv-btn"
              aria-label="Descargar CV"
            >
              <Download size={16} />
              <span>CV</span>
            </a>

            {/* Hamburger */}
            <button
              className={`navbar__hamburger${mobileOpen ? " navbar__hamburger--open" : ""}`}
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-label={mobileOpen ? "Cerrar menú" : "Abrir menú"}
              aria-expanded={mobileOpen}
            >
              {mobileOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>
      </header>

      {/* ── Spacer (evita content jump) ── */}
      <div style={{ height: "var(--header-height)" }} aria-hidden="true" />

      {/* ── Mobile Drawer — patrón §6.4 ── */}
      <div
        className={`navbar__overlay${mobileOpen ? " navbar__overlay--visible" : ""}`}
        aria-hidden="true"
        onClick={() => setMobileOpen(false)}
      />
      <nav
        ref={drawerRef}
        className={`navbar__drawer${mobileOpen ? " navbar__drawer--open" : ""}`}
        aria-label="Menú móvil"
      >
        <ul className="navbar__drawer-links" role="list">
          {NAV_LINKS.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className={`navbar__drawer-link${activeSection === link.href.slice(1) ? " navbar__drawer-link--active" : ""}`}
                onClick={(e) => handleNavClick(e, link.href)}
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="navbar__drawer-footer">
          <a href={SOCIAL.github}   target="_blank" rel="noopener noreferrer" className="navbar__icon-btn"><GithubIcon  size={22}/></a>
          <a href={SOCIAL.linkedin} target="_blank" rel="noopener noreferrer" className="navbar__icon-btn"><LinkedinIcon size={22}/></a>
          <a href={PERSONAL.cv}     target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-shine">
            <Download size={16}/> Descargar CV
          </a>
        </div>
      </nav>
    </>
  );
}
