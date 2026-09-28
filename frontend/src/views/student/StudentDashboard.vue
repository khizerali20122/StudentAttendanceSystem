<template>

<div class="student-page">


    <Navbar />



    <main class="dashboard-container">


        <!-- Welcome Section -->

        <section class="welcome-section">

            <h1>
                Welcome back, {{ username }}
            </h1>

            <p>
                Computer Science Batch 2026
            </p>

        </section>





        <!-- Statistics Cards -->

        <section class="stats-grid">


            <div
    class="stat-card clickable"
    @click="$router.push('/student/attendance')"
>


                <div class="icon">
                    📊
                </div>


                <h3>
                    Attendance
                </h3>


                <h2>
                    {{ attendance?.attendance_percentage ?? 0 }}%
                </h2>


                <p>
                    Overall Attendance
                </p>


            </div>






            <div class="stat-card">


                <div class="icon">
                    📚
                </div>


                <h3>
                    Classes
                </h3>


                <h2>
                    {{ attendance?.total_classes ?? 0 }}
                </h2>


                <p>
                    Total Classes
                </p>


            </div>







            <div class="stat-card">


                <div class="icon">
                    📝
                </div>


                <h3>
                    Leave Requests
                </h3>


                <h2>
                    {{ leaves.length }}
                </h2>


                <p>
                    Total Requests
                </p>


            </div>



        </section>






        <!-- Attendance -->

        <section class="dashboard-section">


            <div class="section-header">

                <h2>
                    Recent Attendance
                </h2>


            </div>




            <div
            class="record-card"

            v-for="record in attendance?.records"

            :key="record.id"
            >



                <div>


                    <h3>
                        {{ record.task_title }}
                    </h3>


                    <p>
                        {{ formatDate(record.check_in_time) }}
                    </p>


                </div>



                <span
                class="status present"
                >

                    Present

                </span>



            </div>



        </section>







        <!-- Leaves -->


        <section class="dashboard-section">


            <div class="section-header">


                <h2>
                    Leave History
                </h2>


                <button
                class="primary-btn"

                @click="$router.push('/student/apply-leave')"
                >

                    + Apply Leave

                </button>


            </div>





            <div

            v-for="leave in leaves"

            :key="leave.id"

            class="record-card"

            >



                <div>


                    <h3>
                        {{ leave.reason }}
                    </h3>


                    <p>

                    {{leave.start_date}}

                    -

                    {{leave.end_date}}

                    </p>


                </div>






                <span

                class="status"

                :class="leave.status"

                >

                    {{ leave.status }}

                </span>





                <button

                v-if="leave.status==='pending'"

                class="cancel-btn"

                @click="cancelLeave(leave.id)"

                >

                    Cancel

                </button>




            </div>



        </section>





    </main>


</div>

</template>






<script>


import api from "../../api/axios";

import Navbar from "../../components/Navbar.vue";

import "../../assets/dashboard.css";



export default{


components:{


Navbar


},




data(){


return {


username:
localStorage.getItem("username"),


attendance:null,


leaves:[]


}


},




async mounted(){


await this.loadAttendance();

await this.loadLeaves();


},





methods:{



async loadAttendance(){


const response =
await api.get(

"/attendance/my-report/"

);


this.attendance =
response.data;


},




async loadLeaves(){


const response =
await api.get(

"/leaves/my-leaves/"

);



this.leaves =
Array.isArray(response.data)

?
response.data

:
[response.data];



},




async cancelLeave(id){


await api.delete(

`/leaves/cancel/${id}/`

);


await this.loadLeaves();


},




formatDate(date){


return new Date(date)

.toLocaleDateString();


}




}



}



</script>