#Commands used to run registration script

#Commands used to register user 1
cd tc && /ats/bin/sipp -i 10.54.81.66 -p 15070 -sf Register_UAC.xml -inf register.csv 10.54.81.66:15088 -m 1 -trace_msg -message_file /home/vkonreddi/tc/register_uac.log

cd tc && /ats/bin/sipp -i 10.54.81.66 -p 15088 -sf Register_UAS.xml -inf users.csv -m 1 -trace_msg -message_file /home/vkonreddi/tc/register_uas.log

#Commands used to register user 2
cd tc && /ats/bin/sipp -i 10.54.81.66 -p 15070 -sf Register_UAC.xml -inf register1.csv 10.54.81.66:15088 -m 1 -trace_msg -message_file /home/vkonreddi/tc/register_uac1.log

cd tc && /ats/bin/sipp -i 10.54.81.66 -p 15088 -sf Register_UAS.xml -inf users1.csv  -m 1 -trace_msg -message_file /home/vkonreddi/tc/register_uas1.log


#commands used to run voice call

/ats/bin/sipp -sf /home/vkonreddi/tc/uac.xml -i 10.54.81.66 -p 15070  -inf /home/vkonreddi/tc/call.csv 10.54.81.66:15088 -m 1  -trace_msg -message_file /home/vkonreddi/tc/uac_messages.log

cd tc && /ats/bin/sipp -sf /home/vkonreddi/tc/uas.xml -i 10.54.81.66 -p 15088  -inf /home/vkonreddi/tc/call.csv 10.54.81.66:15070 -m 1  -screen_file /home/vkonreddi/tc/uas_screen_file -trace_screen -trace_msg -message_file /home/vkonreddi/tc/uas_messages.log

