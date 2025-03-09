# DEPLOY.ps1 - One-Click GitHub Deployment
param(
    [string]$RepoName,
    [string]$Description = "Firecrawl Scraper"
)

# 1. GitHub Connection
$GitHubUser = "Abdulraqib20"
git remote set-url origin "https://github.com/$GitHubUser/$RepoName.git"

# 2. Project Branding
@"
# $RepoName

$Description

## Features
- [ ] TODO: Add features

## Setup
\`\`\`bash
git clone https://github.com/$GitHubUser/$RepoName.git
pip install -r requirements.txt
\`\`\`
"@ | Out-File README.md -Encoding UTF8

# 3. Smart .gitignore
@"
__pycache__/
.env
*.pdf
*.log
.DS_Store
"@ | Out-File .gitignore -Encoding UTF8

# 4. Atomic Commit
git add --all
git commit -m "🚀 Initial deploy: $RepoName

- Core implementation
- Deployment pipeline
- Documentation baseline"

# 5. Force Push
git push -u origin main --force

Write-Host "✅ Success! Live at: https://github.com/$GitHubUser/$RepoName" -ForegroundColor Green


# 1. Create empty repo on GitHub first
# 2. Run the below in PowerShell:

# ./deploy.ps1 -RepoName "your-repo-name" -Description "Project purpose"

# 3. Credential Caching (One-Time Setup):
# git config --global credential.helper wincred


