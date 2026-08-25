#!/bin/zsh
# Point clinepropertymgmt.com at GitHub Pages via the Porkbun API.
#
# Credentials are read from a local file you create -- they are never passed on
# the command line, never echoed, and never leave this machine except in the
# API call itself. Same shape as `gh` CLI auth.
#
# Create ~/.porkbun.json containing:
#   { "apikey": "pk1_...", "secretapikey": "sk1_..." }
# then:  chmod 600 ~/.porkbun.json
#
#   ./build/porkbun-dns.sh           # show what WOULD change; changes nothing
#   ./build/porkbun-dns.sh --apply   # make the changes
set -e

CREDS="${PORKBUN_CREDS:-$HOME/.porkbun.json}"
DOMAIN="clinepropertymgmt.com"
TARGET="colsonrice.github.io"
GH_IPS=(185.199.108.153 185.199.109.153 185.199.110.153 185.199.111.153)
API="https://api.porkbun.com/api/json/v3"
APPLY=0
[ "$1" = "--apply" ] && APPLY=1

if [ ! -f "$CREDS" ]; then
  echo "No credentials at $CREDS"
  echo
  echo "In Porkbun:"
  echo "  1. Account -> API Access -> create an API key. Copy BOTH the key and the secret."
  echo "  2. Domain Management -> $DOMAIN -> switch API ACCESS on for this domain."
  echo "     (Porkbun requires this per-domain toggle; the key alone is not enough.)"
  echo "  3. Save them:"
  echo "       printf '%s' '{\"apikey\":\"pk1_...\",\"secretapikey\":\"sk1_...\"}' > ~/.porkbun.json"
  echo "       chmod 600 ~/.porkbun.json"
  exit 1
fi

auth() { python3 -c "
import json,sys
c=json.load(open('$CREDS'))
extra=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
print(json.dumps({'apikey':c['apikey'],'secretapikey':c['secretapikey'],**extra}))
" "${1:-\{\}}"; }

call() { # call <path> [extra-json]
  curl -sS --max-time 25 -X POST "$API/$1" \
    -H "Content-Type: application/json" -d "$(auth "${2:-{\}}")"
}

echo "== auth check =="
ping=$(call ping)
echo "$ping" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print('  status:',d.get('status'))
if d.get('status')!='SUCCESS': print('  message:',d.get('message','')); raise SystemExit(1)"

echo
echo "== current records on $DOMAIN =="
recs=$(call "dns/retrieve/$DOMAIN")
echo "$recs" | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('status')!='SUCCESS':
    print('  ERROR:',d.get('message'))
    print('  (usually means API ACCESS is not switched on for this domain)')
    raise SystemExit(1)
for r in d['records']:
    print(f\"  [{r['id']:>10}] {r['type']:<6} {r['name']:<34} -> {r['content']}\")"

# ids to remove: apex A records, and any www A/CNAME/ALIAS
doomed=$(echo "$recs" | python3 -c "
import sys,json
d=json.load(sys.stdin); out=[]
for r in d['records']:
    apex = r['name']=='$DOMAIN'
    www  = r['name']=='www.$DOMAIN'
    if apex and r['type'] in ('A','ALIAS','CNAME'): out.append(r['id'])
    if www and r['type'] in ('A','ALIAS','CNAME'):  out.append(r['id'])
print(' '.join(out))")

echo
echo "== plan =="
[ -n "$doomed" ] && echo "  delete record ids: $doomed" || echo "  nothing to delete"
for ip in "${GH_IPS[@]}"; do echo "  create A      $DOMAIN -> $ip"; done
echo "  create CNAME  www.$DOMAIN -> $TARGET"

if [ "$APPLY" != "1" ]; then
  echo
  echo "Dry run. Nothing changed. Re-run with --apply to do it."
  exit 0
fi

echo
echo "== applying =="
for id in ${=doomed}; do
  r=$(call "dns/delete/$DOMAIN/$id")
  echo "  deleted $id: $(echo "$r" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("status"))')"
done
for ip in "${GH_IPS[@]}"; do
  r=$(call "dns/create/$DOMAIN" "{\"type\":\"A\",\"name\":\"\",\"content\":\"$ip\",\"ttl\":\"600\"}")
  echo "  A $ip: $(echo "$r" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("status"))')"
done
r=$(call "dns/create/$DOMAIN" "{\"type\":\"CNAME\",\"name\":\"www\",\"content\":\"$TARGET\",\"ttl\":\"600\"}")
echo "  CNAME www: $(echo "$r" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("status"))')"

echo
echo "== verify (may take a minute to propagate) =="
sleep 5
dig +short "$DOMAIN" A | sed 's/^/  A: /'
echo
echo "Next: ./build/go-live.sh   (checks readiness, then --apply to switch the site over)"
