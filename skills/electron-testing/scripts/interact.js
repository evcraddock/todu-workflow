#!/usr/bin/env node
/**
 * Interact with a running Electron app via CDP + Playwright.
 *
 * Usage: NODE_PATH=<playwright-path> node interact.js <command> [options]
 *
 * Commands:
 *   screenshot [--output path] [--selector sel]   Take a screenshot
 *   text [--selector sel]                         Get visible text content
 *   click <selector>                              Click an element
 *   fill <selector> <value>                       Fill an input field
 *   type <text>                                   Type text with keyboard
 *   press <key>                                   Press a key (e.g. "Control+n", "Escape")
 *   discover                                      List buttons, links, inputs
 *   eval <js-expression>                          Evaluate JS in the renderer
 *   console [--duration ms]                       Capture console output
 *   wait <selector> [--timeout ms]                Wait for element to appear
 *
 * Options:
 *   --port <port>    CDP port (default: 9222)
 *   --help           Show this help
 *
 * Environment:
 *   NODE_PATH must include a directory containing the 'playwright' package.
 *   Or install playwright in the project: npm install -D playwright
 */

const CDP_PORT = getFlag("--port", "9222");
const CDP_URL = `http://127.0.0.1:${CDP_PORT}`;

async function getPage() {
  let chromium;
  try {
    ({ chromium } = require("playwright"));
  } catch {
    console.error(
      "Error: playwright not found. Set NODE_PATH or install it.\n" +
        "  npm install -D playwright\n" +
        '  NODE_PATH=$(npm root -g) node interact.js ...\n' +
        "  NODE_PATH=/path/to/node_modules node interact.js ...",
    );
    process.exit(1);
  }

  const browser = await chromium.connectOverCDP(CDP_URL);
  const contexts = browser.contexts();
  if (!contexts.length) throw new Error("No browser contexts found");
  const pages = contexts[0].pages();
  if (!pages.length) throw new Error("No pages found");
  return { browser, page: pages[0] };
}

function getFlag(name, defaultValue) {
  const idx = process.argv.indexOf(name);
  if (idx === -1) return defaultValue;
  return process.argv[idx + 1];
}

function getPositional(index) {
  // Skip: node, script, command, and any --flags before the positional
  const args = process.argv.slice(3).filter((a) => !a.startsWith("--"));
  return args[index];
}

async function main() {
  const command = process.argv[2];

  if (!command || command === "--help") {
    // Print the header comment as help
    const fs = require("fs");
    const lines = fs.readFileSync(__filename, "utf-8").split("\n");
    for (let i = 1; i < lines.length; i++) {
      if (!lines[i].startsWith(" *")) break;
      console.log(lines[i].replace(/^ \*\s?/, ""));
    }
    process.exit(0);
  }

  const { browser, page } = await getPage();

  try {
    switch (command) {
      case "screenshot": {
        const output = getFlag("--output", "/tmp/electron-screenshot.png");
        const selector = getFlag("--selector", null);
        if (selector) {
          await page.locator(selector).screenshot({ path: output });
        } else {
          await page.screenshot({ path: output, fullPage: true });
        }
        console.log(`Screenshot saved: ${output}`);
        break;
      }

      case "text": {
        const selector = getFlag("--selector", "body");
        const text = await page.locator(selector).first().innerText();
        console.log(text);
        break;
      }

      case "click": {
        const selector = getPositional(0);
        if (!selector) {
          console.error("Usage: click <selector>");
          process.exit(1);
        }
        await page.click(selector);
        await page.waitForTimeout(500);
        console.log(`Clicked: ${selector}`);
        break;
      }

      case "fill": {
        const selector = getPositional(0);
        const value = getPositional(1);
        if (!selector || value === undefined) {
          console.error("Usage: fill <selector> <value>");
          process.exit(1);
        }
        await page.fill(selector, value);
        console.log(`Filled ${selector} with: ${value}`);
        break;
      }

      case "type": {
        const text = getPositional(0);
        if (!text) {
          console.error("Usage: type <text>");
          process.exit(1);
        }
        await page.keyboard.type(text);
        console.log(`Typed: ${text}`);
        break;
      }

      case "press": {
        const key = getPositional(0);
        if (!key) {
          console.error("Usage: press <key>");
          process.exit(1);
        }
        await page.keyboard.press(key);
        await page.waitForTimeout(300);
        console.log(`Pressed: ${key}`);
        break;
      }

      case "discover": {
        const buttons = await page.locator("button").all();
        console.log(`Buttons (${buttons.length}):`);
        for (const btn of buttons) {
          if (await btn.isVisible()) {
            const text = (await btn.innerText()).trim().substring(0, 80);
            console.log(`  - ${text || "[empty]"}`);
          }
        }

        const links = await page.locator("a[href]").all();
        console.log(`\nLinks (${links.length}):`);
        for (const link of links.slice(0, 20)) {
          const text = (await link.innerText()).trim().substring(0, 60);
          const href = await link.getAttribute("href");
          console.log(`  - ${text} -> ${href}`);
        }

        const inputs = await page.locator("input, textarea, select").all();
        console.log(`\nInputs (${inputs.length}):`);
        for (const input of inputs) {
          const tag = await input.evaluate((el) => el.tagName.toLowerCase());
          const type = (await input.getAttribute("type")) || tag;
          const name =
            (await input.getAttribute("name")) ||
            (await input.getAttribute("id")) ||
            (await input.getAttribute("placeholder")) ||
            "[unnamed]";
          console.log(`  - ${name} (${type})`);
        }
        break;
      }

      case "eval": {
        const expr = process.argv.slice(3).join(" ");
        if (!expr) {
          console.error("Usage: eval <js-expression>");
          process.exit(1);
        }
        const result = await page.evaluate(expr);
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      case "console": {
        const duration = parseInt(getFlag("--duration", "5000"), 10);
        const logs = [];
        page.on("console", (msg) => {
          const entry = `[${msg.type()}] ${msg.text()}`;
          logs.push(entry);
          console.log(entry);
        });
        console.log(`Capturing console output for ${duration}ms...`);
        await page.waitForTimeout(duration);
        console.log(`\nCaptured ${logs.length} messages`);
        break;
      }

      case "wait": {
        const selector = getPositional(0);
        const timeout = parseInt(getFlag("--timeout", "5000"), 10);
        if (!selector) {
          console.error("Usage: wait <selector> [--timeout ms]");
          process.exit(1);
        }
        await page.waitForSelector(selector, { timeout });
        console.log(`Element found: ${selector}`);
        break;
      }

      default:
        console.error(`Unknown command: ${command}`);
        process.exit(1);
    }
  } finally {
    await browser.close();
  }
}

main().catch((e) => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
