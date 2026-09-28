<template>
    <div class="attendance-page">

        <Navbar />

        <main class="attendance-container">

            <!-- Back Button -->

            <button
                class="back-button"
                @click="$router.push('/student/attendance')"
            >
                ← Back to My Courses
            </button>


            <!-- Loading -->

            <div
                v-if="loading"
                class="state-card"
            >
                <div class="loader"></div>

                <p>
                    Loading attendance...
                </p>
            </div>


            <!-- Error -->

            <div
                v-else-if="error"
                class="state-card error-card"
            >
                <div class="error-icon">
                    ⚠
                </div>

                <h2>
                    Unable to load attendance
                </h2>

                <p>
                    {{ error }}
                </p>

                <button
                    class="retry-button"
                    @click="loadAttendance"
                >
                    Try Again
                </button>
            </div>


            <!-- Attendance -->

            <template v-else>

                <!-- Course Header -->

                <section class="course-header">

                    <div class="course-icon-large">
                        📚
                    </div>

                    <div>

                        <p class="eyebrow">
                            COURSE ATTENDANCE
                        </p>

                        <h1>
                            {{ course.name }}
                        </h1>

                        <p class="course-code">
                            {{ course.code }}
                        </p>

                    </div>

                </section>


                <!-- Summary Cards -->

                <section class="summary-grid">

                    <!-- Attendance Percentage -->

                    <div class="summary-card">

                        <div class="summary-icon">
                            📊
                        </div>

                        <div>

                            <p class="summary-label">
                                Attendance
                            </p>

                            <h2>
                                {{ attendancePercentage }}%
                            </h2>

                        </div>

                    </div>


                    <!-- Total Classes -->

                    <div class="summary-card">

                        <div class="summary-icon">
                            📚
                        </div>

                        <div>

                            <p class="summary-label">
                                Total Classes
                            </p>

                            <h2>
                                {{ totalClasses }}
                            </h2>

                        </div>

                    </div>


                    <!-- Present -->

                    <div class="summary-card">

                        <div class="summary-icon">
                            ✓
                        </div>

                        <div>

                            <p class="summary-label">
                                Present
                            </p>

                            <h2>
                                {{ present }}
                            </h2>

                        </div>

                    </div>


                    <!-- Absent -->

                    <div class="summary-card">

                        <div class="summary-icon">
                            !
                        </div>

                        <div>

                            <p class="summary-label">
                                Absent
                            </p>

                            <h2>
                                {{ absent }}
                            </h2>

                        </div>

                    </div>

                </section>


                <!-- Attendance Progress -->

                <section class="progress-card">

                    <div class="progress-header">

                        <div>

                            <h2>
                                Attendance Overview
                            </h2>

                            <p>
                                Your attendance percentage for this course
                            </p>

                        </div>

                        <strong>
                            {{ attendancePercentage }}%
                        </strong>

                    </div>


                    <div class="progress-track">

                        <div
                            class="progress-fill"
                            :style="{
                                width: attendancePercentage + '%'
                            }"
                        ></div>

                    </div>

                </section>


                <!-- Attendance Records -->

                <section class="records-section">

                    <div class="section-header">

                        <div>

                            <p class="eyebrow">
                                ATTENDANCE HISTORY
                            </p>

                            <h2>
                                Class Records
                            </h2>

                        </div>

                        <span class="record-count">
                            {{ records.length }} records
                        </span>

                    </div>


                    <!-- No records -->

                    <div
                        v-if="records.length === 0"
                        class="empty-records"
                    >

                        <div>
                            📋
                        </div>

                        <h3>
                            No attendance records
                        </h3>

                        <p>
                            There are no attendance records for this course yet.
                        </p>

                    </div>


                    <!-- Records -->

                    <div
                        v-else
                        class="records-table-wrapper"
                    >

                        <table class="records-table">

                            <thead>

                                <tr>

                                    <th>
                                        Date
                                    </th>

                                    <th>
                                        Day
                                    </th>

                                    <th>
                                        Class
                                    </th>

                                    <th>
                                        Status
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                <tr
                                    v-for="record in records"
                                    :key="record.id"
                                >

                                    <td>

                                        <span class="date-main">
                                            {{ formatDate(record.date) }}
                                        </span>

                                    </td>


                                    <td>
                                        {{ getDay(record.date) }}
                                    </td>


                                    <td>

                                        <span class="class-title">
                                            {{ record.task_title }}
                                        </span>

                                    </td>


                                    <td>

                                        <span
                                            class="status-badge"
                                            :class="getStatusClass(record.status)"
                                        >

                                            <span class="status-dot"></span>

                                            {{ formatStatus(record.status) }}

                                        </span>

                                    </td>

                                </tr>

                            </tbody>

                        </table>

                    </div>

                </section>

            </template>

        </main>

    </div>
</template>


<script>

import api from "../../api/axios";
import Navbar from "../../components/Navbar.vue";


export default {

    name: "CourseAttendance",


    components: {
        Navbar
    },


    data() {

        return {

            loading: true,

            error: "",

            course: {
                id: null,
                name: "",
                code: ""
            },

            totalClasses: 0,

            present: 0,

            absent: 0,

            attendancePercentage: 0,

            records: []

        };

    },


    mounted() {

        this.loadAttendance();

    },


    methods: {

        async loadAttendance() {

            this.loading = true;

            this.error = "";


            try {

                const courseId =
                    this.$route.params.id;


                const response = await api.get(
                    `/attendance/student/courses/${courseId}/attendance/`
                );


                const data = response.data;


                this.course =
                    data.course || {
                        id: courseId,
                        name: "Course",
                        code: ""
                    };


                this.totalClasses =
                    data.total_classes || 0;


                this.present =
                    data.present || 0;


                this.absent =
                    data.absent || 0;


                this.attendancePercentage =
                    data.attendance_percentage || 0;


                this.records =
                    Array.isArray(data.records)
                        ? data.records
                        : [];

            }


            catch (error) {

                console.error(
                    "Attendance loading error:",
                    error
                );


                if (
                    error.response &&
                    error.response.status === 404
                ) {

                    this.error =
                        "This course could not be found or you do not have access to it.";

                }

                else if (
                    error.response &&
                    error.response.status === 401
                ) {

                    this.error =
                        "Your session has expired. Please log in again.";

                }

                else {

                    this.error =
                        "We could not load the attendance information. Please try again.";

                }

            }


            finally {

                this.loading = false;

            }

        },


        formatDate(date) {

            if (!date) {
                return "-";
            }


            const parts =
                date.split("-");


            if (parts.length !== 3) {
                return date;
            }


            const year =
                parts[0];

            const month =
                parts[1];

            const day =
                parts[2];


            const months = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec"
            ];


            const monthName =
                months[
                    parseInt(month, 10) - 1
                ];


            return `${day} ${monthName} ${year}`;

        },


        getDay(date) {

            if (!date) {
                return "-";
            }


            const dateObject =
                new Date(`${date}T00:00:00`);


            return dateObject.toLocaleDateString(
                "en-US",
                {
                    weekday: "long"
                }
            );

        },


        formatStatus(status) {

            if (!status) {
                return "Unknown";
            }


            return status
                .charAt(0)
                .toUpperCase()
                + status.slice(1);

        },


        getStatusClass(status) {

            if (status === "present") {
                return "status-present";
            }


            if (status === "absent") {
                return "status-absent";
            }


            return "status-other";

        }

    }

};

</script>


<style scoped>

.attendance-page {

    min-height: 100vh;

    background: #f8fafc;

}


.attendance-container {

    max-width: 1200px;

    margin: 0 auto;

    padding: 35px 40px 60px;

}


/* Back Button */

.back-button {

    display: inline-flex;

    align-items: center;

    gap: 8px;

    margin-bottom: 28px;

    padding: 9px 14px;

    border: none;

    background: transparent;

    color: #2563eb;

    font-size: 14px;

    font-weight: 600;

    cursor: pointer;

}


.back-button:hover {

    color: #1d4ed8;

}


/* Course Header */

.course-header {

    display: flex;

    align-items: center;

    gap: 20px;

    margin-bottom: 30px;

}


.course-icon-large {

    width: 64px;

    height: 64px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #eff6ff;

    border-radius: 16px;

    font-size: 30px;

}


.eyebrow {

    margin: 0 0 7px;

    color: #2563eb;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1.1px;

}


.course-header h1 {

    margin: 0;

    color: #0f172a;

    font-size: 32px;

    font-weight: 700;

    letter-spacing: -0.5px;

}


.course-code {

    margin: 7px 0 0;

    color: #64748b;

    font-size: 14px;

    font-weight: 600;

}


/* Summary */

.summary-grid {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 18px;

    margin-bottom: 22px;

}


.summary-card {

    display: flex;

    align-items: center;

    gap: 15px;

    padding: 22px;

    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 14px;

    box-shadow:
        0 4px 15px rgba(15, 23, 42, 0.04);

}


.summary-icon {

    width: 42px;

    height: 42px;

    display: flex;

    align-items: center;

    justify-content: center;

    flex-shrink: 0;

    background: #eff6ff;

    border-radius: 11px;

    color: #2563eb;

    font-size: 18px;

    font-weight: 700;

}


.summary-label {

    margin: 0 0 5px;

    color: #64748b;

    font-size: 13px;

}


.summary-card h2 {

    margin: 0;

    color: #0f172a;

    font-size: 24px;

    font-weight: 700;

}


/* Progress */

.progress-card {

    margin-bottom: 30px;

    padding: 25px;

    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 14px;

}


.progress-header {

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 20px;

    margin-bottom: 18px;

}


.progress-header h2 {

    margin: 0 0 5px;

    color: #0f172a;

    font-size: 18px;

}


.progress-header p {

    margin: 0;

    color: #64748b;

    font-size: 13px;

}


.progress-header strong {

    color: #2563eb;

    font-size: 24px;

}


.progress-track {

    width: 100%;

    height: 10px;

    overflow: hidden;

    background: #e2e8f0;

    border-radius: 20px;

}


.progress-fill {

    height: 100%;

    background: #2563eb;

    border-radius: 20px;

    transition: width 0.5s ease;

}


/* Records */

.records-section {

    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 14px;

    overflow: hidden;

}


.section-header {

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 25px;

    border-bottom: 1px solid #e2e8f0;

}


.section-header h2 {

    margin: 0;

    color: #0f172a;

    font-size: 21px;

}


.record-count {

    padding: 6px 10px;

    background: #f1f5f9;

    border-radius: 7px;

    color: #64748b;

    font-size: 12px;

    font-weight: 600;

}


/* Table */

.records-table-wrapper {

    overflow-x: auto;

}


.records-table {

    width: 100%;

    border-collapse: collapse;

}


.records-table th {

    padding: 15px 25px;

    background: #f8fafc;

    color: #64748b;

    font-size: 12px;

    font-weight: 700;

    text-align: left;

    text-transform: uppercase;

    letter-spacing: 0.5px;

}


.records-table td {

    padding: 18px 25px;

    border-top: 1px solid #f1f5f9;

    color: #475569;

    font-size: 14px;

}


.records-table tbody tr {

    transition: background 0.15s ease;

}


.records-table tbody tr:hover {

    background: #f8fafc;

}


.date-main {

    color: #0f172a;

    font-weight: 600;

}


.class-title {

    color: #334155;

    font-weight: 500;

}


/* Status */

.status-badge {

    display: inline-flex;

    align-items: center;

    gap: 7px;

    padding: 6px 10px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 700;

}


.status-dot {

    width: 7px;

    height: 7px;

    border-radius: 50%;

}


.status-present {

    background: #ecfdf5;

    color: #047857;

}


.status-present .status-dot {

    background: #10b981;

}


.status-absent {

    background: #fef2f2;

    color: #b91c1c;

}


.status-absent .status-dot {

    background: #ef4444;

}


.status-other {

    background: #f1f5f9;

    color: #475569;

}


.status-other .status-dot {

    background: #64748b;

}


/* Empty */

.empty-records {

    padding: 60px 25px;

    text-align: center;

}


.empty-records > div {

    font-size: 35px;

}


.empty-records h3 {

    margin: 15px 0 7px;

    color: #0f172a;

}


.empty-records p {

    margin: 0;

    color: #64748b;

    font-size: 14px;

}


/* Loading/Error */

.state-card {

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    min-height: 350px;

    padding: 40px;

    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 16px;

    text-align: center;

}


.state-card p {

    color: #64748b;

}


.error-icon {

    font-size: 35px;

}


.error-card h2 {

    color: #0f172a;

}


.retry-button {

    margin-top: 10px;

    padding: 10px 18px;

    border: none;

    border-radius: 8px;

    background: #2563eb;

    color: #ffffff;

    font-weight: 600;

    cursor: pointer;

}


.loader {

    width: 32px;

    height: 32px;

    border: 3px solid #dbeafe;

    border-top-color: #2563eb;

    border-radius: 50%;

    animation: spin 0.8s linear infinite;

}


@keyframes spin {

    to {
        transform: rotate(360deg);
    }

}


/* Responsive */

@media (max-width: 900px) {

    .summary-grid {

        grid-template-columns:
            repeat(2, minmax(0, 1fr));

    }

}


@media (max-width: 600px) {

    .attendance-container {

        padding: 25px 18px 40px;

    }


    .summary-grid {

        grid-template-columns: 1fr;

    }


    .course-header h1 {

        font-size: 26px;

    }


    .records-table th,
    .records-table td {

        padding: 14px 15px;

    }

}

</style>