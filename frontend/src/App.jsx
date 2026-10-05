/**
 * App.jsx — Orquestador principal
 * Provider tree: ThemeProvider → BrowserRouter → App UI
 * Patrón: TECHNICAL_GUIDE.md §3.1
 */
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { ThemeProvider } from "./contexts/ThemeContext";
import Navbar  from "./components/layout/Navbar";
import Footer  from "./components/layout/Footer";
import Hero    from "./components/sections/Hero";
import About   from "./components/sections/About";
import Skills  from "./components/sections/Skills";
import Projects from "./components/sections/Projects";
import Certifications from "./components/sections/Certifications";
import Timeline from "./components/sections/Timeline";
import Contact from "./components/sections/Contact";
import "./index.css";

/** Página principal — portafolio público */
function HomePage() {
  return (
    <main>
      <Hero />
      <About />
      <Skills />
      <Projects />
      <Certifications />
      <Timeline />
      <Contact />
    </main>
  );
}

/** Página 404 */
function NotFound() {
  return (
    <main style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      minHeight: "60vh",
      gap: "1rem",
      textAlign: "center",
      padding: "2rem",
    }}>
      <h1 style={{ fontSize: "6rem", lineHeight: 1, color: "var(--brand-primary)" }}>404</h1>
      <p style={{ color: "var(--text-secondary)", fontSize: "1.125rem" }}>
        Esta página no existe.
      </p>
      <a href="/" className="btn btn-primary btn-shine">Volver al inicio</a>
    </main>
  );
}

/** Root con providers */
export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </ThemeProvider>
  );
}
