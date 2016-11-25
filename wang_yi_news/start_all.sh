#!/bin/bash
for ((i=1;i<=1;i++))
do
  nohup python zhengwen_producer.py &>/dev/null &
done

for ((i=1;i<=4;i++))
do
  nohup python zhengwen_consumer.py &>/dev/null &
done

for ((i=1;i<=4;i++))
do
  nohup python zhengwen_zw_consumer.py &>/dev/null &
done

for ((i=1;i<=2;i++))
do
  nohup python zhengwen_pinglun_consumer.py &>/dev/null &
done
