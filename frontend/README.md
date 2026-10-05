# ⚛️ Frontend SPA — Portafolio Profesional

Single Page Application (SPA) moderna, reactiva y de alto rendimiento desarrollada con **React 19**, **Vite 8**, **React Router v7** y **CSS Vanilla modularizado** a través de un sistema integral de Tokens de Diseño.

---

## 🛠️ Stack Tecnológico

- **Core**: [React 19](https://react.dev/) + React DOM
- **Bundler & Tooling**: [Vite 8](https://vitejs.dev/) con `@vitejs/plugin-react`
- **Routing**: [React Router v7](https://reactrouter.com/) (`react-router-dom`)
- **Iconografía**: [Lucide React](https://lucide.dev/) (v1.47+) y componentes SVG inline
- **Linter**: [Oxlint](https://oxc.rs/) para análisis estático ultra rápido
- **Estilos**: Vanilla CSS con Custom Properties (`tokens.css`), Glassmorphism, animaciones CSS fluidas y diseño adaptativo Mobile-First.

---

## 📁 Estructura del Frontend

```text
frontend/
├── public/                 # Favicon y assets estáticos públicos
├── src/
│   ├── assets/             # Recursos multimedia y gráficos optimizados
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.jsx  # Navegación con scroll spy, mobile menu y toggle de tema
│   │   │   ├── Footer.jsx  # Enlaces rápidos, redes y copyright
│   │   │   └── ...
│   │   └── sections/
│   │       ├── Hero.jsx            # Presentación de impacto, tipografía dinámica y CTAs
│   │       ├── About.jsx           # Perfil profesional y métricas destacadas
│   │       ├── Skills.jsx          # Matriz de competencias técnicas e interactivas
│   │       ├── Projects.jsx        # Grid de proyectos con filtrado reactivo por categorías
│   │       ├── Certifications.jsx  # Galería de acreditaciones y enlaces a credenciales
│   │       ├── Timeline.jsx        # Trayectoria académica y laboral cronológica
│   │       └── Contact.jsx         # Formulario con validación y conexión al backend
│   ├── contexts/
│   │   └── ThemeContext.jsx# Proveedor de tema claro/oscuro persistido en localStorage
│   ├── data/
│   │   └── content.js      # Datos estáticos fallback del portafolio
│   ├── hooks/
│   │   ├── useCountUp.js   # Animación de contadores numéricos para estadísticas
│   │   └── useReveal.js    # Intersection Observer hook para animaciones al hacer scroll
│   ├── styles/
│   │   ├── tokens.css      # Variables de diseño (colores, espaciados, bordes, sombras)
│   │   └── animations.css  # Keyframes y transiciones reutilizables
│   ├── App.jsx             # Árbol raíz con Providers, enrutamiento y página 404
│   ├── index.css           # Reseteo global, estilos base y clases utilitarias
│   └── main.jsx            # Entry point de React (createRoot)
├── .env                    # Configuración de URLs de API
├── package.json            # Scripts y dependencias npm
└── vite.config.js          # Configuración del bundler Vite
```

---

## 🎨 Sistema de Diseño y Tokens

La aplicación implementa una arquitectura de tokens CSS en `src/styles/tokens.css` con soporte nativo para **Dark Mode** y **Light Mode**:

- **Variables de color**: Paleta semántica con variables para fondos, superficies translúcidas (glassmorphism con `backdrop-filter`), bordes y colores de acento por categoría técnica.
- **Tipografía**: Escala modular fluida con fuentes optimizadas para legibilidad en pantallas de alta densidad.
- **Animaciones**: Microinteracciones en hover, efectos `shine` en botones, y transiciones suaves gestionadas por hooks basados en `IntersectionObserver`.

---

## 🔌 Integración con el Backend

El componente [Contact.jsx](file:///c:/PROYECTOS/FRONTEND/2.%20Portafolio%20V2/frontend/src/components/sections/Contact.jsx) consume directamente la API del backend:

- Lee la variable `VITE_API_URL` definida en el archivo `.env`.
- Envía una petición `POST` al endpoint `/messages/` con el payload validado:
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "subject": "Oportunidad Laboral",
    "message": "Hola, me gustaría conversar sobre..."
  }
  ```
- Gestiona estados de la interfaz en tiempo real: `idle`, `loading` (spinner con feedback visual), `success` (confirmación con opción de reenvío) y `error` (renderizado de mensajes de validación y fallos de conexión).

---

## ⚙️ Configuración de Entorno (`.env`)

Crea un archivo `.env` en el directorio `frontend/`:

```env
# URL base de la API FastAPI (Backend)
VITE_API_URL=http://localhost:8000/api/v1
```

---

## 🚀 Scripts Disponibles

Asegúrate de contar con Node.js v18+ y un gestor de paquetes (`npm`, `pnpm` o `yarn`):

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo con HMR
npm run dev

# Compilar para producción (archivos optimizados en dist/)
npm run build

# Previsualizar el build de producción localmente
npm run preview

# Ejecutar el linter Oxlint
npm run lint
```

El servidor de desarrollo iniciará habitualmente en [http://localhost:5173](http://localhost:5173).
