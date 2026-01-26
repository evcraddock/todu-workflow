.PHONY: dev dev-stop dev-logs check pre-pr

dev:
	overmind start -f Procfile.dev

dev-stop:
	overmind quit || true

dev-logs:
	overmind connect

check:
	{check_command}

pre-pr:
	./scripts/pre-pr.sh
