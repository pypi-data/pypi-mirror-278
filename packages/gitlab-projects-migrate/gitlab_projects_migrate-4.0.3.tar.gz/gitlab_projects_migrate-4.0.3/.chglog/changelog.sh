#!/bin/sh

# Arguments
MODE=${1:-${VERSION}}

# Cleanup changelog file
if [ "${MODE}" = '--clean' ]; then

  # Iterate through changelog commits
  echo '
  changelog: regenerate release tag changes history
  regenerate release tag changes history
  ' | while read -r commit; do
    if [ ! -z "${commit}" ]; then
      sed -i "/* ${commit}/d" ./CHANGELOG.md
    fi
  done

  # Strip empty sections
  sed -i "/^### .*/{
    N;
    N;
    /^### .*\n\n$/{
      d;
    };
  }" ./CHANGELOG.md

# Extract version changelog
else
  sed -n "/^## \[${MODE}\]/,/^## \[/{
    n;
    :a;
    n;
    h;
    /^$/{
      n;
      H;
      /^$/{
        n;
        H;
        /^<a name=/{
          q;
        };
      };
      g;
    };
    p;
    ba;
  }" ./CHANGELOG.md
fi
