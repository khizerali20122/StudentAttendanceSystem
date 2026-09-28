<template>

<div class="courses-page">

    <Navbar />

    <main class="courses-container">

        <!-- Page Header -->

        <div class="page-header">

            <div>

                <p class="eyebrow">
                    ATTENDANCE
                </p>

                <h1>
                    My Courses
                </h1>

                <p class="subtitle">
                    Select a course to view your attendance details.
                </p>

            </div>

        </div>


        <!-- Loading -->

        <div
            v-if="loading"
            class="state-card"
        >

            <div class="loader"></div>

            <p>
                Loading your courses...
            </p>

        </div>


        <!-- Error -->

        <div
            v-else-if="error"
            class="state-card error-card"
        >

            <h3>
                Unable to load courses
            </h3>

            <p>
                {{ error }}
            </p>

            <button
                class="retry-button"
                @click="loadCourses"
            >
                Try Again
            </button>

        </div>


        <!-- Empty -->

        <div
            v-else-if="courses.length === 0"
            class="state-card"
        >

            <div class="empty-icon">
                📚
            </div>

            <h3>
                No courses available
            </h3>

            <p>
                No courses have been assigned to your class yet.
            </p>

        </div>


        <!-- Course List -->

        <div
            v-else
            class="courses-grid"
        >

            <button
                v-for="course in courses"
                :key="course.id"
                class="course-card"
                @click="openCourse(course.id)"
            >

                <div class="course-icon">
                    📚
                </div>


                <div class="course-content">

                    <p class="course-code">
                        {{ course.code || "COURSE" }}
                    </p>

                    <h2>
                        {{ course.name }}
                    </h2>

                    <p class="course-class">
                        {{ course.class_name }}
                    </p>

                </div>


                <div class="course-arrow">
                    →
                </div>

            </button>

        </div>


    </main>

</div>

</template>


<script>

import api from "../../api/axios";
import Navbar from "../../components/Navbar.vue";

export default {

    components: {
        Navbar
    },

    data() {

        return {

            courses: [],

            loading: true,

            error: ""

        };

    },

    async mounted() {

        await this.loadCourses();

    },

    methods: {

        async loadCourses() {

            this.loading = true;
            this.error = "";

            try {

                const response = await api.get(
                    "/attendance/student/courses/"
                );

                this.courses = Array.isArray(response.data)
                    ? response.data
                    : response.data.value || [];

            }

            catch (error) {

                console.error(
                    "Course loading error:",
                    error
                );

                this.error =
                    "We could not load your courses. Please try again.";

            }

            finally {

                this.loading = false;

            }

        },


        openCourse(courseId) {

            this.$router.push(
                `/student/attendance/${courseId}`
            );

        }

    }

};

</script>


<style scoped>

.courses-page {

    min-height: 100vh;

    background: #f8fafc;

}


.courses-container {

    max-width: 1200px;

    margin: 0 auto;

    padding: 45px 40px 60px;

}


.page-header {

    margin-bottom: 35px;

}


.eyebrow {

    margin: 0 0 8px;

    color: #2563eb;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 1.2px;

}


.page-header h1 {

    margin: 0;

    color: #0f172a;

    font-size: 34px;

    font-weight: 700;

    letter-spacing: -0.7px;

}


.subtitle {

    margin-top: 10px;

    color: #64748b;

    font-size: 15px;

}


.courses-grid {

    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 22px;

}


.course-card {

    position: relative;

    display: flex;

    align-items: flex-start;

    gap: 18px;

    width: 100%;

    min-height: 190px;

    padding: 26px;

    text-align: left;

    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 16px;

    box-shadow:
        0 4px 15px rgba(15, 23, 42, 0.05);

    cursor: pointer;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        border-color 0.2s ease;

}


.course-card:hover {

    transform: translateY(-3px);

    border-color: #bfdbfe;

    box-shadow:
        0 10px 25px rgba(15, 23, 42, 0.09);

}


.course-icon {

    width: 48px;

    height: 48px;

    flex-shrink: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #eff6ff;

    border-radius: 12px;

    font-size: 22px;

}


.course-content {

    flex: 1;

}


.course-code {

    margin: 0 0 8px;

    color: #2563eb;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 0.8px;

}


.course-card h2 {

    margin: 0;

    color: #0f172a;

    font-size: 19px;

    font-weight: 650;

    line-height: 1.35;

}


.course-class {

    margin: 12px 0 0;

    color: #64748b;

    font-size: 13px;

    line-height: 1.5;

}


.course-arrow {

    position: absolute;

    right: 22px;

    bottom: 20px;

    color: #2563eb;

    font-size: 22px;

    font-weight: 500;

}


.state-card {

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    min-height: 260px;

    padding: 35px;

    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 16px;

    text-align: center;

}


.state-card h3 {

    margin: 15px 0 5px;

    color: #0f172a;

}


.state-card p {

    color: #64748b;

}


.error-card {

    border-color: #fecaca;

}


.retry-button {

    margin-top: 15px;

    padding: 10px 18px;

    border: none;

    border-radius: 8px;

    background: #2563eb;

    color: white;

    font-weight: 600;

    cursor: pointer;

}


.empty-icon {

    font-size: 38px;

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


@media (max-width: 1000px) {

    .courses-grid {

        grid-template-columns:
            repeat(2, minmax(0, 1fr));

    }

}


@media (max-width: 650px) {

    .courses-container {

        padding: 30px 20px;

    }


    .courses-grid {

        grid-template-columns: 1fr;

    }


    .page-header h1 {

        font-size: 28px;

    }

}

</style>