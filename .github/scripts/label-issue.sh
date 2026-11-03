#!/usr/bin/env bash
# Applies the area:* and priority:* labels chosen in an issue form.
# Issue forms render a dropdown as "### <Label>\n\n<value>" in the body.
# Inputs (env): ISSUE_NUMBER, ISSUE_BODY, GH_REPO, GH_TOKEN
set -euo pipefail

value_after() {
  printf '%s\n' "$ISSUE_BODY" | tr -d '\r' | awk -v h="### $1" '
    $0 == h { found = 1; next }
    found && NF { print; exit }'
}

labels=()
for heading in Area Priority; do
  v=$(value_after "$heading")
  if [[ $v =~ ^(area|priority):[a-z]+$ ]]; then
    labels+=("$v")
  fi
done

if (( ${#labels[@]} == 0 )); then
  echo "No form labels found; nothing to apply."
  exit 0
fi

args=()
for l in "${labels[@]}"; do args+=(--add-label "$l"); done
gh issue edit "$ISSUE_NUMBER" --repo "$GH_REPO" "${args[@]}"
echo "Applied: ${labels[*]}"
