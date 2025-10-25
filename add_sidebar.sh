#!/bin/bash
# Add Sidebar import and wrapper to pages

pages=(
  "app/skill-gaps/page.tsx"
  "app/rl-viz/page.tsx"
  "app/learning-style-quiz/page.tsx"
  "app/learning-style-results/page.tsx"
)

for page in "${pages[@]}"; do
  echo "Processing $page"
  # Check if already has Sidebar
  if grep -q "import Sidebar" "$page"; then
    echo "  Already has Sidebar import"
  else
    echo "  Adding Sidebar import"
  fi
done
