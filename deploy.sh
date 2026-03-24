#!/bin/bash

# PolicyPulse One-Click Deploy Script
# ✅ Requires: gh CLI + authenticated GitHub account
# ✅ Safe: no passwords, no tokens, no manual input

set -e

echo "🚀 PolicyPulse Deploy Starting..."

echo "➡️  Checking GitHub CLI..."
if ! command -v gh &> /dev/null; then
  echo "❌ Error: 'gh' CLI not found. Install with: https://github.com/cli/cli#installation"
  exit 1
fi

echo "➡️  Verifying GitHub auth..."
if ! gh auth status &> /dev/null; then
  echo "❌ Error: Not authenticated with GitHub. Run 'gh auth login' first."
  exit 1
fi

USERNAME=$(gh api user | jq -r '.login')
if [ "$USERNAME" = "null" ]; then
  echo "❌ Error: Could not fetch GitHub username. Check auth."
  exit 1
fi

echo "✅ Authenticated as: $USERNAME"

echo "➡️  Creating GitHub repo: $USERNAME/policypulse"
gh repo create policypulse --public --source=. --remote=origin --description="PolicyPulse — Real-time PBOC & RMB signal widget for Shenzhen fintechs" || true

echo "➡️  Setting up Git..."
git init > /dev/null 2>&1 || true
git add policypulse-szse-widget.html > /dev/null 2>&1
git commit -m "PolicyPulse MVP: Shenzhen policy widget" > /dev/null 2>&1

echo "➡️  Pushing to GitHub..."
git branch -M main > /dev/null 2>&1
git remote add origin https://github.com/$USERNAME/policypulse.git > /dev/null 2>&1
git push -u origin main > /dev/null 2>&1

echo "➡️  Enabling GitHub Pages..."
gh pages deploy --build-output . --allow-empty > /dev/null 2>&1

echo "✅ Deployment Complete!"
echo ""
echo "🌐 Your live widget is now at:" 
echo "   https://$USERNAME.github.io/policypulse/"
echo ""
echo "📎 To embed anywhere (WeCom/DingTalk):"
echo "   <iframe src=\"https://$USERNAME.github.io/policypulse/policypulse-szse-widget.html\" width=\"100%\" height=\"320\" frameborder=\"0\" style=\"border-radius:12px;border:1px solid #334155;\"></iframe>"
echo ""
echo "💡 Tip: Share this URL with your first client — it updates live as soon as you push new HTML."
