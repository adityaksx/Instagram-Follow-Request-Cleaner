# Instagram Follow Request Cleaner

A Python automation tool that cancels sent Instagram follow requests using Playwright.

It reads the list of sent follow-request URLs from an Instagram data-export JSON file, opens each profile in Chromium, detects the **Requested** button, and cancels the request through the Instagram UI.

## Features

- Reads sent follow requests from Instagram's exported JSON data.
- Validates and extracts Instagram profile URLs.
- Uses Playwright to automate Chromium.
- Reuses a saved Instagram login session.
- Opens each profile and clicks:
  - `Requested`
  - `Unfollow`
- Reports successful cancellations, skipped profiles, and failures.
- Uses a visible browser so the automation can be observed while running.

## Project Structure

```text
instagram-follow-request-cleaner/
│
├── cancel_requests.py
├── save_state.py
├── cancel_request.cmd
├── save_state.cmd
├── requirements.txt
├── README.md
│
├── pending_follow_requests.json   # Local input - do not commit
└── ig_state.json                  # Local login state - do not commit
```

## Requirements

- Python 3.9+
- Google Chrome/Chromium-compatible environment
- Playwright
- An Instagram account
- Instagram data export containing sent follow requests

## Installation

Clone the repository:

```bash
git clone https://github.com/adityaksx/Instagram-Follow-Request-Cleaner.git
cd instagram-follow-request-cleaner
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```cmd
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright Chromium:

```bash
playwright install chromium
```

## Setup

### 1. Save Instagram Login State

Run:

```bash
python save_state.py
```

A Chromium window will open.

Log into Instagram manually and return to the terminal.

Press `Enter`.

The script saves the browser authentication state to:

```text
ig_state.json
```

The login state is then reused by the cancellation script instead of requiring login for every run.

### 2. Provide the Follow Request Data

Place the relevant Instagram export JSON file in the project directory and name it:

```text
pending_follow_requests.json
```

The script extracts URLs from:

```text
relationships_follow_requests_sent
```

and validates that they point to Instagram.

### 3. Run the Cleaner

```bash
python cancel_requests.py
```

The browser will open and process the profile URLs one by one.

Example output:

```text
Loaded 25 links
[1] OK
[2] OK
[3] Skip: no Requested/Unfollow
[4] FAIL: timeout

Done. OK=22 FAIL=1
```

## How It Works

1. Load the exported Instagram JSON.
2. Extract sent follow-request URLs.
3. Validate the URLs.
4. Launch Chromium with the saved authentication state.
5. Open each profile.
6. Find the `Requested` button.
7. Click `Requested`.
8. Find and click `Unfollow` in the confirmation dialog.
9. Record the result.
10. Continue with the next profile.

The automation currently uses Playwright locators targeting Instagram's visible `Requested` and `Unfollow` UI elements.

## Important Security Warning

**Never commit `ig_state.json` to GitHub.**

This file contains browser authentication/session information. Treat it like a credential.

Also avoid committing:

```text
pending_follow_requests.json
```

because Instagram exports can contain private account/activity information.

Add both files to `.gitignore`.

If `ig_state.json` has ever been uploaded to a public repository, assume the session may be compromised and log out/revoke the relevant Instagram sessions.

## Limitations

- Instagram's UI can change, which may break the selectors.
- Instagram may rate-limit or restrict automated activity.
- Some profiles may no longer display the expected `Requested` button.
- The script depends on a valid saved login state.
- The automation does not bypass Instagram authentication or security mechanisms.

## Disclaimer

This project is intended for personal automation and educational purposes.

Use automation responsibly and in accordance with Instagram's current terms and policies.

## License

MIT License
