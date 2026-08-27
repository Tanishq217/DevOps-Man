# DevOps — Chapter 5: Git and GitHub

> **Goal:** Learn version control from zero: track changes with Git, collaborate through GitHub, and use the everyday Git workflow safely.

---

## 1. Why Git and GitHub Matter

Software changes continually—features, fixes, documentation, and infrastructure. Before version control, teams passed ZIP files through email or copied files to shared servers. This creates versions like `final.zip` and `final-final.zip`, loses context about who changed what, and makes rollback risky.

Git records project history; GitHub hosts Git repositories online and adds collaboration tools. Together they enable:

- **Version history:** see what changed, who changed it, when, and why.
- **Rollback:** return to a known-good snapshot.
- **Safe teamwork:** several people contribute without silently overwriting work.
- **Online backup and sharing:** keep a remote project copy.
- **Review and automation:** test/review a change before it reaches the main branch.

DevOps uses Git for application code, docs, CI/CD definitions, Dockerfiles, Kubernetes manifests, Terraform, Ansible, and config.

## 2. Git vs GitHub

| Topic | Git | GitHub |
| --- | --- | --- |
| What it is | Distributed version-control system | Cloud platform that hosts Git repos |
| Runs where | Local computer | GitHub servers and web tools |
| Job | Tracks file changes and commits | Sharing, review, planning, automation |
| Internet required? | No for local commits | Yes to sync/collaborate |
| Examples | `git add`, `git commit` | PRs, Issues, Actions, Projects |

Git is the tool; GitHub is a service built around it. GitLab and Bitbucket are alternatives.

### Distributed version control

A clone holds the full project history, not just current files. You can create local commits offline and push them later.

## 3. Terms to Know

- **Repository (repo):** a project folder plus its Git history.
- **Commit:** a saved snapshot of staged changes with a message, author, timestamp, and unique hash.
- **Branch:** an independent line of development.
- **Remote:** a hosted copy; it is commonly named `origin`.
- **Clone:** a full local copy of a remote repo.
- **Push / pull:** upload local commits / download and integrate remote commits.
- **Fetch:** download remote information without changing current files.
- **HEAD:** reference to the currently checked-out commit or branch.

## 4. Create a GitHub Repository

1. Sign in to GitHub and select **New repository**.
2. Name it clearly, for example `devops-learning-notes`.
3. Add an optional description.
4. Choose **Public** (visible to everyone) or **Private** (only invited users).
5. Optionally add a README, a `.gitignore`, and a license.
6. Select **Create repository**.

### README, ignore rules, and licenses

- **README.md** introduces the project: purpose, setup, use, and important details.
- **.gitignore** prevents untracked secrets, logs, generated output, and local-only files from being added.
- **License** states how others may use an open-source project. Choose it deliberately.

### Create locally, then publish

```bash
mkdir devops-learning-notes
cd devops-learning-notes
git init
git branch -M main
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/devops-learning-notes.git
git push -u origin main
```

Replace `USERNAME` and repo name. `-u` sets an upstream so future `git push` and `git pull` commands can be shorter.

### Clone an existing repository

```bash
git clone https://github.com/USERNAME/devops-learning-notes.git
cd devops-learning-notes
```

SSH URLs such as `git@github.com:USERNAME/repo.git` require an SSH key registered with GitHub. HTTPS normally uses browser authentication or a personal access token, not an account password.

## 5. Configure Git Identity

Every commit stores its author. Configure it before committing:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

`--global` applies to all repos for the current user. To set an identity only in the current repo, omit `--global`.

```bash
git config user.name "Work Name"
git config user.email "work@example.com"
git config --global --list
git config --list
git config --global init.defaultBranch main
git config --global pull.rebase false
```

## 6. The Four Git Locations

```text
Working directory --git add--> Staging area --git commit--> Local repository --git push--> GitHub remote
      files                         index                       history
                                                                  ^
                                              git pull / fetch ---|
```

1. **Working directory:** files being edited.
2. **Staging area (index):** selected changes for the next commit.
3. **Local repository:** committed history on this computer.
4. **Remote repository:** shared GitHub copy.

Staging is valuable: it lets one commit contain only related files, or selected portions of a file.

## 7. Essential Commands

### Inspect

```bash
git status
git diff
git diff --staged
```

- `git status` shows branch, untracked, modified, staged, and unpushed changes.
- `git diff` shows unstaged changes.
- `git diff --staged` shows the proposed next commit.

### Start, stage, and commit

```bash
git init
git add README.md
git add notes/
git add .
git add -p
git commit -m "Add Chapter 5 Git notes"
```

`git init` creates a hidden `.git` directory holding Git metadata—do not edit it manually. `git add` stages changes; `git add .` stages all changes below the current folder, so inspect `git status` first. `git add -p` interactively stages selected sections.

Use clear, imperative commit messages such as `Add README`, `Fix database timeout`, or `Update deployment guide`. Keep each commit focused on one logical change.

### History, remotes, and sync

```bash
git log
git log --oneline --graph --decorate --all
git show COMMIT_HASH
git remote -v
git push origin main
git push -u origin feature/add-notes
git fetch origin
git pull origin main
```

`git fetch` downloads commits/branch information without modifying working files. `git pull` normally fetches then merges into the current branch. Save or commit work and check status before pulling.

## 8. Branching and Merging

A branch isolates work, keeping `main` stable and deployable.

```bash
git branch
git branch feature/add-git-notes
git switch feature/add-git-notes
git switch -c feature/add-git-notes
```

`git branch` lists branches; `*` marks the active branch. `git switch -c NAME` creates and switches at once. Older tutorials may use:

```bash
git checkout -b feature/add-git-notes
git checkout main
```

Useful names: `feature/add-login`, `fix/database-timeout`, `docs/chapter-5-git-notes`, and `chore/update-dependencies`.

Uncommitted changes may prevent switching if they would be overwritten. Commit or safely store that work first.

### Merge a completed branch

```bash
git switch main
git pull origin main
git merge feature/add-git-notes
git push origin main
```

A **fast-forward merge** simply advances a branch pointer when no divergent commits exist. A **merge commit** connects two histories when both branches contain distinct commits.

Delete a branch only after it is confirmed merged and unneeded:

```bash
git branch -d feature/add-git-notes
git push origin --delete feature/add-git-notes
```

Teams generally merge through a GitHub pull request rather than directly pushing to `main`.

## 9. Merge Conflicts

A conflict occurs when Git cannot safely combine edits, for example when two branches modify the same lines.

```text
<<<<<<< HEAD
Current-branch version
=======
Incoming-branch version
>>>>>>> feature/add-git-notes
```

Resolution process:

1. Run `git status` to find conflicted files.
2. Edit each file and choose or combine the required content.
3. Remove every `<<<<<<<`, `=======`, and `>>>>>>>` marker.
4. Review and test.
5. Stage resolved files and complete the merge.

```bash
git add conflicted-file.md
git commit
git merge --abort
```

`git merge --abort` cancels an in-progress merge. Never blindly accept “ours” or “theirs”; understand the intended final result.

## 10. Rebase

Rebase reapplies a branch's commits on top of a different base, commonly the latest `main`, producing a linear history.

```bash
git switch feature/add-git-notes
git fetch origin
git rebase origin/main
```

On conflict:

```bash
git add conflicted-file.md
git rebase --continue
git rebase --abort
git rebase --skip
```

`--abort` restores the pre-rebase state. Use `--skip` only when omitting that commit is correct.

**Safety rule:** rebase rewrites history and changes commit hashes. Do not rebase shared commits without team agreement. If a previously pushed personal feature branch needs updating:

```bash
git push --force-with-lease origin feature/add-git-notes
```

Prefer `--force-with-lease` to `--force`; it refuses to overwrite unexpected remote work. Never force-push shared protected branches like `main`.

| Merge | Rebase |
| --- | --- |
| Preserves existing history | Rewrites rebased branch history |
| May create a merge commit | Usually creates linear history |
| Safe shared-branch default | Good for local/private cleanup |

## 11. Cherry-pick

Cherry-pick copies one chosen commit from another branch to the current branch. Use it when only a single fix is needed.

```bash
git switch main
git cherry-pick a1b2c3d
```

Find hashes with `git log`. Cherry-pick makes a new commit with a new hash. Resolve any conflict, then:

```bash
git add conflicted-file.md
git cherry-pick --continue
git cherry-pick --abort
```

Avoid repeated cherry-picks between long-lived branches because history becomes difficult to follow.

## 12. Ignoring Files and Protecting Secrets

A `.gitignore` file lists untracked files Git should skip:

```gitignore
# Secrets and local configuration
.env
*.key

# Logs
*.log
logs/

# Dependencies and build output
node_modules/
dist/
__pycache__/

# Editor and OS files
.vscode/
.DS_Store
```

- Never commit passwords, API keys, tokens, private keys, or real `.env` files.
- Ignore rules do not affect files already committed.
- To stop tracking a file while retaining it locally:

```bash
git rm --cached .env
git commit -m "Stop tracking local environment file"
```

- Commit a safe `.env.example` with placeholders.
- If a secret is committed, rotate/revoke it immediately; later deletion does not remove it from history.

## 13. GitHub Features

### Pull requests (PRs)

A PR proposes merging one branch into another, usually a feature branch into `main`. It provides a place for review, conversation, approvals, and automated checks.

1. Create a focused branch and commits.
2. Push it to GitHub.
3. Open a PR explaining problem, solution, testing, and risk.
4. Address review comments and checks.
5. Merge after required approval/checks.
6. Delete the completed branch when appropriate.

### Issues

Issues track bugs, feature requests, questions, and tasks. Include a clear title, context, expected/actual behavior for bugs, reproduction steps, labels, priority, and owner. Use `#123` to link an issue; `Fixes #123` in a merged PR can close it.

### GitHub Actions

Actions automates work on pushes, PRs, schedules, manual events, and more. Workflow YAML belongs in `.github/workflows/`.

```yaml
name: Validate notes
on:
  pull_request:
  push:
    branches: [main]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: find . -name '*.md' -print
```

Actions can test, lint, build, scan, and deploy. Treat workflow files as code and place credentials in GitHub Secrets, never files or logs.

### GitHub Projects

Projects organizes Issues and PRs in tables or boards, for example:

```text
Todo → In progress → In review → Done
```

This makes status, priority, ownership, sprints, and roadmaps visible.

## 14. Hands-On Workflow

```bash
# Get shared work
git switch main
git pull origin main

# Make a dedicated branch
git switch -c docs/chapter-5-git-notes

# Edit, inspect, stage, and commit
git status
git diff
git add 05-git-and-github.md
git diff --staged
git commit -m "Add Chapter 5 Git and GitHub notes"

# Publish the branch
git push -u origin docs/chapter-5-git-notes
```

Then create a GitHub PR to `main`, review it, complete checks, and merge under the repository's rules. Afterwards:

```bash
git switch main
git pull origin main
git branch -d docs/chapter-5-git-notes
```

## 15. Best Practices

- Run `git status` often.
- Keep commits small, focused, and clearly named.
- Review `git diff` before staging and `git diff --staged` before committing.
- Fetch/pull before beginning and before merging.
- Use branches and PRs instead of unreviewed direct changes to `main`.
- Keep `main` stable and protect it with reviews/checks where possible.
- Never commit secrets; use ignore rules, templates, and secret scanning.
- Resolve conflicts carefully and test afterward.
- Avoid rewriting shared history with rebase, amend, or force-push.
- Keep the README useful for future contributors.

## 16. Common Problems

### Nothing to commit

Run `git status`. The file may be unchanged, already committed, or ignored.

### Push rejected

The remote has commits missing locally. Save current work, then integrate it:

```bash
git pull origin main
```

Resolve conflicts, commit the resolution, and push again. Follow the team merge/rebase policy—do not force-push by default.

### Accidentally staged a file

```bash
git restore --staged FILE_NAME
```

This un-stages the file but retains working-directory edits.

### Discard an uncommitted file change

```bash
git restore FILE_NAME
```

This is destructive: it replaces the file with the last committed version. Check `git diff` first.

## 17. Command Cheat Sheet

| Task | Command |
| --- | --- |
| Start tracking a folder | `git init` |
| Copy a repo | `git clone URL` |
| Show state | `git status` |
| Show changes | `git diff` / `git diff --staged` |
| Stage work | `git add FILE_NAME` |
| Commit work | `git commit -m "Message"` |
| View history | `git log --oneline --graph --all` |
| Switch/create branch | `git switch NAME` / `git switch -c NAME` |
| Combine branches | `git merge BRANCH` |
| Download remote info | `git fetch origin` |
| Download and integrate | `git pull origin BRANCH` |
| Upload commits | `git push origin BRANCH` |
| Rebase current branch | `git rebase BRANCH` |
| Apply one commit | `git cherry-pick COMMIT_HASH` |
| Show remotes | `git remote -v` |

## 18. DevOps Career Relevance

Git is foundational for DevOps. CI/CD pipelines often begin when a push or PR occurs, while infrastructure and deployment definitions become safer when versioned, reviewed, and auditable.

Be ready to explain Git vs GitHub; the working directory, staging area, local repo, and remote; `fetch` vs `pull`; branches, PRs, conflicts, merge, rebase, and cherry-pick; why secrets must not be committed; and how GitHub Actions connects Git events to CI/CD.

## 19. Practice Checklist

- [ ] Configure Git name and email.
- [ ] Create and clone a GitHub repository.
- [ ] Create a branch, edit a file, stage it, commit it, and push it.
- [ ] Open and merge a pull request.
- [ ] Add suitable ignore rules.
- [ ] Practice resolving a merge conflict.
- [ ] Regularly use `git status`, `git diff`, and `git log`.
- [ ] Explore a workflow in `.github/workflows/`.

## 20. Useful Resources

- [Git documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)
- [Learn Git Branching](https://learngitbranching.js.org/)
- [GitHub Skills](https://skills.github.com/)

---

## Key Takeaway

Git tracks a project's local history. GitHub hosts Git repositories and adds collaboration, review, planning, and automation. A strong habit is: work on a branch, inspect changes, stage intentionally, commit clearly, push safely, and merge reviewed changes through pull requests.

