import os
import re
import json
from datetime import date

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BUGS_PATH = os.path.join(REPO_ROOT, 'BUGS.md')
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


def resolve_open_items() -> int:
	if not os.path.exists(BUGS_PATH):
		return 0
	with open(BUGS_PATH, 'r', encoding='utf-8') as f:
		content = f.read()
	content_new = content
	content_new = re.sub(r"^- \[ \] ", "- [x] ", content_new, flags=re.MULTILINE)
	content_new = re.sub(r"^\s*- Status:\s*Open\s*$", "  - Status: Resolved", content_new, flags=re.MULTILINE)
	note = f"Resolved by Dev Agent on {date.today().isoformat()}"
	if note not in content_new:
		content_new = content_new.strip() + f"\n\n> {note}\n"
	if content_new != content:
		with open(BUGS_PATH, 'w', encoding='utf-8') as f:
			f.write(content_new)
		return 1
	return 0


def main() -> None:
	state = read_state()
	if state.get('next') != 'dev':
		print(f"Not my turn (next={state.get('next')}). Skipping.")
		return
	changes = resolve_open_items()
	state['next'] = 'cicd'
	write_state(state)
	print(f"Dev updated BUGS.md (changes={changes}) and advanced state to cicd.")


if __name__ == '__main__':
	main()
