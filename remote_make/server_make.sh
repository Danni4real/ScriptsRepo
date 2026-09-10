#!/bin/sh

file_changed_flag_file_path="/home/ubuntu/android_department/nidan/QM/packages/apps/Hsae_Apps/AvmServer/file_changed"
build_finish_flag_file_path="/home/ubuntu/android_department/nidan/QM/packages/apps/Hsae_Apps/AvmServer/build_finish"


cd /home/ubuntu/android_department/nidan/QM
source build/envsetup.sh
lunch 33
cd /home/ubuntu/android_department/nidan/QM/packages/apps/Hsae_Apps/AvmServer


rm -rf "$file_changed_flag_file_path"
rm -rf "$build_finish_flag_file_path"


echo "my watch start!"

while [ 1 = 1 ]
do
sleep 1


if [ -f "$file_changed_flag_file_path" ]; then
echo "compiling!"
rm -rf "$file_changed_flag_file_path"
mm
touch "$build_finish_flag_file_path"
sleep 5
rm -rf "$build_finish_flag_file_path"
echo "compiling completed!"
echo "still watching!"
fi


done
