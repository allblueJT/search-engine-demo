crawlers=("scs.py" "sds.py" "teach.py")

cd crawl

for crawler in "${crawlers[@]}"; 
do
    echo "Running crawler: $crawler"
    python $crawler --debug True
done