<template>

<nav class="navbar">


    <!-- Brand -->

    <div class="brand">

        🎓 Student Attendance System

    </div>



    <!-- Navigation -->

    <div class="nav-links">


        <button
        @click="$router.push('/student')"
        >

            Dashboard

        </button>



        <button
        @click="$router.push('/student/messages')"
        >

            Messages

        </button>



        <button
        @click="$router.push('/student/apply-leave')"
        >

            Apply Leave

        </button>



        <button
        class="logout"
        @click="logout"
        >

            Logout

        </button>


    </div>


</nav>


</template>




<script>


export default {


methods:{



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



this.$router.push("/");


}



}



}


</script>





<style scoped>


.navbar{


height:70px;

background:#1e3a8a;

display:flex;

align-items:center;

justify-content:space-between;

padding:0 40px;

color:white;

box-shadow:
0 2px 8px rgba(0,0,0,0.15);


}



.brand{


font-size:22px;

font-weight:700;


}



.nav-links{


display:flex;

gap:15px;


}



.nav-links button{


background:white;

color:#1e3a8a;

border:none;

padding:10px 18px;

border-radius:8px;

font-weight:600;

cursor:pointer;


}



.nav-links button:hover{


background:#dbeafe;


}



.nav-links .logout{


background:#dc2626;

color:white;


}



.nav-links .logout:hover{


background:#b91c1c;


}



</style>