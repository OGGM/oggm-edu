#!/bin/bash
echo "Step 1: gettext"
make gettext
echo "Step 2: sphinx-intl"
sphinx-intl update -p _build/locale/ -l de -l fr -l es
