# How to Upload This Project to GitHub

## Prerequisites

- GitHub account (create one at https://github.com if you don't have one)
- Git installed on your computer

## Step-by-Step Instructions

### Step 1: Install Git (if not already installed)

**Windows:**
- Download from https://git-scm.com/download/win
- Run installer with default settings

**Mac:**
```bash
# Using Homebrew
brew install git

# Or download from https://git-scm.com/download/mac
```

**Linux:**
```bash
sudo apt install git  # Ubuntu/Debian
sudo yum install git  # CentOS/RHEL
```

### Step 2: Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Create a New Repository on GitHub

1. Go to https://github.com
2. Click the "+" icon in top right → "New repository"
3. Repository name: `california-parks-monitor` (or your preferred name)
4. Description: `AI agent that monitors California national parks for camping availability in June 2026`
5. Choose **Public** or **Private**
6. **DO NOT** check "Initialize with README" (we already have files)
7. Click "Create repository"

### Step 4: Prepare Your Local Repository

Open terminal/command prompt and navigate to your project folder:

```bash
cd /path/to/your/project
```

### Step 5: Initialize Git and Add Files

```bash
# Initialize git repository
git init

# Add all files
git add .

# Check what will be committed
git status

# Commit the files
git commit -m "Initial commit: California National Parks availability monitor"
```

### Step 6: Connect to GitHub and Push

Replace `YOUR_USERNAME` and `REPO_NAME` with your actual GitHub username and repository name:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/johndoe/california-parks-monitor.git
git branch -M main
git push -u origin main
```

### Step 7: Enter GitHub Credentials

When prompted:
- **Username:** Your GitHub username
- **Password:** Use a **Personal Access Token** (not your password)

#### How to Create a Personal Access Token:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Note: `Git operations`
4. Expiration: Choose duration (90 days or custom)
5. Select scopes: Check `repo` (full control of private repositories)
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again!)
8. Use this token as your password when pushing

### Step 8: Verify Upload

1. Go to your GitHub repository URL
2. You should see all your files listed
3. README.md will be displayed automatically

## Alternative: Using GitHub Desktop (Easier for Beginners)

### Step 1: Install GitHub Desktop
- Download from https://desktop.github.com
- Install and sign in with your GitHub account

### Step 2: Add Your Project
1. Click "File" → "Add local repository"
2. Choose your project folder
3. Click "Create repository" if prompted

### Step 3: Publish to GitHub
1. Click "Publish repository" button
2. Choose name and description
3. Select Public or Private
4. Click "Publish repository"

Done! Your project is now on GitHub.

## Important: Protect Sensitive Information

Before pushing, make sure your `config.yaml` contains placeholder values, not real credentials:

```yaml
notifications:
  email:
    sender_email: "your-email@gmail.com"  # ← Placeholder
    sender_password: "your-app-password"   # ← Placeholder
```

The `.gitignore` file already prevents `config.yaml` from being committed if you've edited it.

## After Upload

### Clone Your Repository Elsewhere

To download your project on another computer:

```bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME
pip install -r requirements.txt
cp config.yaml.example config.yaml  # Create your config
nano config.yaml  # Edit with your settings
```

### Update Your Repository

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

### Create a README Badge (Optional)

Add this to the top of your README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
```

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### Error: "failed to push some refs"
```bash
git pull origin main --rebase
git push -u origin main
```

### Error: "Authentication failed"
- Make sure you're using a Personal Access Token, not your password
- Check token has `repo` permissions
- Token might be expired - create a new one

### Large files error
If you have files over 100MB:
```bash
# Remove from git
git rm --cached large-file.ext
# Add to .gitignore
echo "large-file.ext" >> .gitignore
git commit -m "Remove large file"
```

## Making Your Repository Professional

### Add a License

Create `LICENSE` file:
```bash
# For MIT License
curl https://raw.githubusercontent.com/licenses/license-templates/master/templates/mit.txt > LICENSE
```

Edit the LICENSE file to add your name and year.

### Add Topics/Tags

On GitHub repository page:
1. Click the gear icon next to "About"
2. Add topics: `python`, `monitoring`, `national-parks`, `automation`, `recreation-gov`
3. Save changes

### Create a Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Initial Release - California Parks Monitor`
5. Description: Brief overview of features
6. Click "Publish release"

## Sharing Your Project

Your repository URL will be:
```
https://github.com/YOUR_USERNAME/california-parks-monitor
```

Share this link with others who want to use your monitoring tool!

## Next Steps

1. ✅ Upload to GitHub
2. ✅ Add a proper LICENSE file
3. ✅ Add repository topics/tags
4. ✅ Create a release
5. ✅ Share with others
6. ✅ Deploy to Oracle Cloud or other hosting

---

**Congratulations! Your project is now on GitHub! 🎉**