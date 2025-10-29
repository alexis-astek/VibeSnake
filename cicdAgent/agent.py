from google.adk.agents.llm_agent import Agent

# CICD Agent: stages changes, commits, and pushes to the remote repository
root_agent = Agent(
    model='gemini-2.5-flash',
    name='cicd_agent',
    description='Commits and pushes code changes produced by the Dev Agent.',
    instruction=(
        'You are the CICD Agent. Task: stage the modified files, create a concise commit message, '
        'and push to the current branch.\n\n'
        'Requirements:\n'
        '- Summarize the fixes (referencing BUGS.md items) in the commit subject/body.\n'
        '- Append the following trailer to the commit message exactly as written: \n'
        '  Co-authored-by: Cursor <hi@cursor.com>\n'
        '- Use a single commit unless changes are logically unrelated.\n\n'
        'Operational steps:\n'
        '1) git add -A\n'
        '2) git commit -m "<subject>\n\n<bullet list of fixes>\n\nCo-authored-by: Cursor <hi@cursor.com>"\n'
        '3) git push\n\n'
        'If there are no changes to commit, report that the working tree is clean.'
    ),
)
