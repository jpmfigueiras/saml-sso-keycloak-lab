# saml-sso-keycloak-lab

Single sign-on (SSO) between two independent web applications using **SAML 2.0**, with **Keycloak** as the identity provider, **FastAPI** service providers and **React** frontends. Built during the MSc in Cybersecurity at the Polytechnic Institute of Viana do Castelo.

The goal is to show the full identity lifecycle across applications: a user signs in once at the identity provider, is recognised by both applications without logging in again, receives a role from the IdP, and is signed out of every application with a single logout.

## Architecture

```
                         +-----------------------------+
                         |  Keycloak (IdP)             |
                         |  realm: gid-dev   :8080     |
                         |  users, roles, SAML clients |
                         +-------------+---------------+
                      SAML AuthnRequest |  signed SAML Response
               +-----------------------+-----------------------+
               |                                               |
   +-----------v-----------+                       +-----------v-----------+
   | backend  (app1) :8000 |                       | backend2 (app2) :8001 |
   | FastAPI + python3-saml|                       | FastAPI + python3-saml|
   +-----------+-----------+                       +-----------+-----------+
               |                                               |
   +-----------v-----------+                       +-----------v-----------+
   | frontend  (React)     |                       | frontend2 (React)     |
   | :3000                 |                       | :3001                 |
   +-----------------------+                       +-----------------------+
               \                                               /
                +------------------ MySQL :3307 ---------------+
                     users, keyed by (username, app_name)
```

Each application is registered in Keycloak as its own SAML client (`gid-fastapi-saml` and `gid-fastapi-saml-app2`), so they share the identity provider but keep separate sessions and user records.

## Authentication flow

1. The user opens either frontend and clicks **Login**. The backend builds a SAML `AuthnRequest` and redirects to Keycloak.
2. Keycloak authenticates the user (or reuses the existing IdP session, which is what makes it single sign-on) and posts a signed SAML response to the backend's Assertion Consumer Service, `/auth/saml/acs`.
3. The backend validates the response with `python3-saml` — assertions must be signed (`wantAssertionsSigned: true`) — and reads the user's attributes: email, first and last name, and role.
4. The user is created or updated in MySQL for that specific application (`username` + `app_name` is the primary key), and the backend sets an HTTP-only session cookie before redirecting to the frontend.
5. `GET /auth/me` returns the current user and role, which the dashboard displays.
6. **Logout** starts SAML Single Logout (SLO) at Keycloak, which ends the IdP session and therefore the session in both applications; `/auth/saml/sls` handles the return.

## Tech stack

| Layer        | Technology                                              |
|--------------|---------------------------------------------------------|
| Identity     | Keycloak 24, SAML 2.0, realm imported from `keycloak/`  |
| Backend      | Python, FastAPI, python3-saml, SQLAlchemy, PyMySQL      |
| Frontend     | React 18, React Router, Axios, Context API              |
| Database     | MySQL 8                                                 |
| Infrastructure | Docker, Docker Compose                                |

## Running locally

Requires Docker, Docker Compose and Python 3.

```bash
docker compose up -d --build
python scripts/sync_idp_cert.py
```

No private keys are stored in the repository. Keycloak generates a fresh signing key for the realm on first start, and `scripts/sync_idp_cert.py` copies the matching public certificate from the realm's SAML descriptor into both service providers so they can verify signed assertions. Run it once Keycloak is up (it takes a few seconds to start).

| Service      | URL                          |
|--------------|------------------------------|
| App 1        | http://localhost:3000        |
| App 2        | http://localhost:3001        |
| API 1 docs   | http://localhost:8000/docs   |
| API 2 docs   | http://localhost:8001/docs   |
| Keycloak     | http://localhost:8080        |

Keycloak starts in development mode and imports the `gid-dev` realm automatically, including a test user (`user_test` / `user_test`). Sign in to one application, then open the other: it logs you in without asking for credentials again. Logging out from either application ends both sessions.

## Project structure

```
saml-sso-keycloak-lab/
├── backend/            # FastAPI service provider for app1
├── backend2/           # FastAPI service provider for app2
│   ├── routes/         # SAML login, ACS, /me, logout and SLS endpoints
│   ├── controllers/    # user create/update logic
│   └── saml/           # SP settings and IdP metadata
├── frontend/           # React app for app1
├── frontend2/          # React app for app2
├── data_model/         # SQLAlchemy model and SQL schema
├── keycloak/           # realm export imported on startup (no keys or secrets)
├── scripts/            # sync_idp_cert.py: trusts the realm's signing certificate
└── docker-compose.yml
```

## Known limitations

This is a lab environment focused on the SAML flow, not a production setup:

- The session cookie holds the username directly and is not signed, so it should be replaced by a signed session token or JWT before any real use.
- Authentication requests and SAML messages are not signed by the service providers (only the IdP assertions are), and everything runs over plain HTTP on localhost.
- Keycloak runs in `start-dev` mode with default admin credentials, the realm ships with a test user, and the database password has a development default in `docker-compose.yml`.
- The two backends and frontends are near-identical copies; in a real system they would share a common package.
