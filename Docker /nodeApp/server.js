const express = require("express");

const app = express() ; 

app.get("/" , (req ,res) => {
    res.send("Hello, i am first node app"); 
}) ; 


app.listen(3000 , "0.0.0.0" , () => {
    console.log("Server is running on post 3000") ; 
}) ; 



