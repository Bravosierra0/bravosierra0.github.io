#!/bin/zsh
# Checks the site before a push. Run from the repo root: ./check.zsh
# Exit code 0 = no FAIL. WARN lines do not block.

emulate -L zsh
setopt extended_glob null_glob

root=${0:A:h}
cd $root || exit 2

fails=0
warns=0
fail() { print -r -- "FAIL  $1"; (( fails++ )) }
warn() { print -r -- "WARN  $1"; (( warns++ )) }
ok()   { print -r -- "ok    $1" }

# Published pages: every .html outside folders that start with "_".
pages=( **/*.html~_*/*~_* )

required_privacy=(
  "Your data"
  "Third parties"
  "Data on your device"
  "Delete your data"
  "Changes"
  "Controller and contact"
)

# 1. Internal links and assets resolve to a file.
for p in $pages; do
  for ref in ${(f)"$(grep -oE '(href|src)="[^"]+"' $p | sed -E 's/^(href|src)="//; s/"$//')"}; do
    case $ref in
      http://*|https://*|mailto:*|\#*|\{\{*) continue ;;
    esac
    target=${ref%%\#*}
    target=${target%%\?*}
    [[ -z $target ]] && continue
    if [[ $target == /* ]]; then
      file=$root$target
    else
      file=${p:h}/$target
    fi
    [[ $target == */ || -d $file ]] && file=$file/index.html
    [[ -e $file ]] || fail "$p: broken link $ref"
  done
done
(( fails == 0 )) && ok "internal links"

# 2. Placeholders left in published pages.
for p in $pages; do
  n=$(grep -c '{{' $p)
  (( n > 0 )) && warn "$p: $n placeholder line(s) ({{...}})"
done

# 3. No third-party resources (fonts, scripts, styles, images).
for p in $pages; do
  grep -qE '<(script|img|iframe)[^>]+src="https?://' $p && fail "$p: external src"
  grep -E '<link[^>]+rel="(stylesheet|preload|icon)[^"]*"' $p | grep -q 'href="https\?://' && fail "$p: external stylesheet or font"
done
grep -qE 'url\(["'"'"']?https?://' site.css && fail "site.css: external url()"

# 4. Every app folder has support, privacy, a redirect stub and a start page row.
for dir in */support.html(:h); do
  [[ $dir == _* ]] && continue
  [[ -f $dir/privacy.html ]] || fail "$dir: privacy.html missing"
  [[ -f $dir.html ]]         || fail "$dir: redirect stub $dir.html missing"
  grep -q "id=\"$dir\"" index.html || fail "$dir: no row with id=\"$dir\" in index.html"
  grep -q "/$dir/support.html" index.html || fail "$dir: start page does not link support"
  grep -q "/$dir/privacy.html" index.html || fail "$dir: start page does not link privacy"
  grep -q 'href="mailto:' $dir/support.html || fail "$dir/support.html: no mailto link"
  grep -q 'href="mailto:' $dir/privacy.html || fail "$dir/privacy.html: no mailto link"
  for s in $required_privacy; do
    grep -qF -- "[ $s ]" $dir/privacy.html || fail "$dir/privacy.html: section '$s' missing"
  done
  grep -qE 'class="sub">.*rev: [0-9]{8}</p>' $dir/privacy.html || fail "$dir/privacy.html: no rev date under the title"
done

# 5. Required root files.
for f in index.html privacy.html 404.html CNAME site.css favicon.ico; do
  [[ -f $f ]] || fail "$f missing"
done

grep -qE 'class="sub">.*rev: [0-9]{8}</p>' privacy.html || fail "privacy.html: no rev date under the title"

# 6. One rev date across the site. Any rev format counts, so a leftover old date shows up.
revs=( ${(u)${(f)"$(grep -ohE 'rev:? [0-9][0-9-]*[0-9]' $pages | grep -oE '[0-9][0-9-]*[0-9]$')"}} )
(( ${#revs} > 1 )) && warn "different rev dates: ${(j:, :)revs}"

print -- "--"
print -- "$fails fail, $warns warn"
(( fails == 0 ))
