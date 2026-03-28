py=`python --version`
echo $py
ankiconf="ankisyncd.conf"
ankidir="/data/anki/"
ankisyncd="ankisyncd/"
auth="auth.db"
collection="collections"

if [ ! -d $ankidir ];then
    mkdir $ankidir
    echo "create $ankidir"
else
    echo "exists $ankidir"
fi
if [ ! -d $ankidir$ankisyncd ];then
    mkdir $ankidir$ankisyncd
    echo "create $ankidir$ankisyncd"
else
    echo "exists $ankidir$ankisyncd"
fi
if [ -f $ankidir$ankiconf ]; then
    echo "$ankiconf found"
else
    echo "Creating new configuration file: $ankiconf."
    cp ./conf/$ankiconf $ankidir$ankiconf
fi
if [ -f $ankidir$ankisyncd$ankiconf ]; then
    echo "$ankisyncd$ankiconf found"
else
    echo "ln -s ankisyncd"
    ln -s $ankidir$ankiconf $ankidir$ankisyncd
fi
if [ -f $ankidir$auth ]; then
    echo "$auth found"
else
    echo "Creating new authentication database: $auth."
    sqlite3 $ankidir$auth 'CREATE TABLE auth (username VARCHAR PRIMARY KEY, hash VARCHAR)'
fi
if [ -d $ankidir$collection ]; then
    echo "$collection directory exists"
else
    echo "Creating collections directory: $collection."
    mkdir $ankidir$collection
fi
echo start running ankisyncd
cd ./anki-sync-server/src
python -m ankisyncd