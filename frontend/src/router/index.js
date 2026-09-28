import { createRouter, createWebHistory } from "vue-router";


// Login

import Login from "../views/Login.vue";


// Student

import StudentDashboard from "../views/student/StudentDashboard.vue";

import ApplyLeave from "../views/student/ApplyLeave.vue";


// Counselor

import CounselorDashboard from "../views/counselor/CounselorDashboard.vue";


// Admin

import AdminDashboard from "../views/admin/AdminDashboard.vue";




const routes = [



{
    path:"/",
    name:"Login",
    component:Login
},




{
    path:"/student",
    name:"StudentDashboard",
    component:StudentDashboard
},




{
    path:"/student/apply-leave",
    name:"ApplyLeave",
    component:ApplyLeave
},




{
    path:"/counselor",
    name:"CounselorDashboard",
    component:CounselorDashboard
},




{
    path:"/admin",
    name:"AdminDashboard",
    component:AdminDashboard
},
{
path:"/student/messages",
name:"StudentMessages",
component:{
template:"<h1>Messages Coming Soon</h1>"
}
},

{
    path: "/student/attendance",

    name: "StudentAttendanceCourses",

    component: () =>
        import(
            "../views/student/AttendanceCourses.vue"
        )
},

{
    path: "/student/attendance/:id",

    name: "StudentCourseAttendance",

    component: () =>
        import(
            "../views/student/CourseAttendance.vue"
        )
},



];





const router = createRouter({


history:createWebHistory(),


routes


});





export default router;