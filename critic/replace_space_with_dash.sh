path=$1
cd $path;

for oldname in *
do
  newname=`echo $oldname | sed -e 's/:/-/g'`
  mv "$oldname" "$newname"
done

for oldname in *
do
  newname=`echo $oldname | sed -e 's/ /-/g'`
  mv "$oldname" "$newname"
done