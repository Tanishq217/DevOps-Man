#!/bin/bash

echo "Hello World!"


echo "this is my first script" 



# Variables ! 

name="Tanishq" 


echo "$name"




echo "${name} Hello"



sumof2and3=$((2 + 3))
echo "$sumof2and3" 




a=4
b=3


echo $((a+b))
echo $((a*b))
echo $((a/b))
echo $((a-b)) 



# Conditional Statements # 



if [ "$a" -eq 4 ]; then 
   echo "Hi" 
else
   echo "Hello" 
fi 


