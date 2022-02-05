const express = require ("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose")
const _ = require("lodash");
const app = express()

app.set("view engine", "ejs");

app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static("public"));

mongoose.connect("mongodb+srv://uofthacks123:spiderman123@cluster0.whjm8.mongodb.net/myFirstDatabase?retryWrites=true&w=majority");