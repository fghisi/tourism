export SRC_PATH="$( dirname "${BASH_SOURCE[0]}" )"

export $(cat $SRC_PATH/.environment | xargs)

echo ""
echo "     host:" $PGHOST
echo "     port:" $PGPORT
echo "     user:" $PGUSER
echo " password:" $PGPASSWORD
echo " database:" $PGDATABASE
echo ""