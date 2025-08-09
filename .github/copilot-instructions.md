# GitHub Copilot Instructions

These instructions guide GitHub Copilot to always generate code following our best practices for **React**, **FastAPI**, **WebSockets**, and general programming.

---

## 1. General Programming Best Practices

- Always **follow SOLID principles** and **DRY** (Don’t Repeat Yourself).
- Use **clear and descriptive variable/function names** (no abbreviations unless standard).
- Follow **PEP8 for Python** and **Airbnb Style Guide for JavaScript/React**.
- Add **docstrings** and **inline comments** where necessary, especially for complex logic.
- Always validate **user inputs** and **sanitize outputs**.
- Avoid hardcoding secrets — use **environment variables** and `.env` files.
- Ensure **error handling** with clear error messages and appropriate status codes.
- Prefer **async/await** for asynchronous code over callbacks or `.then()` chains.
- Use **logging** instead of `print` statements for production-ready applications.
- Optimize for **readability first**, performance second (but avoid obvious inefficiencies).

---

## 2. React Best Practices

- Use **functional components** with React Hooks (`useState`, `useEffect`, `useMemo`, `useCallback`).
- Keep components **small and reusable**.
- Extract **business logic** into custom hooks instead of bloating components.
- Use **TypeScript** for type safety whenever possible.
- Manage global state with **React Context** or a state library (Zustand, Redux Toolkit) only if necessary.
- Use **prop-types** (JS) or TypeScript interfaces (TS) for all components.
- Handle **loading** and **error states** in UI.
- Optimize renders using **React.memo** and `useMemo` where applicable.
- Avoid inline styles — use CSS modules, TailwindCSS, or styled-components.
- Ensure **accessibility (a11y)**: semantic HTML, ARIA labels, keyboard navigation.
- For API calls, use `fetch` or Axios in a `useEffect` or custom hook, **never directly in the render**.

---

## 3. FastAPI Best Practices

- Use **Pydantic models** for request validation and response schemas.
- Organize code using **routers** (`app/routers/`) and **services** (`app/services/`).
- Follow **async-first** approach for endpoints where possible.
- Use **dependency injection** for database connections, authentication, and config.
- Return **standardized response formats** (success, error, data).
- Implement **CORS middleware** with explicit allowed origins.
- Use **background tasks** for non-blocking jobs.
- Implement **JWT authentication** or OAuth2 for secure endpoints.
- Separate **configuration** into environment-based settings files.
- Always include **OpenAPI documentation** using FastAPI’s built-in annotations.

---

## 4. WebSockets Best Practices

- Use **async WebSocket handlers** for non-blocking communication.
- Always **authenticate WebSocket connections** before accepting messages.
- Handle **connection lifecycle events** (`connect`, `disconnect`, `error`) gracefully.
- Avoid sending sensitive data unless encrypted.
- Implement **heartbeat/ping-pong** messages to keep connections alive.
- Handle **reconnection logic** on the client side.
- Limit **message size** and validate incoming messages.
- Broadcast messages efficiently using **channels or rooms**.
- Use a **message schema** (JSON format with `type` and `payload`) for clarity.

---

## 5. Testing & Quality

- Write **unit tests** for core logic and **integration tests** for API/websocket flows.
- Use **pytest** for Python and **Jest/React Testing Library** for React.
- Aim for **minimum 80% coverage** for critical modules.
- Always run tests before committing code.
- Use **Prettier** + **ESLint** (React) and **black** + **flake8** (Python) for consistent formatting.
- Configure **CI/CD pipelines** to enforce tests, linting, and security scans.

---

## 6. Security Practices

- Never commit secrets, API keys, or database credentials.
- Validate **all incoming data** — both client and server side.
- Use **HTTPS** in production.
- Escape/encode output to prevent XSS.
- Use **parameterized queries** to prevent SQL injection.
- Enable **rate limiting** for APIs and WebSocket connections.
- Keep dependencies updated and scan for vulnerabilities regularly.

---

**End of Instructions**
