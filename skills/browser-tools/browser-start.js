#!/usr/bin/env node

import { spawn, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, statSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

const args = process.argv.slice(2);
const useProfile = args.includes("--profile");

if (args.some((arg) => arg !== "--profile")) {
	console.log("Usage: browser-start.js [--profile]");
	console.log("\nOptions:");
	console.log("  --profile  Use a persistent Chromium profile directory");
	console.log("\nEnvironment:");
	console.log("  BROWSER_TOOLS_CHROMIUM_PATH  Absolute path to the Chromium executable");
	console.log("  CHROMIUM_PATH                Fallback Chromium executable override");
	console.log("  PUPPETEER_EXECUTABLE_PATH    Fallback executable override");
	console.log("  BROWSER_TOOLS_USER_DATA_DIR  Override the Chromium user data directory");
	console.log("  BROWSER_TOOLS_SKIP_CHROMIUM_INSTALL=1  Disable automatic Chromium install");
	process.exit(1);
}

const SCRIPT_DIR = fileURLToPath(new URL(".", import.meta.url));
const CACHE_DIR = `${process.env.HOME}/.cache/browser-tools`;
const PROFILE_DIR =
	process.env.BROWSER_TOOLS_USER_DATA_DIR ||
	(useProfile ? `${process.env.HOME}/.config/browser-tools/chromium-profile` : `${CACHE_DIR}/chromium-profile`);

// Check if already running on :9222
try {
	const browser = await puppeteer.connect({
		browserURL: "http://localhost:9222",
		defaultViewport: null,
	});
	await browser.disconnect();
	console.log("✓ Chromium-compatible browser already running on :9222");
	process.exit(0);
} catch {}

function isExecutablePath(path) {
	if (!path) return false;
	try {
		return existsSync(path) && statSync(path).isFile();
	} catch {
		return false;
	}
}

function isUsableChromiumExecutable(path) {
	if (!isExecutablePath(path)) return false;

	const result = spawnSync(path, ["--version"], {
		encoding: "utf8",
		timeout: 5000,
	});

	if (result.status !== 0) return false;
	return /Chrom(e|ium)|HeadlessChrome/i.test(`${result.stdout || ""}\n${result.stderr || ""}`);
}

function findCommand(command) {
	const result =
		process.platform === "win32"
			? spawnSync("where", [command], { encoding: "utf8" })
			: spawnSync("sh", ["-lc", `command -v ${command}`], { encoding: "utf8" });

	if (result.status !== 0) return null;
	return result.stdout.trim().split(/\r?\n/).find(Boolean) || null;
}

function puppeteerCacheChromiumPaths() {
	const cacheDir = `${process.env.HOME}/.cache/puppeteer/chromium`;
	if (!existsSync(cacheDir)) return [];

	let builds;
	try {
		builds = readdirSync(cacheDir, { withFileTypes: true })
			.filter((entry) => entry.isDirectory())
			.map((entry) => entry.name)
			.sort()
			.reverse();
	} catch {
		return [];
	}

	return builds.flatMap((build) => {
		const buildDir = join(cacheDir, build);
		if (process.platform === "darwin") {
			return [join(buildDir, "chrome-mac", "Chromium.app", "Contents", "MacOS", "Chromium")];
		}
		if (process.platform === "linux") {
			return [join(buildDir, "chrome-linux", "chrome"), join(buildDir, "chrome-linux64", "chrome")];
		}
		if (process.platform === "win32") {
			return [join(buildDir, "chrome-win", "chrome.exe"), join(buildDir, "chrome-win64", "chrome.exe")];
		}
		return [];
	});
}

function commonChromiumPaths() {
	const paths = [...puppeteerCacheChromiumPaths()];

	if (process.platform === "darwin") {
		paths.push(
			"/Applications/Chromium.app/Contents/MacOS/Chromium",
			`${process.env.HOME}/Applications/Chromium.app/Contents/MacOS/Chromium`,
		);
	} else if (process.platform === "linux") {
		paths.push(
			"/usr/bin/chromium",
			"/usr/bin/chromium-browser",
			"/usr/local/bin/chromium",
			"/snap/bin/chromium",
		);
	} else if (process.platform === "win32") {
		const localAppData = process.env.LOCALAPPDATA;
		const programFiles = process.env.ProgramFiles;
		const programFilesX86 = process.env["ProgramFiles(x86)"];
		paths.push(
			localAppData && join(localAppData, "Chromium", "Application", "chrome.exe"),
			programFiles && join(programFiles, "Chromium", "Application", "chrome.exe"),
			programFilesX86 && join(programFilesX86, "Chromium", "Application", "chrome.exe"),
		);
	}

	return paths.filter(Boolean);
}

function resolveChromiumExecutable() {
	const configuredPaths = [
		process.env.BROWSER_TOOLS_CHROMIUM_PATH,
		process.env.CHROMIUM_PATH,
		process.env.PUPPETEER_EXECUTABLE_PATH,
	];

	for (const path of configuredPaths) {
		if (isUsableChromiumExecutable(path)) return path;
	}

	for (const path of commonChromiumPaths()) {
		if (isUsableChromiumExecutable(path)) return path;
	}

	for (const command of ["chromium", "chromium-browser"]) {
		const path = findCommand(command);
		if (isUsableChromiumExecutable(path)) return path;
	}

	return null;
}

function puppeteerCliPath() {
	const executable = process.platform === "win32" ? "puppeteer.cmd" : "puppeteer";
	const localPath = join(SCRIPT_DIR, "node_modules", ".bin", executable);
	return isExecutablePath(localPath) ? localPath : null;
}

function installChromium() {
	if (process.env.BROWSER_TOOLS_SKIP_CHROMIUM_INSTALL === "1") {
		return null;
	}

	console.log("Chromium not found; installing Puppeteer-managed Chromium...");

	const localCli = puppeteerCliPath();
	const command = localCli || "npm";
	const installArgs = localCli
		? ["browsers", "install", "chromium@latest"]
		: ["exec", "--", "puppeteer", "browsers", "install", "chromium@latest"];

	const result = spawnSync(command, installArgs, {
		cwd: SCRIPT_DIR,
		encoding: "utf8",
		stdio: ["ignore", "pipe", "pipe"],
	});

	const output = `${result.stdout || ""}\n${result.stderr || ""}`.trim();
	if (result.status !== 0) {
		if (output) console.error(output);
		return null;
	}

	if (output) console.log(output);

	const executablePath = output
		.split(/\r?\n/)
		.map((line) => line.match(/^chromium@\S+\s+(.+)$/)?.[1])
		.find(Boolean);

	return isUsableChromiumExecutable(executablePath) ? executablePath : resolveChromiumExecutable();
}

const chromiumExecutable = resolveChromiumExecutable() || installChromium();

if (!chromiumExecutable) {
	console.error("✗ Chromium executable not found");
	console.error("  Install Chromium or run:");
	console.error("    cd \"%s\" && npm exec -- puppeteer browsers install chromium@latest", SCRIPT_DIR);
	console.error("  Or set BROWSER_TOOLS_CHROMIUM_PATH=/absolute/path/to/chromium");
	process.exit(1);
}

// Setup profile directory
mkdirSync(PROFILE_DIR, { recursive: true });

// Remove singleton files to allow a new isolated Chromium instance.
for (const filename of ["SingletonLock", "SingletonSocket", "SingletonCookie"]) {
	try {
		unlinkSync(join(PROFILE_DIR, filename));
	} catch {}
}

// Start Chromium with flags to force a new instance and expose CDP on :9222.
spawn(
	chromiumExecutable,
	[
		"--remote-debugging-port=9222",
		`--user-data-dir=${PROFILE_DIR}`,
		"--no-first-run",
		"--no-default-browser-check",
	],
	{ detached: true, stdio: "ignore" },
).unref();

// Wait for Chromium to be ready
let connected = false;
for (let i = 0; i < 30; i++) {
	try {
		const browser = await puppeteer.connect({
			browserURL: "http://localhost:9222",
			defaultViewport: null,
		});
		await browser.disconnect();
		connected = true;
		break;
	} catch {
		await new Promise((r) => setTimeout(r, 500));
	}
}

if (!connected) {
	console.error("✗ Failed to connect to Chromium on :9222");
	process.exit(1);
}

console.log(`✓ Chromium started on :9222 using ${chromiumExecutable}`);
console.log(`  Profile: ${PROFILE_DIR}`);
