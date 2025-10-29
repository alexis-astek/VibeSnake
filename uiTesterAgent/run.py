import os
import json
from datetime import date

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BUGS_PATH = os.path.join(REPO_ROOT, 'BUGS.md')
VERSION_PATH = os.path.join(REPO_ROOT, 'VERSION')
STATE_PATH = os.path.join(REPO_ROOT, 'PIPELINE_STATE.json')


def read_version_label() -> str:
	try:
		with open(VERSION_PATH, 'r', encoding='utf-8') as f:
			n = int(f.read().strip() or '0')
		return f"V.{n}"
	except Exception:
		return "V.0"


def get_pages_url() -> str:
	return os.environ.get('PAGES_URL', '').strip()


def read_state() -> dict:
	try:
		with open(STATE_PATH, 'r', encoding='utf-8') as f:
			return json.load(f)
	except Exception:
		return {"next": "uiTester", "lastCompletedVersion": None}


def write_state(state: dict) -> None:
	with open(STATE_PATH, 'w', encoding='utf-8') as f:
		json.dump(state, f, indent=1)


def append_bugs_template(version_label: str, pages_url: str) -> None:
	if not os.path.exists(BUGS_PATH):
		with open(BUGS_PATH, 'w', encoding='utf-8') as f:
			f.write('# Bug Backlog\n\n')
	date_str = date.today().isoformat()
	entry = []
	entry.append(f"## [{date_str}] UI Test Run")
	entry.append("- [ ] P1 Example: Verify page loads")
	entry.append("  - Status: Open")
	entry.append("  - Area: landing page")
	entry.append(f"  - Versions: [{version_label}]")
	entry.append("  - FixVersions: []")
	entry.append("  - Steps: Navigate to the app")
	entry.append("  - Expected: App loads without errors")
	entry.append("  - Actual: Please replace with actual observation")
	entry.append(f"  - Evidence: {pages_url or '(local review)'}")
	entry.append("")
	with open(BUGS_PATH, 'a', encoding='utf-8') as f:
		f.write('\n'.join(entry) + '\n')


def main() -> None:
	state = read_state()
	if state.get('next') != 'uiTester':
		print(f"Not my turn (next={state.get('next')}). Skipping.")
		return
	version_label = read_version_label()
	pages_url = get_pages_url()
	append_bugs_template(version_label, pages_url)
	state['next'] = 'dev'
	write_state(state)
	print(f"UI Tester wrote sample bugs for {version_label} and advanced state to dev.")


if __name__ == '__main__':
	main()
