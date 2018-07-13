#/usr/bin/env bash

if [ $# -ne 3 ]; then
    echo 'Usage: batch.sh directory lang out_encode'
    exit 1
fi

dir=$1
lang=$2
pattern=$2u
encode=$3

echo "Working on directory:$dir"
echo "Language: $lang"

for f in $(ls $dir/*${pattern}*); do
    fin=${f}
    fout=${f}."tok"
    echo $fin
    echo $fout
    python tools/my_tokenizer.py --fin $fin --fout $fout --in_encode utf-8 --out_encode $encode --lang $lang
done

