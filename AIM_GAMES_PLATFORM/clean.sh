python manage.py flush --noinput
python manage.py migrate
python manage.py create_groups
python manage.py populate
echo
read -n 1 -p "Press enter to close this window"