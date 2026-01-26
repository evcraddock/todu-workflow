/**
 * Repo Create Tool - Creates a remote repository and clones it locally
 *
 * Supports Forgejo (via fj CLI) and GitHub (via gh CLI)
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { Text } from "@mariozechner/pi-tui";

interface RepoCreateResult {
	success: boolean;
	repoUrl: string;
	localPath: string;
	error?: string;
}

const RepoCreateParams = Type.Object({
	name: Type.String({ description: "Project/repository name" }),
	host: Type.String({ description: '"forgejo" or "github"', default: "forgejo" }),
	description: Type.String({ description: "Repository description" }),
	localPath: Type.String({ description: "Full local path where project should be cloned" }),
});

function errorResult(message: string): { content: { type: "text"; text: string }[]; details: RepoCreateResult } {
	return {
		content: [{ type: "text", text: `Error: ${message}` }],
		details: { success: false, repoUrl: "", localPath: "", error: message },
	};
}

function successResult(
	repoUrl: string,
	localPath: string
): { content: { type: "text"; text: string }[]; details: RepoCreateResult } {
	return {
		content: [{ type: "text", text: `Repository created and cloned successfully.\nURL: ${repoUrl}\nPath: ${localPath}` }],
		details: { success: true, repoUrl, localPath },
	};
}

export default function repoCreate(pi: ExtensionAPI) {
	pi.registerTool({
		name: "repo_create",
		label: "Create Repository",
		description:
			"Create a new remote repository (on Forgejo or GitHub), clone it locally, and register with todu. " +
			"Requires fj CLI for Forgejo or gh CLI for GitHub.",
		parameters: RepoCreateParams,

		async execute(toolCallId, params, onUpdate, ctx, signal) {
			const { name, host, description, localPath } = params;
			const normalizedHost = (host || "forgejo").toLowerCase();

			// Expand ~ in localPath
			const expandedPath = localPath.replace(/^~/, process.env.HOME || "~");

			// Step 1: Check if directory already exists
			onUpdate?.({ content: [{ type: "text", text: "Checking local path..." }] });
			const dirCheck = await pi.exec("test", ["-d", expandedPath], { signal });
			if (dirCheck.code === 0) {
				return errorResult(`Directory already exists: ${expandedPath}`);
			}

			// Step 2: Check CLI installed and authenticated
			onUpdate?.({ content: [{ type: "text", text: `Checking ${normalizedHost} CLI...` }] });

			// Helper to run fj commands through zsh (needed for keyring access)
			const fjExec = async (args: string[], opts: { signal?: AbortSignal; timeout?: number } = {}) => {
				return pi.exec("zsh", ["-ic", `fj ${args.join(" ")}`], opts);
			};

			if (normalizedHost === "forgejo") {
				// Check fj installed
				const fjCheck = await pi.exec("which", ["fj"], { signal });
				if (fjCheck.code !== 0) {
					return errorResult(
						"fj CLI not installed.\n\n" +
							"Install with:\n" +
							"  Arch: paru -S forgejo-cli\n" +
							"  Other: cargo install forgejo-cli\n\n" +
							"Then authenticate:\n" +
							"  fj auth login forgejo.caradoc.com"
					);
				}

				// Check fj authenticated
				const authCheck = await fjExec(["whoami"], { signal, timeout: 10000 });
				if (authCheck.code !== 0 || authCheck.stderr?.includes("not logged in")) {
					return errorResult(
						"fj CLI not authenticated.\n\n" +
							"Run:\n" +
							"  fj auth login forgejo.caradoc.com"
					);
				}
			} else if (normalizedHost === "github") {
				// Check gh installed
				const ghCheck = await pi.exec("which", ["gh"], { signal });
				if (ghCheck.code !== 0) {
					return errorResult(
						"gh CLI not installed.\n\n" +
							"Install from: https://cli.github.com/\n\n" +
							"Then authenticate:\n" +
							"  gh auth login"
					);
				}

				// Check gh authenticated
				const authCheck = await pi.exec("gh", ["auth", "status"], { signal, timeout: 10000 });
				if (authCheck.code !== 0) {
					return errorResult(
						"gh CLI not authenticated.\n\n" +
							"Run:\n" +
							"  gh auth login"
					);
				}
			} else {
				return errorResult(`Unknown host: ${host}. Must be "forgejo" or "github".`);
			}

			// Step 3: Create remote repository
			onUpdate?.({ content: [{ type: "text", text: `Creating repository on ${normalizedHost}...` }] });

			let repoUrl = "";

			if (normalizedHost === "forgejo") {
				const createResult = await fjExec(
					["repo", "create", name, "-d", `"${description}"`],
					{ signal, timeout: 30000 }
				);

				if (createResult.code !== 0) {
					const stderr = createResult.stderr || "";
					if (stderr.includes("already exists") || stderr.includes("409")) {
						return errorResult(
							`Repository "${name}" already exists on Forgejo.\n\n` +
								"Options:\n" +
								"  1. Choose a different name\n" +
								"  2. Delete the existing repo first"
						);
					}
					return errorResult(`Failed to create repository on Forgejo:\n${stderr || createResult.stdout}`);
				}

				// Extract repo URL from output or construct it
				// fj repo create typically outputs the URL
				const output = createResult.stdout || "";
				const urlMatch = output.match(/https?:\/\/[^\s]+/);
				if (urlMatch) {
					repoUrl = urlMatch[0];
				} else {
					// Construct URL - need to get username
					const userResult = await fjExec(["whoami"], { signal });
					// Output is like "currently signed in to erik@forgejo.caradoc.com"
					const match = userResult.stdout?.match(/signed in to (\w+)@([^\s]+)/);
					const username = match?.[1] || "user";
					const host = match?.[2] || "forgejo.caradoc.com";
					repoUrl = `https://${host}/${username}/${name}`;
				}
			} else {
				// GitHub
				const createResult = await pi.exec(
					"gh",
					["repo", "create", name, "--public", "--description", description],
					{ signal, timeout: 30000 }
				);

				if (createResult.code !== 0) {
					const stderr = createResult.stderr || "";
					if (stderr.includes("already exists") || stderr.includes("Name already exists")) {
						return errorResult(
							`Repository "${name}" already exists on GitHub.\n\n` +
								"Options:\n" +
								"  1. Choose a different name\n" +
								"  2. Delete the existing repo first"
						);
					}
					return errorResult(`Failed to create repository on GitHub:\n${stderr || createResult.stdout}`);
				}

				// gh repo create outputs the URL
				repoUrl = createResult.stdout?.trim() || "";
				if (!repoUrl.startsWith("http")) {
					// Try to extract URL or construct it
					const urlMatch = (createResult.stdout || "").match(/https?:\/\/[^\s]+/);
					if (urlMatch) {
						repoUrl = urlMatch[0];
					} else {
						// Get username and construct
						const userResult = await pi.exec("gh", ["api", "user", "-q", ".login"], { signal });
						const username = userResult.stdout?.trim() || "user";
						repoUrl = `https://github.com/${username}/${name}`;
					}
				}
			}

			// Step 4: Clone repository
			onUpdate?.({ content: [{ type: "text", text: `Cloning to ${expandedPath}...` }] });

			// Create parent directory if needed
			const parentDir = expandedPath.substring(0, expandedPath.lastIndexOf("/"));
			await pi.exec("mkdir", ["-p", parentDir], { signal });

			const cloneResult = await pi.exec(
				"git",
				["clone", repoUrl, expandedPath],
				{ signal, timeout: 60000 }
			);

			if (cloneResult.code !== 0) {
				return errorResult(
					`Failed to clone repository:\n${cloneResult.stderr || cloneResult.stdout}\n\n` +
						`Repository was created at: ${repoUrl}\n` +
						"You may need to clone manually."
				);
			}

			// Step 5: Register with todu
			onUpdate?.({ content: [{ type: "text", text: "Registering with todu..." }] });

			const toduResult = await pi.exec(
				"todu",
				["project", "add", "--name", name, "--description", description],
				{ signal, timeout: 10000 }
			);

			if (toduResult.code !== 0) {
				// Non-fatal - repo is created and cloned, just warn
				const warning = `Warning: Failed to register with todu: ${toduResult.stderr || toduResult.stdout}`;
				return {
					content: [
						{
							type: "text",
							text: `Repository created and cloned successfully.\nURL: ${repoUrl}\nPath: ${expandedPath}\n\n${warning}`,
						},
					],
					details: { success: true, repoUrl, localPath: expandedPath },
				};
			}

			return successResult(repoUrl, expandedPath);
		},

		renderCall(args, theme) {
			const host = (args.host as string) || "forgejo";
			const name = args.name as string;
			let text = theme.fg("toolTitle", theme.bold("repo_create "));
			text += theme.fg("accent", name);
			text += theme.fg("muted", ` → ${host}`);
			return new Text(text, 0, 0);
		},

		renderResult(result, options, theme) {
			const details = result.details as RepoCreateResult | undefined;
			if (!details) {
				const text = result.content[0];
				return new Text(text?.type === "text" ? text.text : "", 0, 0);
			}

			if (!details.success) {
				return new Text(theme.fg("error", `✗ ${details.error || "Failed"}`), 0, 0);
			}

			const lines = [
				theme.fg("success", "✓ Repository created"),
				`  ${theme.fg("muted", "URL:")} ${details.repoUrl}`,
				`  ${theme.fg("muted", "Path:")} ${details.localPath}`,
			];
			return new Text(lines.join("\n"), 0, 0);
		},
	});
}
