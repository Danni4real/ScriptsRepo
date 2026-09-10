#!/bin/sh
server=192.168.20.27
username=ubuntu
password=27@hsaeyz
local_bin_dir=./bin
local_src_dir=/home/dan/workspace/AvmServer
server_src_dir=/home/ubuntu/android_department/nidan/QM/packages/apps/Hsae_Apps/AvmServer
server_bin_dir=/home/ubuntu/android_department/nidan/QM/out/target/product/mek_8q/system/bin
server_so_dir=/home/ubuntu/android_department/nidan/QM/out/target/product/mek_8q/system/lib

#flag file which tells server that scp has finished, it can compile now
flag_file=file_changed
#flag file which tells us that server has finished compile   		
flag_file_from_server=build_finish 	

#start scp
./scp_expect $server $username $password $local_src_dir $server_src_dir main_avmserver.cpp
./scp_expect $server $username $password $local_src_dir $server_src_dir adas.h
./scp_expect $server $username $password $local_src_dir $server_src_dir BackCarCommon.h
./scp_expect $server $username $password $local_src_dir $server_src_dir log.h
./scp_expect $server $username $password $local_src_dir $server_src_dir log.cpp
./scp_expect $server $username $password $local_src_dir $server_src_dir AvmClient.h
./scp_expect $server $username $password $local_src_dir $server_src_dir AvmClient.cpp
./scp_expect $server $username $password $local_src_dir $server_src_dir AvmService.h
./scp_expect $server $username $password $local_src_dir $server_src_dir AvmService.cpp
./scp_expect $server $username $password $local_src_dir $server_src_dir MultiThread.h
./scp_expect $server $username $password $local_src_dir $server_src_dir MultiThread.cpp
./scp_expect $server $username $password $local_src_dir $server_src_dir IAvmService.h
./scp_expect $server $username $password $local_src_dir $server_src_dir IAvmService.cpp
./scp_expect $server $username $password $local_src_dir $server_src_dir IAvmCallBack.h
./scp_expect $server $username $password $local_src_dir $server_src_dir IAvmCallBack.cpp
./scp_expect $server $username $password $local_src_dir $server_src_dir BackCarOverlay.h
./scp_expect $server $username $password $local_src_dir $server_src_dir BackCarOverlay.cpp
./scp_expect $server $username $password $local_src_dir $server_src_dir InputManagerService.h
./scp_expect $server $username $password $local_src_dir $server_src_dir InputManagerService.cpp


#tell server to compile,and remove flag file
touch  $local_src_dir/$flag_file
./scp_expect $server $username $password $local_src_dir $server_src_dir $flag_file
rm -rf $local_src_dir/$flag_file

#wait server to compile completed, and remove flag file
./scp_expect_from $server $username $password $local_src_dir $server_src_dir $flag_file_from_server
rm -rd $local_src_dir/$flag_file_from_server

#fetch bin file from server
./scp_expect_from $server $username $password $local_bin_dir $server_bin_dir avmserver
./scp_expect_from $server $username $password $local_bin_dir $server_so_dir libavmserver.so
