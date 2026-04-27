
# Git Usage Notes

## Create the repo
```bash
# 1. Initialize the repo
git init

# 2. Stage everything
git add .

# 3. First commit
git commit -m "Initial commit"

# 4. Create the remote repo on GitHub and push
gh repo create jumpack-01 --public --source=. --remote=origin --push

```

## If the repo already exists on github
```bash
git remote add origin https://github.com/LouisB-CA/jumpack-01.git
git branch -M main
git push -u origin main
```



