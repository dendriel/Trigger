#!/bin/bash

times=1

for i in 0 1 2 3 4 5
    do
        psql -U trigger -c "insert into sms values ('vitor', '99190777,91553988,96710766,88150420', 'dosiajdadada', 2, '2012-03-11 20:21:00', 0)"
    done
