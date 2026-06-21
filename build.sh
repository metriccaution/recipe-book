set -e

echo "Testing data"
./test.sh > /dev/null

echo "Exporting JSON data"
uv run python -m housekeeping export_json recipes exported

echo "Exporting Linked Data data"
uv run python -m housekeeping json_ld_export recipes exported

echo "Exporting PDF generation data"
uv run python -m housekeeping typst_export recipes exported

# Build the PDF
cp -r exported/pdf ./book/data
typst compile ./book/recipes.typ

# Build the site
cp exported/full/repo.json site/public/repo.json
cp -r ./exported/json_ld site/public/
cp ./book/recipes.pdf site/public/cookbook.pdf
pushd site
BASE_PATH="/" npm run build
popd
