<template>

<div class="login-page">


    <!-- Logout button -->

    <div
    v-if="isLoggedIn"
    class="logout-container"
    >

        <button
        @click="logout"
        >

            Logout

        </button>

    </div>



    <h1>
        Student Attendance System
    </h1>



    <div class="login-box">


        <input
        v-model="username"
        type="text"
        placeholder="Username"
        />


        <br><br>



        <input
        v-model="password"
        type="password"
        placeholder="Password"
        />


        <br><br>



        <button
        @click="login"
        >

            Login

        </button>



        <p v-if="message">

            {{ message }}

        </p>



    </div>


</div>


</template>





<script>


import api from "../api/axios";



export default {



data(){


return {


username:"",

password:"",

message:"",

isLoggedIn:
!!localStorage.getItem("access")


}


},





methods:{



async login(){


try{


const response =
await api.post(

"/token/",

{

username:this.username,

password:this.password

}

);





// Save JWT tokens


localStorage.setItem(

"access",

response.data.access

);



localStorage.setItem(

"refresh",

response.data.refresh

);



localStorage.setItem(

"username",

this.username

);




// Get user role from username

let role = "";



if(
this.username.includes("student")
){

role="student";

}

else if(
this.username.includes("counselor")
){

role="counselor";

}

else if(
this.username === "admin"
){

role="admin";

}




localStorage.setItem(
"role",
role
);




this.isLoggedIn = true;



this.message =
"Login successful";




// Redirect


if(role==="student"){


this.$router.push(
"/student"
);


}


else if(role==="counselor"){


this.$router.push(
"/counselor"
);


}


else if(role==="admin"){


this.$router.push(
"/admin"
);


}


else{


this.message =
"Unknown role";


}



}



catch(error){


console.log(
"Login Error:",
error
);



this.message =
"Invalid username or password";


}



},






logout(){


localStorage.removeItem(
"access"
);


localStorage.removeItem(
"refresh"
);


localStorage.removeItem(
"username"
);


localStorage.removeItem(
"role"
);



this.isLoggedIn=false;



this.username="";

this.password="";



this.$router.push("/");



}




}



}



</script>





<style scoped>


.login-page{

padding:40px;

}



.logout-container{

position:absolute;

top:20px;

right:30px;

}



.logout-container button{


background:#dc3545;

color:white;

border:none;

padding:10px 20px;

border-radius:5px;

cursor:pointer;


}



.login-box{

margin-top:40px;

}



input{

padding:10px;

width:250px;

}



button{


padding:10px 20px;

cursor:pointer;


}



</style>