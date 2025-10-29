import os
import re
import json
import subprocess

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BUGS_PATH = os.path.join(REPO_ROOT, 'BUGS.md')
VERSION_PATH = os.path.join(REPO_ROOT, 'VERSION')
STATE_PATH = os.path.join(REPO_ROOT, 'PIPELINE_STATE.json')


def read_state() -> dict:
	try:
		with open(STATE_PATH, 'r', encoding='utf-8') as f:
			return json.load(f)
	except Exception:
		return {"next": "uiTester", "lastCompletedVersion": None}


def write_state(state: dict) -> None:
	with open(STATE_PATH, 'w', encoding='utf-8') as f:
		json.dump(state, f, indent=1)


def read_version() -> int:
	try:
		with open(VERSION_PATH, 'r', encoding='utf-8') as f:
			return int((f.read().strip() or '0').splitlines()[0])
	except Exception:
		return 0


def write_version(n: int) -> None:
	with open(VERSION_PATH, 'w', encoding='utf-8') as f:
		f.write(str(n))


def update_bugs_to_released(version_label: str) -> int:
	if not os.path.exists(BUGS_PATH):
		return 0
	with open(BUGS_PATH, 'r', encoding='utf-8') as f:
		content = f.read()
	content_new = content
	# Set Resolved -> Released
	content_new = re.sub(r"^\s*- Status:\s*Resolved\s*$", "  - Status: Released", content_new, flags=re.MULTILINE)
	# Append FixVersions entry for current release if not present in line
	def add_fix_version(match: re.Match) -> str:
		line = match.group(0)
		if version_label in line:
			return line
		return line.replace('[]', f"[{version_label}]") if '[]' in line else line.replace(']', f", {version_label}]")
	content_new = re.sub(r"^\s*- FixVersions:\s*\[[^\]]*\]\s*$", add_fix_version, content_new, flags=re.MULTILINE)
	if content_new != content:
		with open(BUGS_PATH, 'w', encoding='utf-8') as f:
			f.write(content_new)
		return 1
	return 0


def git(cmd: list) -> None:
	subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def main() -> None:
	state = read_state()
	if state.get('next') != 'cicd':
		print(f"Not my turn (next={state.get('next')}). Skipping.")
		return
	current = read_version()
	next_v = current + 1
	write_version(next_v)
	version_label = f"V.{next_v}"
	changes = update_bugs_to_released(version_label)
	# Commit and push
	git(["git", "add", "-A"])
	message = (
		f"{version_label} 🚀 chore(release): mark fixes Released and bump VERSION\n\n"
		f"- BUGS.md updates: {changes}\n\n"
		"Co-authored-by: Cursor <hi@cursor.com>\n"
	)
	git(["git", "commit", "-m", message])
	git(["git", "push"])
	state['next'] = 'uiTester'
	state['lastCompletedVersion'] = version_label
	write_state(state)
	print(f"CICD released {version_label}, updated BUGS.md (changes={changes}), and advanced state to uiTester.")


if __name__ == '__main__':
	main()
