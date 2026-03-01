# Auth System + Frontend Redesign Plan

## Phase 1: Backend Auth Foundation

### New dependencies (`pyproject.toml`)
- `PyJWT` for JWT token encoding/decoding
- `passlib[bcrypt]` for password hashing

### New files
- `api/app/db/models.py` — Add `User` model (id, email, password_hash, created_at)
- `api/app/core/config.py` — Add `jwt_secret: str` and `jwt_algorithm: str = "HS256"` to Settings
- `api/app/core/auth.py` — `hash_password()`, `verify_password()`, `create_access_token()`, `decode_access_token()`
- `api/app/schemas/auth.py` — `UserCreate(email, password)`, `UserResponse(id, email)`, `TokenResponse(access_token, token_type)`
- `api/app/services/users/queries.py` — `create_user()`, `get_user_by_email()`
- `api/app/api/routers/auth.py` — `POST /auth/register`, `POST /auth/login`, `GET /auth/me`
- `api/app/api/deps.py` — Add `get_current_user()` and `get_optional_user()` dependencies

### Modified files
- `api/app/main.py` — Include `auth.router`
- `.env` — Add `JWT_SECRET=<random hex>`

## Phase 2: Per-User Links

### Modified files
- `api/app/db/models.py` — `Link.user_id = Column(Integer, ForeignKey("users.id"), nullable=True)`
- `api/app/schemas/link.py` — Add `user_id: int | None` to LinkResponse; add `created_at: str`
- `api/app/api/routers/links.py`:
  - `POST /links` — Accept optional auth; set `user_id` if authenticated
  - `GET /links` — Require auth; return only the user's links
  - `GET /links/{code}` and `GET /links/{code}/analytics` — No auth required (public)
- `api/app/services/links/queries.py` — `create_unique_link()` accepts optional `user_id`

## Phase 3: Backend Tests

### New test files
- `api/tests/test_auth_router.py` — Register, login, duplicate email, bad credentials, /me endpoint
- `api/tests/test_auth_utils.py` — Password hashing, JWT encode/decode

### Modified test files
- `api/tests/conftest.py` — Add `auth_client` fixture (client with JWT header), `sample_user` fixture
- `api/tests/test_links_router.py` — Update to use auth for POST/GET /links
- `api/tests/test_link_queries.py` — Update `create_unique_link` calls with user_id

## Phase 4: Frontend Design Updates

### Modified files
- `web/src/app.html` — Replace Inter with IBM Plex Mono from Google Fonts
- `web/src/routes/layout.css` — Update `--font-sans` to `'IBM Plex Mono'` (monospace)

### New files
- `web/src/lib/components/Mascot.svelte` — Inline SVG mascot: a stylized chain-link character with dot eyes (friendly, geometric, monochrome). Accepts `size` prop.

## Phase 5: Frontend Auth System

### New files
- `web/src/lib/stores/auth.svelte.ts` — Svelte 5 runes-based auth store: `user` state, `isLoggedIn` derived, `login()`, `logout()`, `register()`, `loadUser()` methods. Persists JWT in localStorage.
- `web/src/routes/login/+page.svelte` — Dark login form: email + password, link to register, error handling
- `web/src/routes/register/+page.svelte` — Dark register form: email + password + confirm, link to login
- `web/src/routes/profile/+page.svelte` — User's links dashboard with analytics, account info

### Modified files
- `web/src/lib/api.ts` — Add `register()`, `login()`, `getMe()`, `getMyLinks()`; add `authFetch()` helper that injects Bearer token
- `web/src/lib/types.ts` — Add `User`, `TokenResponse` interfaces
- `web/src/lib/components/Header.svelte` — Show "Login" button or profile avatar based on auth state; add profile link
- `web/src/routes/+layout.svelte` — Call `loadUser()` on mount to restore session

## Phase 6: Guest Banner + Mascot Integration

### New files
- `web/src/lib/components/GuestBanner.svelte` — Animated slide-down banner shown to unauthenticated users on first visit. Contains mascot + message ("Sign up to save your links!"). Dismissible, uses localStorage to remember dismissal. Smooth CSS animation (slideDown + fadeIn).

### Modified files
- `web/src/routes/+page.svelte` — Import GuestBanner, show when not logged in and not dismissed. Add mascot to hero section next to the headline.

---

## Technical Decisions

- **JWT stored in localStorage** — Simple SPA pattern, sent as Bearer header
- **No refresh tokens** — Keeps it simple; token expires in 7 days
- **Link.user_id nullable** — Anonymous users can still shorten, links just won't be saved to a profile
- **GET /links requires auth** — Only returns *your* links. Anonymous shortening returns the link inline but doesn't persist to a user
- **Database reset required** — Using `create_all()` means new tables auto-create, but the existing links table schema change (adding user_id) requires deleting `app.db` and starting fresh
- **IBM Plex Mono** — Monospace font everywhere, matches the dev/hacker aesthetic
- **Mascot** — Simple SVG chain-link character, used in banner and hero section
