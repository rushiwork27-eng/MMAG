#!/usr/bin/env bash
# Usage: linkcheck.sh <urls.txt> <out.csv>
# Checks each URL with HEAD, falls back to a 1-byte GET when HEAD is refused.
IN="$1"; OUT="$2"
check() {
  u="$1"
  r=$(curl -sS -o /dev/null -I -L --max-redirs 5 -m 25 -A "Mozilla/5.0 (site-audit link check)" -w '%{http_code}\t%{url_effective}' "$u" 2>/dev/null)
  code=${r%%$'\t'*}
  if [ -z "$code" ] || [ "$code" = "000" ] || [ "$code" = "405" ] || [ "$code" = "403" ] || [ "$code" = "400" ] || [ "$code" = "404" ] || [ "$code" = "999" ]; then
    r=$(curl -sS -o /dev/null -L --max-redirs 5 -m 25 -r 0-0 -A "Mozilla/5.0 (site-audit link check)" -w '%{http_code}\t%{url_effective}' "$u" 2>/dev/null)
    code=${r%%$'\t'*}
  fi
  final=${r#*$'\t'}
  printf '"%s",%s,"%s"\n' "$u" "${code:-000}" "$final"
}
export -f check
echo "url,status,final" > "$OUT"
grep -E '^https?://' "$IN" | sort -u | xargs -P 8 -I{} bash -c 'check "$@"' _ {} >> "$OUT"
