#!/bin/zsh
# Move the site from the borrowed squatchcraft path onto its own domain.
#
# Run this ONLY once clinepropertymgmt.com's A records point at GitHub Pages.
# Adding the CNAME file is what tells GitHub to serve this repo at the apex
# domain -- do it while DNS still points at Porkbun parking and the site is
# simply down until DNS catches up.
#
#   ./build/go-live.sh            # check readiness, make no changes
#   ./build/go-live.sh --apply    # make the changes, build, commit, deploy
set -e
cd "$(dirname "$0")/.."

DOMAIN="clinepropertymgmt.com"
GH_IPS=(185.199.108.153 185.199.109.153 185.199.110.153 185.199.111.153)
APPLY=0
[ "$1" = "--apply" ] && APPLY=1

echo "== DNS readiness for $DOMAIN =="
live=$(dig +short "$DOMAIN" A 2>/dev/null | sort)
if [ -z "$live" ]; then
  echo "  no A records at all -- nothing set yet"
  ready=0
else
  ready=1
  for ip in "${GH_IPS[@]}"; do
    if echo "$live" | grep -q "^${ip}$"; then
      echo "  ok      $ip"
    else
      echo "  MISSING $ip"
      ready=0
    fi
  done
  extra=$(echo "$live" | grep -vE "$(printf '%s|' "${GH_IPS[@]}" | sed 's/|$//')" || true)
  [ -n "$extra" ] && { echo "  stale records still present:"; echo "$extra" | sed 's/^/    /'; ready=0; }
fi

echo
echo "== www =="
w=$(dig +short "www.$DOMAIN" CNAME 2>/dev/null)
[ -n "$w" ] && echo "  CNAME -> $w" || echo "  no www CNAME (optional, but recommended)"

if [ "$ready" != "1" ]; then
  echo
  echo "NOT READY. Point DNS first, then re-run. Nothing has been changed."
  exit 1
fi

echo
if [ "$APPLY" != "1" ]; then
  echo "READY. Re-run with --apply to switch the site over."
  exit 0
fi

echo "== applying =="
echo "$DOMAIN" > site/CNAME
echo "  wrote site/CNAME"

python3 - <<PY
import re
p = "build/data.py"
s = open(p, encoding="utf-8").read()
s = re.sub(r'"base":\s*"[^"]*"', '"base": "https://$DOMAIN"', s, count=1)
s = re.sub(r'^STAGING\s*=\s*True', 'STAGING = False', s, count=1, flags=re.M)
open(p, "w", encoding="utf-8").write(s)
PY
python3 -c "import sys;sys.path.insert(0,'build');import data;print('  base   :',data.SITE['base']);print('  STAGING:',data.STAGING)"

python3 build/build.py > /dev/null && echo "  rebuilt"
python3 build/qa.py 2>&1 | tail -4

echo
echo "  robots.txt now:"
sed 's/^/    /' site/robots.txt

git add -A
git -c user.name="Colson Rice" -c user.email="colsonrice@gmail.com" commit -q -m "Move the site onto clinepropertymgmt.com and allow indexing

Adds site/CNAME so GitHub Pages serves this repo at the apex domain
instead of as a path under the squatchcraft user site, points every
canonical, OG tag and sitemap entry at the new domain, and clears the
STAGING flag now that the address is permanent.

The old squatchcraft.com/cline-property-management path stops working;
that is the intended consequence of giving the project its own domain.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push -q origin main
git subtree push --prefix site origin gh-pages 2>&1 | tail -1
echo
echo "Deployed. GitHub still needs a few minutes to issue the TLS certificate."
echo "Check: https://$DOMAIN"
