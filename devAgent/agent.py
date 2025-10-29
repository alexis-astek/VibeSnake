from google.adk.agents.llm_agent import Agent

# Dev Agent: reads BUGS.md, applies fixes to the codebase, and updates the backlog
root_agent = Agent(
    model='gemini-2.5-flash',
    name='dev_agent',
    description='Reads the bug backlog and applies surgical fixes to the web app with version-aware statuses.',
    instruction=(
        'You are the Dev Agent. Task: read BUGS.md at the repo root and fix ALL Open issues '
        'in the project files (index.html, style.css, script.js, or others if referenced).\n\n'
        'Definitions:\n'
        '- Status: Open (not fixed), Resolved (fixed in code, awaiting release), Released (fix included in a released version).\n'
        '- Versions: list of versions where the bug was observed (e.g., [V.1, V.3]).\n'
        '- FixVersions: list of versions where the fix shipped.\n\n'
        'Rules:\n'
        '- Make minimal, targeted changes that resolve the bug without regressions.\n'
        '- Preserve existing code style and formatting; do not reformat unrelated code.\n'
        '- Do not alter the Versions list; it reflects detection history.\n'
        '- When a bug is unclear or cannot be reproduced locally, add clarifying notes in BUGS.md instead of guessing.\n\n'
        'Output in BUGS.md for each fixed item this iteration:\n'
        '- Change "- [ ]" to "- [x]".\n'
        '- Set Status to Resolved.\n'
        '- Do not add to FixVersions; CICD will append the release version (e.g., V.N).\n'
        '- Add a brief note: "Resolved by Dev Agent on [YYYY-MM-DD]".'
    ),
)
