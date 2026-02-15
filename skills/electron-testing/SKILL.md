---
name: electron-testing
description: Test and interact with Electron desktop applications using Playwright via CDP (Chrome DevTools Protocol). Use when testing Electron apps, debugging UI issues, taking screenshots, verifying interactions, walking through manual test plans, or exercising Electron-based desktop applications. Trigger when user mentions "test electron app", "debug electron", "electron screenshot", "walk through the app", or references testing a desktop app built with Electron.
---

# Electron Testing

Test Electron apps by launching with CDP debugging and connecting Playwright.

## How It Works

1. **Launch** Electron with `--remote-debugging-port`
2. **Connect** Playwright's Chromium via CDP
3. **Interact** — screenshots, clicks, form fills, keyboard shortcuts, console capture

Playwright's `_electron.launch()` often times out on apps with async initialization. The CDP approach is reliable and gives full access to the renderer.

## Prerequisites

Playwright must be available to Node.js. Find it with:

```bash
# Check npx cache (usually available if playwright was ever run via npx)
find ~/.npm/_npx -name "playwright" -type d 2>/dev/null | head -1

# Or check uv cache (from Python playwright)
find ~/.cache/uv -path "*/playwright/driver/package" -type d 2>/dev/null | head -1
```

Set `NODE_PATH` to the parent `node_modules` directory. Example:

```bash
export NODE_PATH=$(find ~/.npm/_npx -path "*/node_modules/playwright" -type d 2>/dev/null | head -1 | xargs dirname)
```

If not found, install once: `npm install -g playwright` or add as project dev dependency.

## Quick Start

### 1. Launch

```bash
# Build first if needed
npm run build  # or: make build-electron

# Launch with CDP
./scripts/launch.sh --app-path ./packages/electron/dist/main/index.js
```

Run `./scripts/launch.sh --help` for all options (custom port, electron binary, build command).

### 2. Interact

```bash
NODE_PATH=<path> node scripts/interact.js <command>
```

**Commands:**

| Command | Description |
|---------|-------------|
| `screenshot [--output path]` | Full-page screenshot (default: `/tmp/electron-screenshot.png`) |
| `screenshot --selector ".my-class"` | Screenshot a specific element |
| `text [--selector sel]` | Get visible text (default: body) |
| `click <selector>` | Click an element (`text=Tasks`, `button.primary`, `#my-id`) |
| `fill <selector> <value>` | Fill an input field |
| `type <text>` | Type with keyboard |
| `press <key>` | Key press (`Control+n`, `Escape`, `Enter`) |
| `discover` | List all buttons, links, and inputs |
| `eval <js>` | Run JS in the renderer |
| `console [--duration ms]` | Capture console output (default: 5s) |
| `wait <selector> [--timeout ms]` | Wait for element |

### 3. Stop

```bash
./scripts/stop.sh
```

## Writing Custom Scripts

For complex test flows, write Node.js scripts directly:

```javascript
const { chromium } = require("playwright");

async function main() {
  const browser = await chromium.connectOverCDP("http://127.0.0.1:9222");
  const page = browser.contexts()[0].pages()[0];

  // Navigate
  await page.click("text=Tasks");
  await page.waitForTimeout(500);

  // Screenshot
  await page.screenshot({ path: "/tmp/tasks-view.png" });

  // Read content
  const text = await page.locator(".task-list").innerText();
  console.log(text);

  // Fill forms
  await page.keyboard.press("Control+n"); // open dialog
  await page.waitForSelector(".dialog");
  await page.fill('input[placeholder="Task title"]', "Test task");
  await page.click("text=Create Task");

  // Console errors
  page.on("console", (msg) => {
    if (msg.type() === "error") console.error("CONSOLE:", msg.text());
  });

  await browser.close();
}

main().catch(console.error);
```

Run with: `NODE_PATH=<path> node my-test.js`

## Selectors

Playwright supports multiple selector strategies:

- **Text**: `text=Save`, `text=+ New Task`
- **CSS**: `.sidebar button`, `#task-list tr`
- **Role**: `role=button[name="Save"]`
- **Placeholder**: `[placeholder="Search tasks..."]`
- **Combine**: `text=Tasks` then wait, then `text=Fix overdue bug`

## Typical Test Workflow

1. Launch app with `scripts/launch.sh`
2. Use `discover` to map out the UI
3. Take a screenshot to see current state
4. Navigate and interact (click, fill, press)
5. Screenshot after each action to verify
6. Check `console` for errors
7. Stop with `scripts/stop.sh`

## Troubleshooting

**Port already in use**: `scripts/launch.sh` auto-kills existing processes on the port.

**Timeout on launch**: Check `/tmp/electron-testing-stderr.log` for crash details.

**"No browser contexts"**: App may not have created a window yet. Increase sleep in launch or check if the app requires additional setup (database, config files).

**vaapi/dbus errors in stderr**: Non-fatal GPU/system integration warnings. Safe to ignore.
