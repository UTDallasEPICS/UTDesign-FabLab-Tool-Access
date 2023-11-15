const userData1 = {
    userID: "2020123654",
    IsAdmin: 1,
    machineID: "Test Bench",
    TimeUsedSeconds: 120
};
const userData2 = {
    userID: "202",
    IsAdmin: 0,
    machineID: "Test Bench",
    TimeUsedSeconds: 0
};

let array = [];
const fs = require('fs');

//const jsonUserData = JSON.stringify(userData1);
//const jsonUserData2 = JSON.stringify(userData2);

array.push(userData1);
array.push(userData2);

//fs.writeFileSync('userdata.json', JSON.stringify(array));
//fs.writeFileSync('userdata.json', JSON.stringify(array, null, 2));

//fs.writeFileSync('userdata.json', jsonUserData2);

//Read from file
jsonUserData = fs.readFileSync('userdata.json', 'utf8');
userData = JSON.parse(jsonUserData);
//console.log(userData);
//For loop to print out the userdata to console
for (let i = 0; i < userData.length; i++) {
    console.log(userData);
}

//Only write userID and Admin status from objects to new json file
let newUserData = [];
for (let i = 0; i < userData.length; i++) {
    newUserData.push({
        userID: userData[i].userID,
        IsAdmin: userData[i].IsAdmin
    });
}
//console.log(newUserData);
fs.writeFileSync('newuserdata.json', JSON.stringify(newUserData, null, 2));


