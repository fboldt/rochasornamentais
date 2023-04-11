#!/bin/bash


userAgent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0"

function pdfIsGood(){
    f="$1"
    if ! pdfinfo "$f" &> /dev/null;then
       return 1
    else
        return 0
    fi
}

function ifExist(){
    f="$1"
    if [ ! -e "$f" ];then
       return 0
    else
        return 1
    fi
}




function usage(){
	echo -e "Help
-l <string> \tlist of data
-d <string> \tset path to save documents
-o \tsave output file

"
exit
}

unset _data _path _out
#By default, this script simulate only 20 scrollings on subreddit
_number=20
_preview=false
while getopts ':l:d:o:' c;
do
	case $c in
		l) _data=$OPTARG ;;
		d) _path=$OPTARG ;;
        o) _out=$OPTARG;;
		*) usage ;;
	esac
done


if [ -z "$_data" ] || [ -z "$_path" ];
then
	usage
fi


declare -a dependecies=("jq" "wget" "tr" "curl" )

err=0

for i in "${dependecies[@]}"
do
   if ! command -v "$i" > /dev/null;then
    echo "$i not found!"
    err=1
   fi
done


if [ $err -eq 1 ]; then
    echo "Install programs not found!!!!!"
    exit
fi



mkdir -p "$_path"
mkdir -p "$_path/documents/"
mkdir -p "$_path/texts/"



if [ -z "$_out" ];
then
    rm out.csv
	_out="log.csv"
fi





cont=1
max=`wc -l $_data | awk '{print $1}'`

while read line
do
    title=`echo $line | cut -d ';' -f1 | sed -e 's/ /_/g;s/\//_/g;s/[,.;:~^ºª@#!$%&*()?!]/_/g'`
    link=`echo $line | cut -d ';' -f3`
    label=`echo $line | cut -d ';' -f2`
    echo "$cont/$max"
    let cont=$cont+1
    
    if  [ ! -e  "$_path/documents/$title.pdf" ];then
        wget --user-agent="$userAgent" -w 5 -c -O "$_path/documents/$title.pdf" "$link" -q --show-progress
    fi
    
    if pdfIsGood "$_path/documents/$title.pdf" ;then
        # REMOVE CARACTERES NÃO RECONHECIDOS NA UTF-8
        # tr -cd '\11\12\15\40-\176'
        # curl -s -X POST -F "file=@$_path/documents/$title.pdf" localhost:5000 | jq -r .text |tr -cd '\11\12\15\40-\176' > "$_path/texts/$title.txt"
        echo "$_path/documents/$title.pdf;$label" >> $_out
        
    else 
        rm "$_path/documents/$title.pdf"
        # echo $link >> $_out
    fi
    

done < $_data
