# Nueva versión de Librero con Vue 3 + TypeScript

Estado: Propuesta
Responsable: [Asignar]
Rama sugerida: feature/vue3-ts
Objetivo: Implementar una nueva UI en Vue 3 + TypeScript dentro de `frontend/` con paridad de funcionalidades, manteniendo la app actual operativa durante la migración.

## Objetivos y alcance

- Reescribir la UI con Vue 3 + TypeScript.
- Mantener en paralelo la versión existente (vanilla JS).
- Migración incremental en pasos muy pequeños, con verificación tras cada paso.
- Integración con el backend actual:
  - POST `/api/recommend` (body: `{ "books_read": ["string"] }`)
  - GET `/health`
- Nuevo diseño (no es necesario mantener los colores actuales). Se usará un nuevo archivo de estilos base.

## Arquitectura y estructura

Nueva estructura dentro de `frontend/`:

```
frontend/
  static/                     # versión actual (se mantiene)
  vue/                        # nueva versión (Vue + TS)
    public/
      index.html
    src/
      assets/
        styles/
          base.css
      components/
        BookInput.vue
        ReadingHistory.vue
        RecommendButton.vue
      views/
        Home.vue
        Recommendations.vue
      services/
        api.ts
        bookStorage.ts
      stores/
        books.ts
      router/
        index.ts
      App.vue
      main.ts
    env.d.ts
    index.html                # si se usa Vite
    package.json
    tsconfig.json
    vite.config.ts
```

Herramientas:
- Build: Vite
- Marco: Vue 3 + TypeScript
- Estado: Pinia
- Router: Vue Router
- Testing: Vitest + Vue Test Utils (posterior)
- Linter/Formatter: ESLint + Prettier (preset de Vite)

## Prerrequisitos

- Node 18+
- Backend corriendo en 8000 (o actualizar proxy del dev server)
- Docker/Nginx para producción (opcional más adelante)

## Plan incremental (pasos pequeños con verificación)

Cada paso termina con una verificación rápida, para evitar romper la app actual.

### Paso 1 — Bootstrap del proyecto Vue + TS
1. Crear carpeta `frontend/vue`.
2. Inicializar proyecto con Vite:
   ```
   cd frontend
   npm create vite@latest vue -- --template vue-ts
   # o: npm create vite@latest
   #   -> framework: Vue
   #   -> variant: TypeScript
   mv vue ./vue
   cd vue
   npm install
   ```
3. Agregar Pinia y Vue Router:
   ```
   npm i pinia vue-router
   npm i -D @types/node
   ```

Verificación:
- `cd frontend/vue && npm run dev`
- Abrir http://localhost:5173 y ver la pantalla base de Vite + Vue.

### Paso 2 — Router básico y dos vistas
1. Crear `src/router/index.ts` con rutas `/` (Home) y `/recommendations`.
2. Crear `src/views/Home.vue` y `src/views/Recommendations.vue`.
3. En `main.ts`, registrar el router.

Verificación:
- Navegar entre `/` y `/recommendations` en el dev server de Vite.

### Paso 3 — Estilos base nuevos
1. Crear `src/assets/styles/base.css` con el nuevo look & feel (colores y tipografía libres).
2. Importar en `main.ts`:
   ```ts
   import '@/assets/styles/base.css';
   ```

Verificación:
- Se ve el nuevo estilo en ambas vistas.

### Paso 4 — Servicio de almacenamiento (equivalente a bookStorage)
1. Crear `src/services/bookStorage.ts`:
   ```ts
   export const bookStorage = {
     getBooks(): string[] {
       const json = localStorage.getItem('librero_books');
       return json ? JSON.parse(json) : [];
     },
     saveBook(title: string): boolean {
       if (!title) return false;
       const books = this.getBooks();
       if (books.includes(title)) return false;
       books.push(title);
       localStorage.setItem('librero_books', JSON.stringify(books));
       return true;
     },
     clearBooks(): void {
       localStorage.removeItem('librero_books');
     },
   };
   ```
2. No borrar aún [frontend/static/services/bookStorage.js](cci:7://file:///Users/jlr/CascadeProjects/windsurf-project/librero_app/frontend/static/services/bookStorage.js:0:0-0:0).

Verificación:
- Desde la consola del dev server, probar importación en un componente temporal.

### Paso 5 — Componentes atómicos
- `components/BookInput.vue`: input con v-model y evento `book-added` al guardar.
- `components/ReadingHistory.vue`: lista de libros y botón “Clear History”.
- `components/RecommendButton.vue`: botón de “Recommend a Book”, disabled durante carga.

Verificación:
- Renderizar los componentes en `Recommendations.vue` con datos locales y asegurar que el estado se actualiza en pantalla.

### Paso 6 — Estado con Pinia
1. Crear `stores/books.ts`:
   ```ts
   import { defineStore } from 'pinia';

   export const useBooksStore = defineStore('books', {
     state: () => ({
       books: [] as string[],
       recommendation: null as string | null,
       loading: false as boolean,
       error: null as string | null,
       totalBooks: 0 as number,
     }),
     getters: {
       lastBook: (state) => state.books[state.books.length - 1] ?? null,
     },
     actions: {
       loadBooks() {
         const json = localStorage.getItem('librero_books');
         this.books = json ? JSON.parse(json) : [];
       },
       addBook(title: string) {
         if (!title || this.books.includes(title)) return false;
         this.books.push(title);
         localStorage.setItem('librero_books', JSON.stringify(this.books));
         return true;
       },
       clearBooks() {
         this.books = [];
         localStorage.removeItem('librero_books');
       },
     },
   });
   ```
2. Conectar store a `BookInput.vue` y `ReadingHistory.vue`.

Verificación:
- Al añadir/limpiar libros en Vue, el estado persiste y la UI reacciona.

### Paso 7 — Servicio de API
1. Crear `src/services/api.ts`:
   ```ts
   const API_URL = window.location.origin; // o importar de env

   export async function recommend(booksRead: string[]) {
     const res = await fetch(`${API_URL}/api/recommend`, {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ books_read: booksRead }),
     });
     if (!res.ok) throw new Error(`HTTP ${res.status}`);
     return res.json() as Promise<{ recommendation: string; message: string; total_books: number }>;
   }

   export async function health() {
     const res = await fetch(`${API_URL}/health`);
     return res.ok;
   }
   ```
2. Consumirlo en `Recommendations.vue` (o agregar acción en Pinia para [getRecommendation](cci:1://file:///Users/jlr/CascadeProjects/windsurf-project/librero_app/frontend/static/app.js:38:0-107:1)).

Verificación:
- Click en “Recommend a Book” muestra el resultado, maneja loading y errores.

### Paso 8 — Paralelo con la versión actual
- Mantener la versión actual en `frontend/static/`.
- Para producción con Nginx, servir Vue bajo `/vue/` y la app actual en `/`.
- Para dev, usar Vite con proxy a `/api`.

Verificación:
- Ambas versiones accesibles. Enlace “Probar nueva versión” en la landing actual.

### Paso 9 — Tests (opcional por ahora)
- Vitest + Vue Test Utils para componentes.
- Casos: `BookInput.vue` guarda correctamente, `ReadingHistory.vue` muestra libros, `Recommendations.vue` integra API.

### Paso 10 — Ajustes finales y limpieza
- Paridad de funcionalidades con la versión legacy.
- Feedback visual y UX.
- Cuando la versión Vue supere validación, plan para retirar gradualmente la legacy.

## Notas de estilo (nuevo CSS)

- Base simple en `src/assets/styles/base.css`, ejemplo:
  ```css
  :root {
    --bg: #0f172a;
    --panel: #111827;
    --text: #e5e7eb;
    --accent: #22d3ee;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica Neue, Arial, "Apple Color Emoji", "Segoe UI Emoji";
    background: linear-gradient(180deg, var(--bg), #0b1220);
    color: var(--text);
  }
  .container {
    max-width: 960px;
    margin: 0 auto;
    padding: 24px;
  }
  .card {
    background: var(--panel);
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,.35);
  }
  .btn {
    background: var(--accent);
    color: #041016;
    border: 0;
    padding: 12px 18px;
    border-radius: 999px;
    cursor: pointer;
    transition: transform .08s ease;
  }
  .btn:active { transform: translateY(1px); }
  input {
    width: 100%;
    padding: 12px 14px;
    border-radius: 10px;
    border: 1px solid #334155;
    background: #0b1220;
    color: var(--text);
  }
  ul { list-style: none; padding: 0; margin: 0; }
  ```

## Integración con Nginx (producción)

Ejemplo conceptual:
```
location /vue/ {
  alias /usr/share/nginx/html/vue/;
  try_files $uri $uri/ /vue/index.html;
}
location / {
  root /usr/share/nginx/html;
  index index.html;
  try_files $uri $uri/ /index.html;
}
location /api/ {
  proxy_pass http://backend:8000;
}
```

## Comandos útiles

- Desarrollo (Vue):
  ```
  cd frontend/vue
  npm install
  npm run dev
  ```
- Build:
  ```
  npm run build
  ```
  Copiar salida a `/usr/share/nginx/html/vue` en la imagen final.

## Criterios de aceptación

- La vista de Recomendaciones muestra:
  - Input para último libro leído.
  - Historial persistente con localStorage.
  - Botón “Recommend a Book” con estados loading/disabled.
  - Manejo de error y mensaje del backend.
- Navegación entre Home y Recommendations.
- La versión actual continúa operativa durante la migración.
- Documentación de pasos de despliegue y rollback.

## Rollback

- Mantener rama `feature/vue3-ts` separada hasta validación completa.
- Deshabilitar `/vue/` en Nginx para volver a la versión legacy si es necesario.

---
Checklist de implementación (marcar durante el desarrollo):

- [ ] Vite + Vue + TS inicial
- [ ] Router con Home/Recommendations
- [ ] Estilos base
- [ ] Servicio `bookStorage.ts`
- [ ] Componentes: `BookInput`, `ReadingHistory`, `RecommendButton`
- [ ] Pinia store `books.ts`
- [ ] Servicio API (`recommend`, `health`)
- [ ] Integración en `Recommendations.vue`
- [ ] Deploy paralelo con Nginx (`/vue/`)
- [ ] Pruebas y validación
