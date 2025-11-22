# GitHub Repository Setup Guide

This guide will help you turn your project into a GitHub repository and push it to GitHub.

## Prerequisites

- Git installed on your computer
- A GitHub account (create one at https://github.com if you don't have one)
- GitHub CLI (`gh`) is optional but helpful

## Step-by-Step Instructions

### Step 1: Initialize Git Repository

Open your terminal and navigate to your project directory:

```bash
cd /Users/shaansriram/Desktop/ECE570-Final-Project
```

Initialize a git repository:

```bash
git init
```

### Step 2: Add All Files to Git

Add all files to the staging area:

```bash
git add .
```

**Note:** The `.gitignore` file will automatically exclude:
- `.env` files (containing API keys)
- `__pycache__/` directories
- `node_modules/` (if you add frontend later)
- Log files and other temporary files

### Step 3: Make Your First Commit

Create your initial commit:

```bash
git commit -m "Initial commit: AI Code Quality & Bug Explanation Assistant backend"
```

### Step 4: Create GitHub Repository

You have two options:

#### Option A: Using GitHub Website (Recommended for beginners)

1. Go to https://github.com and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name:** `ece570-ai-debugging-assistant` (or your preferred name)
   - **Description:** "AI-powered code debugging assistant that analyzes code and error messages to provide structured explanations and fix suggestions"
   - **Visibility:** Choose **Private** (for academic work) or **Public**
   - **DO NOT** check "Initialize with README" (you already have files)
   - **DO NOT** add .gitignore or license (you already have them)
5. Click **"Create repository"**

#### Option B: Using GitHub CLI

If you have GitHub CLI installed:

```bash
gh repo create ece570-ai-debugging-assistant --private --source=. --remote=origin --push
```

This will create the repo, add it as a remote, and push your code in one command.

### Step 5: Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see a page with setup instructions. Use the "push an existing repository" option:

```bash
# Add GitHub repository as remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/ece570-ai-debugging-assistant.git

# Or if you prefer SSH (if you have SSH keys set up):
# git remote add origin git@github.com:USERNAME/ece570-ai-debugging-assistant.git
```

**Replace `USERNAME` with your actual GitHub username.**

### Step 6: Push Your Code to GitHub

Push your code to the main branch:

```bash
# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

You may be prompted for your GitHub username and password. If you have two-factor authentication enabled, you'll need to use a Personal Access Token instead of your password.

### Step 7: Verify on GitHub

1. Go to https://github.com/USERNAME/ece570-ai-debugging-assistant
2. You should see all your files there!

## Quick Reference Commands

```bash
# Check status
git status

# See what files are tracked/ignored
git status --ignored

# Add specific file
git add filename

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes (if working from multiple locations)
git pull

# View commit history
git log

# See remote repositories
git remote -v
```

## Important: Protecting Sensitive Information

Before pushing, make sure:

✅ **`.env` file is in `.gitignore`** (it should be - check the .gitignore file)
✅ **No API keys in code** - All secrets should be in `.env` which is ignored
✅ **`env.example` is committed** - This shows what environment variables are needed without exposing values

To verify nothing sensitive is being committed:

```bash
# Check if .env would be committed (should show nothing)
git check-ignore .env

# See what files will be committed
git status
```

## Setting Up GitHub Repository Settings

After creating the repository, consider:

1. **Add a README description** on the GitHub repository page
2. **Add topics/tags** like: `python`, `fastapi`, `ai`, `debugging`, `ece570`
3. **Set up branch protection** (optional, for academic projects)
4. **Add collaborators** (if working with a team)

## Future Updates

When you make changes to your code:

```bash
# 1. Check what changed
git status

# 2. Add changed files
git add .

# 3. Commit with descriptive message
git commit -m "Description of what you changed"

# 4. Push to GitHub
git push
```

## Troubleshooting

### "Repository not found" error
- Check that the repository name and your username are correct
- Verify you have access to the repository

### "Authentication failed" error
- Use a Personal Access Token instead of password
- Generate one at: https://github.com/settings/tokens
- Use the token as your password when prompted

### "Permission denied" error
- Make sure you're using the correct remote URL
- Check your SSH keys if using SSH

### Want to change the remote URL?
```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/USERNAME/NEW-REPO-NAME.git
```

## Next Steps

Once your code is on GitHub:

1. **Clone on another machine:**
   ```bash
   git clone https://github.com/USERNAME/ece570-ai-debugging-assistant.git
   ```

2. **Share with others:**
   - Share the repository URL
   - Add collaborators via Settings → Collaborators

3. **Create releases/tags:**
   - Tag important versions (e.g., v1.0.0 for final submission)

4. **Add GitHub Actions** (optional):
   - Set up CI/CD for automated testing
   - Auto-deploy documentation

## Repository Structure on GitHub

Your repository should look like this on GitHub:

```
ece570-ai-debugging-assistant/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── config.py
│   ├── hf_client.py
│   ├── aggregator.py
│   ├── json_handler.py
│   ├── scorer.py
│   ├── cache.py
│   ├── evaluator.py
│   ├── requirements.txt
│   ├── README.md
│   ├── BACKEND_REPORT.md
│   └── ...
├── cursor.md
├── LOVABLE_PROMPT.md
├── .gitignore
└── README.md (you may want to create a root-level one)
```

## Creating a Root-Level README

You might want to create a `README.md` at the root level that explains the entire project:

```markdown
# ECE 570 - AI Code Quality & Bug Explanation Assistant

[Brief project description]

## Project Structure

- `backend/` - FastAPI backend service
- `frontend/` - React/TypeScript frontend (to be added)

## Quick Start

[Instructions for running the project]

## Documentation

- Backend documentation: See `backend/README.md`
- Backend report: See `backend/BACKEND_REPORT.md`
```

---

**Need help?** Check GitHub's documentation: https://docs.github.com/en/get-started

