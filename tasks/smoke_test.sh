#!/bin/sh
# sleep 15
# if [ "$SERVICE_INTERNAL_URL" == "testapp.prod-2.svc.cluster.local" ]; then
#    echo "Test failed"
#    exit 1;
# fi
sleep 10
for i in 1 2 3 4 5
do
   echo $SERVICE_INTERNAL_URL
   resp=$(curl $SERVICE_INTERNAL_URL:5000/)
   if [ "$resp" != "Hello, World!" ]; then
      echo "Did not return correctly."
      exit 1;
   fi
   sleep 1
done
echo "Test completed correctly."