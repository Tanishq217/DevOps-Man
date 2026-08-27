#!/bin/bash

read -p "Enter marks: " marks

if [ "$marks" -ge 90 ]; then
   echo "A" 
elif [ "$marks" -ge 50 ]; then 
   echo "B" 
else 
   echo "Need Improvenent" 
fi 




# LOOPS 



for i in {1..5}; do 
	echo "$i" 
done 
 



# Function ! 



printMyName(){
	echo "hey i am tanishq" 
}



printMyName




# taking Arguments! 


echo "First Argu: $1"
echo "Second Argu: $2" 








