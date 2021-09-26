#! /usr/bin/bash

whitelist=()
arrId=()
arrIp=()
arrMac=()

while read line; do
	whitelist+=($line)
done < whitelist.txt

while read line; do
  start=${line:0:13}
	if [ "$start" == "(0x(B [93m" ]
	then
		# ID

		id=${line:13:2}

		if [ "${id:1:1}" == "" ]
		then
			id=${id:0:1}
		fi

		# IP

		ip=${line:28:15}

		if [ "${ip:13:2}" == "  " ]
		then
			ip=${ip:0:13}
		fi

		if [ "${ip:14:1}" == " " ]
		then
			ip=${ip:0:14}
		fi

		# MAC

		mac=$(echo "${line:51:18}" | xargs)

		for i in "${whitelist[@]}"
		do
		  if [ "$i" == "$mac" ]
			then
				arrMac+=($mac)
				arrId+=($id)
				arrIp+=($ip)
			fi
		done

	fi
done < hosts.txt

printf '%s\n' "${arrId[@]}"
# printf '%s\n' "${arrIp[@]}"
# printf '%s\n' "${arrMac[@]}"
echo "000end"