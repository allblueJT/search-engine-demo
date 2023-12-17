crawlers=("scs.py" "sds.py" "teach.py" "mathematics.py" "sist.py" "sse.py" "press.py" "grad.py")

cd crawl

for crawler in "${crawlers[@]}"; 
do
    echo "Running crawler: $crawler"
    python $crawler --debug True --verbose True
done