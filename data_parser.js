const fs = require("fs")
const { exit } = require("process")

const fileContent = fs.readFileSync("drawing_data_final.txt", {encoding: "utf-8"})

const result = []

for(x of fileContent.split(";\n")){
    try {
        result.push(JSON.parse(x))
    } catch (error) {
        
    }
    
}

console.log(JSON.stringify(result))