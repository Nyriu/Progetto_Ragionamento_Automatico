i=3
DIR=./batches/input_batch_$(printf %02d $i)/

if [[ -e $DIR || -L $DIR ]] ; then
    while [[ -e $DIR || -L $DIR ]] ; do
        let i++
        DIR=./batches/input_batch_$(printf %02d $i)/
    done
    DIR=./batches/input_batch_$(printf %02d $i)/
fi

mkdir -p $DIR

cp ./*.png  $DIR
cp ./*.mzn  $DIR
cp -r ./inputs  $DIR
cp -r ./outputs  $DIR


