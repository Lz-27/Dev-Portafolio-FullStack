/**
 * ============================================
 * PORTAFOLIO — FUENTE ÚNICA DE VERDAD
 * ============================================
 * Todos los textos, datos y configuración del portafolio
 * residen aquí. Los componentes SOLO consumen este archivo.
 * Patrón: REDSAM Technical Reference §2.1
 */

export const PERSONAL = {
  nombre: "Tu Nombre Completo",
  titulo: "Ingeniero de Sistemas",
  subtitulo: "Full Stack Developer & Data Science Specialist",
  eslogan: "Transformando Datos en Soluciones Inteligentes",
  descripcion:
    "Ingeniero de Sistemas especializado en desarrollo Full Stack, Ciencia de Datos y Machine Learning. Creo experiencias digitales innovadoras y modelos predictivos de alto impacto con arquitecturas escalables.",
  email: "keloiso271714@gmail.com",
  telefono: "+51939943007",
  ubicacion: "Lima, Perú",
  cv: "https://drive.google.com/file/d/TU_ID_AQUI/view",
};

export const SOCIAL = {
  github: "https://github.com/tu-usuario",
  linkedin: "https://linkedin.com/in/tu-perfil",
  whatsapp: "https://wa.me/51939943007",
  telegram: "https://t.me/tu-usuario",
  instagram: "https://instagram.com/tu-usuario",
  email: "mailto:keloiso271714@gmail.com",
};

export const STATS = [
  { value: 3, suffix: "+", label: "Años de Experiencia" },
  { value: 15, suffix: "+", label: "Proyectos Completados" },
  { value: 10, suffix: "+", label: "Certificaciones" },
  { value: 20, suffix: "+", label: "Tecnologías" },
];

// ─── SKILLS ───────────────────────────────────────────────────────────────────

export const SKILLS_CATEGORIES = [
  {
    id: "languages",
    label: "Lenguajes",
    icon: "Code2",
    skills: [
      { name: "Python", icon: "🐍", level: 90, color: "#3776AB" },
      { name: "JavaScript", icon: "⚡", level: 85, color: "#F7DF1E" },
      { name: "TypeScript", icon: "🔷", level: 80, color: "#3178C6" },
      { name: "SQL", icon: "🗄️", level: 85, color: "#336791" },
      { name: "Java", icon: "☕", level: 75, color: "#ED8B00" },
    ],
  },
  {
    id: "frontend",
    label: "Frontend",
    icon: "Monitor",
    skills: [
      { name: "React", icon: "⚛️", level: 88, color: "#61DAFB" },
      { name: "Next.js", icon: "▲", level: 78, color: "#FFFFFF" },
      { name: "CSS / Tailwind", icon: "🎨", level: 85, color: "#38BDF8" },
      { name: "HTML5", icon: "🌐", level: 90, color: "#E34F26" },
    ],
  },
  {
    id: "backend",
    label: "Backend",
    icon: "Server",
    skills: [
      { name: "FastAPI", icon: "🚀", level: 82, color: "#009688" },
      { name: "Node.js", icon: "🟩", level: 80, color: "#339933" },
      { name: "Django", icon: "🎸", level: 75, color: "#092E20" },
      { name: "Express", icon: "🔧", level: 76, color: "#FFFFFF" },
    ],
  },
  {
    id: "data",
    label: "Data & ML",
    icon: "BrainCircuit",
    skills: [
      { name: "TensorFlow", icon: "🧠", level: 85, color: "#FF6F00" },
      { name: "PyTorch", icon: "🔥", level: 80, color: "#EE4C2C" },
      { name: "Pandas", icon: "🐼", level: 92, color: "#150458" },
      { name: "Scikit-Learn", icon: "📊", level: 87, color: "#F7931E" },
      { name: "OpenCV", icon: "👁️", level: 78, color: "#5C3EE8" },
    ],
  },
  {
    id: "tools",
    label: "Bases & Herramientas",
    icon: "Wrench",
    skills: [
      { name: "PostgreSQL", icon: "🐘", level: 85, color: "#336791" },
      { name: "MongoDB", icon: "🍃", level: 76, color: "#47A248" },
      { name: "Docker", icon: "🐳", level: 80, color: "#2496ED" },
      { name: "Git", icon: "🌿", level: 88, color: "#F05032" },
      { name: "AWS", icon: "☁️", level: 70, color: "#FF9900" },
    ],
  },
];

// Marquee ticker — tecnologías para la animación de banda inferior
export const TECH_TICKER = [
  "Python", "React", "FastAPI", "TensorFlow", "Node.js",
  "PostgreSQL", "Docker", "TypeScript", "PyTorch", "Django",
  "MongoDB", "AWS", "Git", "OpenCV", "Pandas", "NumPy",
  "Scikit-Learn", "Next.js", "GraphQL", "Redis",
];

// ─── CERTIFICATIONS ───────────────────────────────────────────────────────────

export const CERT_CATEGORIES = [
  { id: "all",       label: "Todas" },
  { id: "data",      label: "Data & IA" },
  { id: "cloud",     label: "Cloud" },
  { id: "dev",       label: "Desarrollo" },
  { id: "other",     label: "Otras" },
];

export const CERTIFICATIONS = [
  {
    id: 1,
    titulo: "Universidad Desarrollo Web",
    emisor: "DataCamp",
    fecha: "2022",
    categoria: "data",
    categoriaLabel: "Data & IA",
    imagen: "/certificados/Universidad Desarrollo Web (30h).jpg",
    credencial: "https://www.datacamp.com",
    descripcion: "Certificación integral en Data Science cubriendo estadística, machine learning, deep learning y visualización de datos con Python.",
    habilidades: ["Python", "Machine Learning", "Statistics", "Deep Learning"],
  },
  {
    id: 2,
    titulo: "AWS Cloud Practitioner",
    emisor: "Amazon Web Services",
    fecha: "2023",
    categoria: "cloud",
    categoriaLabel: "Cloud",
    imagen: null,
    credencial: "https://aws.amazon.com/certification/",
    descripcion: "Fundamentos de servicios cloud de AWS: computación, almacenamiento, redes, seguridad y arquitectura de soluciones.",
    habilidades: ["AWS", "Cloud Computing", "S3", "EC2", "IAM"],
  },
  {
    id: 3,
    titulo: "TensorFlow Developer Certificate",
    emisor: "Google",
    fecha: "2023",
    categoria: "data",
    categoriaLabel: "Data & IA",
    imagen: null,
    credencial: "https://www.tensorflow.org/certificate",
    descripcion: "Construcción y entrenamiento de modelos de deep learning para visión computacional, NLP y series temporales.",
    habilidades: ["TensorFlow", "Deep Learning", "NLP", "Computer Vision"],
  },
  {
    id: 4,
    titulo: "React Developer Certification",
    emisor: "Meta",
    fecha: "2022",
    categoria: "dev",
    categoriaLabel: "Desarrollo",
    imagen: null,
    credencial: "https://www.coursera.org/professional-certificates/meta-front-end-developer",
    descripcion: "Dominio del ecosistema React: hooks, context, routing, state management y optimización de rendimiento.",
    habilidades: ["React", "JavaScript", "Redux", "REST APIs"],
  },
  {
    id: 5,
    titulo: "Python for Everybody Specialization",
    emisor: "University of Michigan",
    fecha: "2021",
    categoria: "dev",
    categoriaLabel: "Desarrollo",
    imagen: null,
    credencial: "https://www.coursera.org/specializations/python",
    descripcion: "Especialización completa en Python abarcando desde fundamentos hasta bases de datos, web scraping y APIs.",
    habilidades: ["Python", "SQL", "Web Scraping", "APIs"],
  },
  {
    id: 6,
    titulo: "Docker & Kubernetes Essentials",
    emisor: "Linux Foundation",
    fecha: "2023",
    categoria: "cloud",
    categoriaLabel: "Cloud",
    imagen: null,
    credencial: "https://training.linuxfoundation.org",
    descripcion: "Containerización de aplicaciones con Docker y orquestación de servicios con Kubernetes en entornos de producción.",
    habilidades: ["Docker", "Kubernetes", "CI/CD", "DevOps"],
  },
];

// ─── PROJECTS ─────────────────────────────────────────────────────────────────

export const PROJECT_CATEGORIES = [
  { id: "all",      label: "Todos" },
  { id: "frontend", label: "Frontend" },
  { id: "fullstack",label: "Full-Stack" },
  { id: "data",     label: "Data / IA" },
  { id: "desktop",  label: "Desktop" },
  { id: "backend",  label: "Backend" },
];

export const PROJECTS = [
  {
    id: 1,
    slug: "sistema-prediccion-ventas",
    titulo: "Sistema de Predicción de Ventas",
    descripcion: "Modelo ML para predecir ventas con series temporales y análisis de tendencias.",
    detalles: "Desarrollo completo de un sistema de predicción de ventas usando Python, TensorFlow y FastAPI. El modelo alcanza 94% de precisión en predicciones a 30 días utilizando LSTM y técnicas de feature engineering avanzadas.",
    categoria: "data",
    categoriaLabel: "Data / IA",
    imagen: null, // Se generará
    imagenes: [],
    tecnologias: ["Python", "TensorFlow", "FastAPI", "React", "PostgreSQL"],
    github: "https://github.com/tu-usuario/proyecto",
    demo: "https://demo.com",
    destacado: true,
  },
  {
    id: 2,
    slug: "dashboard-analisis-realtime",
    titulo: "Dashboard de Análisis en Tiempo Real",
    descripcion: "Visualización interactiva de métricas y datos con WebSockets y D3.js.",
    detalles: "Dashboard interactivo construido con React y D3.js que procesa datos en tiempo real desde múltiples fuentes vía WebSockets. Maneja hasta 10,000 eventos/segundo con latencia sub-100ms.",
    categoria: "fullstack",
    categoriaLabel: "Full-Stack",
    imagen: null,
    imagenes: [],
    tecnologias: ["React", "Node.js", "D3.js", "WebSockets", "MongoDB"],
    github: "https://github.com/tu-usuario/proyecto",
    demo: "https://demo.com",
    destacado: true,
  },
  {
    id: 3,
    slug: "plataforma-ecommerce",
    titulo: "Plataforma E-Commerce",
    descripcion: "Tienda online completa con gestión de inventario, pagos y panel admin.",
    detalles: "Sistema e-commerce full-stack con React en el frontend y FastAPI+SQLAlchemy en el backend. Incluye autenticación JWT, gestión de pedidos, integración con pasarelas de pago y panel administrativo CMS.",
    categoria: "fullstack",
    categoriaLabel: "Full-Stack",
    imagen: null,
    imagenes: [],
    tecnologias: ["React", "FastAPI", "SQLAlchemy", "PostgreSQL", "JWT"],
    github: "https://github.com/tu-usuario/proyecto",
    demo: "https://demo.com",
    destacado: true,
  },
  {
    id: 4,
    slug: "vision-computacional-defectos",
    titulo: "Detección de Defectos con Vision Computacional",
    descripcion: "Sistema automatizado de control de calidad usando OpenCV y CNN.",
    detalles: "Pipeline de procesamiento de imágenes que detecta defectos en líneas de manufactura con 97% de precisión. Usa CNNs personalizadas y OpenCV para segmentación y clasificación en tiempo real.",
    categoria: "data",
    categoriaLabel: "Data / IA",
    imagen: null,
    imagenes: [],
    tecnologias: ["Python", "OpenCV", "PyTorch", "FastAPI", "Docker"],
    github: "https://github.com/tu-usuario/proyecto",
    demo: null,
    destacado: false,
  },
  {
    id: 5,
    slug: "gestor-inventario-pyqt6",
    titulo: "Gestor de Inventario Desktop",
    descripcion: "Aplicación de escritorio para control de stock con reportes y alertas.",
    detalles: "Aplicación de escritorio desarrollada con PyQt6 y SQLite. Incluye generación de reportes en PDF, sistema de alertas por bajo stock, dashboard visual con gráficos y exportación a Excel.",
    categoria: "desktop",
    categoriaLabel: "Desktop",
    imagen: null,
    imagenes: [],
    tecnologias: ["Python", "PyQt6", "SQLite", "Matplotlib", "ReportLab"],
    github: "https://github.com/tu-usuario/proyecto",
    demo: null,
    destacado: false,
  },
  {
    id: 6,
    slug: "api-microservicios",
    titulo: "Arquitectura de Microservicios",
    descripcion: "API gateway con servicios independientes orquestados con Docker Compose.",
    detalles: "Arquitectura de microservicios con FastAPI donde cada dominio (usuarios, pedidos, notificaciones) es un servicio independiente. Comunicación via REST y mensajería con Redis. Orquestado con Docker Compose.",
    categoria: "backend",
    categoriaLabel: "Backend",
    imagen: null,
    imagenes: [],
    tecnologias: ["FastAPI", "Docker", "Redis", "PostgreSQL", "JWT"],
    github: "https://github.com/tu-usuario/proyecto",
    demo: null,
    destacado: false,
  },
];

// ─── TIMELINE ─────────────────────────────────────────────────────────────────

export const TIMELINE = [
  {
    id: 1,
    tipo: "trabajo",
    titulo: "Full Stack Developer",
    empresa: "Tu Empresa Actual",
    periodo: "2024 — Presente",
    descripcion: "Desarrollo de aplicaciones web con React y FastAPI. Implementación de pipelines de datos y modelos ML en producción.",
    tecnologias: ["React", "FastAPI", "Python", "PostgreSQL"],
  },
  {
    id: 2,
    tipo: "trabajo",
    titulo: "Data Analyst",
    empresa: "Empresa Anterior",
    periodo: "2022 — 2024",
    descripcion: "Análisis de datos de negocio, creación de dashboards y modelos predictivos para optimizar decisiones estratégicas.",
    tecnologias: ["Python", "Pandas", "Power BI", "SQL"],
  },
  {
    id: 3,
    tipo: "educacion",
    titulo: "Ingeniería de Sistemas",
    empresa: "Universidad Nacional",
    periodo: "2018 — 2023",
    descripcion: "Graduado con honores. Especialización en Ciencia de Datos e Inteligencia Artificial. Tesis sobre predicción de series temporales con Deep Learning.",
    tecnologias: ["Algorithms", "Machine Learning", "Software Engineering"],
  },
  {
    id: 4,
    tipo: "educacion",
    titulo: "Certificación Data Science",
    empresa: "DataCamp",
    periodo: "2022",
    descripcion: "Professional Data Scientist Certificate. Cubre estadística, machine learning, deep learning y visualización de datos.",
    tecnologias: ["Python", "ML", "Statistics", "Deep Learning"],
  },
];

// ─── ABOUT ────────────────────────────────────────────────────────────────────

export const ABOUT = {
  titulo: "Sobre Mí",
  kicker: "¿Quién soy?",
  parrafos: [
    "Soy Ingeniero de Sistemas con profunda pasión por construir software que importa. Me especializo en el puente entre el análisis de datos y las interfaces de usuario: creo sistemas que no solo funcionan, sino que deleitan.",
    "Mi enfoque combina principios de Clean Code, arquitecturas SOLID y diseño centrado en el usuario. Cada línea de código que escribo tiene un propósito — resolver un problema real con elegancia técnica.",
  ],
  fortalezas: [
    { icon: "Code2",       label: "Clean Architecture" },
    { icon: "BrainCircuit",label: "Machine Learning" },
    { icon: "Layers",      label: "Full Stack" },
    { icon: "Zap",         label: "Performance" },
  ],
  softSkills: [
    "Pensamiento Analítico",
    "Resolución de Problemas",
    "Trabajo en Equipo",
    "Comunicación Efectiva",
    "Liderazgo Técnico",
    "Aprendizaje Continuo",
  ],
};

// ─── CONTACT ──────────────────────────────────────────────────────────────────

export const CONTACT = {
  titulo: "¿Hablamos?",
  kicker: "Contacto",
  descripcion: "Estoy disponible para proyectos freelance, consultoría y oportunidades laborales. Respondo en menos de 24 horas.",
  links: [
    { label: "Email",     icon: "Mail",     href: "mailto:keloiso271714@gmail.com", value: "keloiso271714@gmail.com" },
    { label: "LinkedIn",  icon: "Linkedin", href: "https://linkedin.com/in/tu-perfil", value: "linkedin.com/in/tu-perfil" },
    { label: "GitHub",    icon: "Github",   href: "https://github.com/tu-usuario", value: "github.com/tu-usuario" },
    { label: "Telegram",  icon: "Send",     href: "https://t.me/tu-usuario", value: "@tu-usuario" },
    { label: "WhatsApp",  icon: "MessageCircle", href: "https://wa.me/51 939943007", value: "+51 939 943 007" },
  ],
};

// ─── SITE META ────────────────────────────────────────────────────────────────

export const SITE = {
  titulo: "Tu Nombre — Full Stack Developer & Data Science",
  descripcion: "Portafolio profesional de Ingeniero de Sistemas especializado en Full Stack Development, Data Science & Machine Learning",
  url: "https://tu-dominio.com",
  idioma: "es",
  temaDefault: "dark",
};
