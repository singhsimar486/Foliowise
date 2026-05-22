# Foliowise Documentation Index

## Quick Links

| Document | Description | Pages |
|----------|-------------|-------|
| [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md) | Core technical docs | ~50 |
| [TECHNICAL_DOCUMENTATION_PART2.md](./TECHNICAL_DOCUMENTATION_PART2.md) | API examples & troubleshooting | ~30 |

---

## Documentation Overview

### What's Included

#### Part 1: Core Documentation
1. **Executive Summary** - Product overview, capabilities, architecture highlights
2. **System Architecture** - High-level diagrams, request flow, directory structure
3. **Technology Stack** - Complete list of all technologies with versions
4. **Backend Implementation** - FastAPI app, config, database, ORM models, services
5. **Frontend Implementation** - Angular setup, routes, guards, services, components
6. **Database Schema** - ERD, table definitions, indexes
7. **API Reference** - All 60+ endpoints organized by domain
8. **Authentication & Security** - JWT flow, password hashing, security headers
9. **Third-Party Integrations** - Yahoo Finance, Stripe, Resend, TextBlob
10. **Feature Documentation** - Portfolio tracking, Arena, AI Insights, Subscriptions
11. **Performance & Optimization** - Caching, indexing, frontend optimization
12. **Deployment Guide** - Environment variables, Render config, checklist

#### Part 2: Extended Documentation
13. **Complete API Examples** - curl commands for every endpoint with responses
14. **Troubleshooting Guide** - Common errors and solutions
15. **Testing Documentation** - Unit, integration, E2E tests
16. **Monitoring & Observability** - Logging, metrics, health checks
17. **Security Checklist** - Pre-production security verification
18. **Changelog** - Version history

---

## Quick Stats

| Metric | Count |
|--------|-------|
| **Backend Files** | 27 |
| **Frontend Files** | 35+ |
| **API Endpoints** | 60+ |
| **Database Tables** | 15 |
| **ORM Models** | 9 |
| **Angular Components** | 22 |
| **Dependencies (Backend)** | 22 |
| **Dependencies (Frontend)** | 15 |

---

## Converting to PDF

### Option 1: Pandoc (Recommended)

```bash
# Install
brew install pandoc wkhtmltopdf

# Run converter
chmod +x convert_to_pdf.sh
./convert_to_pdf.sh
```

### Option 2: VS Code Extension

1. Install "Markdown PDF" extension
2. Open `TECHNICAL_DOCUMENTATION.md`
3. Press `Cmd+Shift+P` > "Markdown PDF: Export (pdf)"

### Option 3: Online Converters

- [MarkdownToPDF.com](https://www.markdowntopdf.com/)
- [MD2PDF](https://md2pdf.netlify.app/)
- [CloudConvert](https://cloudconvert.com/md-to-pdf)

---

## For Developers

### Reading Order

1. Start with **Executive Summary** for high-level understanding
2. Review **System Architecture** for component relationships
3. Dive into **Backend/Frontend Implementation** for code details
4. Use **API Reference** as daily reference
5. Consult **Troubleshooting** when issues arise

### Key Files to Know

```
Backend:
├── app/main.py              # Application entry point
├── app/config.py            # Environment configuration
├── app/database.py          # SQLAlchemy setup
├── app/models/user.py       # User model (core)
├── app/routers/auth.py      # Authentication endpoints
├── app/services/market_data.py  # Yahoo Finance integration

Frontend:
├── src/app/app.routes.ts    # Route definitions
├── src/app/services/api.ts  # HTTP client (60+ methods)
├── src/app/services/auth.ts # Auth state management
├── src/app/components/dashboard/  # Main dashboard
├── src/app/components/arena/      # Trading competitions
```

---

## Contact

**Engineering Team:** engineering@foliowise.app
**Documentation Issues:** Open a GitHub issue

---

*Last Updated: April 9, 2026*
