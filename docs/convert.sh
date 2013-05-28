for f in `find markdown -name '*.md'`; do
    full=`echo $f | sed -r 's/^.{9}//' | sed -r 's/.{3}$$//'`
    pandoc $f -r markdown_github -o rst/$full.rst
done
