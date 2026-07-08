# 🚀 Installation & Running the Application

## 📦 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Recommended: virtual environment (`venv`)

---

## 🔧 Setup Steps

1. **Clone the repository**

```bash
  git clone https://github.com/Ilangos87/qa_challenge.git
  cd qa_challenge
```

2. **Environment Variables**

```bash
  Edit .env with your credentials:
  APP_USERNAME=your_username
  APP_PASSWORD=your_password
  MFA_CODE=your_code
  SITE_URL=site_url
  API_URL=api_url
```

3. **Create and Activate a Virtual Environment**

```bash
python -m venv .venv
source venv/bin/activate   # Linux / macOS
cd .venv\Scripts\activate      # Windows
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5.  **Install Browser binaries**

```bash
playwright install
```

6. **Running UI Tests**

```bash
pytest tests/ui
```

7. **Running API Tests**

```bash
pytest tests/api
```

# 🔍 Cross‑Layer Data Integrity Check

### What Class of Bug Does It Catch?

The cross‑layer check is designed to catch **data divergence bugs** — situations where the backend API stores or returns one value, but the UI displays another.

- **Example:** The API confirms a card update with `"****1234"`, but the UI summary shows `"****5678"`.
- This indicates either the wrong account was updated or the masking logic differs between layers, which can silently corrupt financial records.

---

### ❌ Why UI‑Only or Status‑Code‑Only Tests Miss It

- **UI‑only tests**: Verify what’s shown on screen, but have no visibility into backend storage.
- If the UI masks `"****1234"` while the database holds `"987654321"`, the test passes even though sensitive data is exposed.
- **Status‑code‑only tests**: Confirm success/failure (`200 OK`), but don’t validate actual values.
- A `200 OK` doesn’t guarantee the masked confirmation matches the UI summary.

---

### ✅ Why This Check Matters

By comparing **API masked confirmation values** against **UI summaries**, we ensure:

- Sensitive data is never leaked in clear text.
- The system’s stored values and the user‑facing values remain consistent.
- Subtle bugs that could compromise trust or compliance are caught early.

## 🔑 Approach

### Page Object Model (POM)

Structured the project with POM to keep selectors and actions reusable and maintainable. This reduces duplication and makes future changes easier.

### Environment Variables

Externalized sensitive values (API URL, credentials, MFA code) into environment variables so nothing is hardcoded in the scripts. This improves security and makes the setup configurable across environments.

### Fixtures & Test Organization

Implemented fixtures at both the suite and root levels to handle authentication and browser state separately. This keeps the test code clean, avoids clutter, and ensures responsibilities are well‑separated.

## 📝 Tradeoffs

### Logging & Exception Handling

Kept it minimal. In production, structured logging and richer exception handling would be required for observability and resilience.

### Negative Scenario Coverage

Parametrization was not used for boundary/negative case testing; instead, a few representative cases were hard‑coded. This makes the suite easier to follow but less scalable if many variations are needed.

### Reporting

Full‑fledged reporting (e.g., HTML dashboards, Allure integration). For production, richer reporting would be essential.

## 🤖 AI Tooling Notes

### Documentation Generation

Leveraged Microsoft Copilot to draft docstrings for classes and methods. This accelerated documentation work and ensured consistency in style.

### README File Creation

Used AI assistance to scaffold the README content, including installation steps, environment variable setup, and approach/tradeoff sections.

### Helper Function Drafting

Applied AI support to generate boilerplate helper functions. These drafts provided a quick starting point, but correctness, edge‑case handling, and integration with the test suite were manually reviewed and adjusted to ensure reliability.

## ✅ Verified by Hand

### Authentication & API Flow

Manually validated the login + MFA process, token handling, and endpoint contracts to ensure the actual API documentation matched with the test case correctly.

### Playwright Fixture & Test Setup

Reviewed and tested the fixture implementation for authentication and browser state reuse. Confirmed that storage state was applied correctly and that tests remained isolated and reliable.
