<template>
    <div class="page-background">
        <!-- Message Box -->
        <div v-if="message.visible" :class="['message-box', message.type]">
            {{ message.text }}
            <button @click="message.visible = false" class="close-btn">&times;</button>
        </div>

        <div class="container">
            <h1>Student Signup / Profile Info</h1>

            <form @submit.prevent="handleSubmit">
                
                <!-- FIRST + LAST NAME -->
                <label for="firstName">First Name</label>
                <input type="text" id="firstName" v-model="firstName" required />

                <label for="lastName">Last Name</label>
                <input type="text" id="lastName" v-model="lastName" required />

                <!-- EMAIL + PASSWORD -->
                <label for="email">Email</label>
                <input type="email" id="email" v-model="email" required />

                <label for="password">Password</label>
                <input type="password" id="password" v-model="password" required />

                <label for="confirmPassword">Confirm Password</label>
                <input type="password" id="confirmPassword" v-model="confirmPassword" required />

                <!-- PROFILE FIELDS -->
                <label for="birthday">Date of Birth</label>
                <input type="date" id="birthday" v-model="birthday" />

                <label>International Student</label>
                <div class="radio-group">
                    <label><input type="radio" value="yes" v-model="international" /> Yes</label>
                    <label><input type="radio" value="no" v-model="international" /> No</label>
                </div>

                <label for="semester">Current Semester</label>
                <select id="semester" v-model="semester">
                    <option disabled value="">Select semester</option>
                    <option v-for="n in 8" :key="n" :value="n">{{ n }}</option>
                </select>

                <label>Enrollment Type</label>
                <div class="radio-group">
                    <label><input type="radio" value="full-time" v-model="enrollment" /> Full-time</label>
                    <label><input type="radio" value="part-time" v-model="enrollment" /> Part-time</label>
                </div>

                <!-- COURSES -->
                <label>Taken Courses</label>
                <div class="chip-container">
                    <div v-for="course in courses" :key="course"
                        :class="['chip', { selected: selectedCourses.includes(course) }]"
                        @click="toggleCourse(course)">
                        {{ course }}
                    </div>
                </div>

                <label for="otherCourse">Other Course(s)</label>
                <input type="text" id="otherCourse" v-model="otherCourse" placeholder="Enter other course" />

                <!-- GENEDS -->
                <label>Taken GenEd Types</label>
                <div class="chip-container">
                    <div v-for="gened in geneds" :key="gened"
                        :class="['chip', { selected: selectedGeneds.includes(gened) }]"
                        @click="toggleGened(gened)">
                        {{ gened }}
                    </div>
                </div>

                <label for="otherGened">Other GenEd Type(s)</label>
                <input type="text" id="otherGened" v-model="otherGened" placeholder="Enter other GenEd" />

                <button type="submit" class="submit-btn">
                    {{ isLoading ? "Submitting..." : "Submit" }}
                </button>

                <p class="small-text">
                    Already have an account?
                    <a @click="$router.push('/login')">Log in</a>
                </p>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { supabase } from "../supabase";

const router = useRouter();
const isLoading = ref(false);

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const birthday = ref("");
const international = ref("");
const semester = ref("");
const enrollment = ref("");
const otherCourse = ref("");
const otherGened = ref("");

const courses = ref([
    "CIS 1001","SCTC 2001","CIS 1051","CIS 1057","CIS 1166","CIS 2033","CIS 2107",
    "CIS 2166","CIS 2168","CIS 3207","CIS 3223","CIS 3296","CIS 4398","CIS 4397",
    "CIS 3203","CIS 3211","CIS 3217","CIS 3219","CIS 3242","CIS 3308","CIS 3319",
    "CIS 3381","CIS 3441","CIS 3515","CIS 3605","CIS 3715","CIS 4282","CIS 4305",
    "CIS 4307","CIS 4308","CIS 4319","CIS 4324","CIS 4331","CIS 4345","CIS 4350",
    "CIS 4360","CIS 4382","CIS 4419","CIS 4515","CIS 4517","CIS 4523","CIS 4524",
    "CIS 4615","MATH 1041","MATH 1042","PHYS 1061","PHYS 1062",
]);

const geneds = ref(["GA","GB","GD","GG","GS","GU","GW","GQ","GY","GZ"]);
const selectedCourses = ref([]);
const selectedGeneds = ref([]);

const message = ref({ text: "", type: "", visible: false });

const showMessage = (text, type) => {
    message.value = { text, type, visible: true };
};

const toggleCourse = (course) => {
    const idx = selectedCourses.value.indexOf(course);
    idx === -1 ? selectedCourses.value.push(course) : selectedCourses.value.splice(idx, 1);
};

const toggleGened = (gened) => {
    const idx = selectedGeneds.value.indexOf(gened);
    idx === -1 ? selectedGeneds.value.push(gened) : selectedGeneds.value.splice(idx, 1);
};

const handleSubmit = async () => {
    isLoading.value = true;

    if (password.value !== confirmPassword.value) {
        showMessage("Passwords do not match.", "error");
        isLoading.value = false;
        return;
    }

    try {
        // 1️⃣ Create auth user
        const { data, error } = await supabase.auth.signUp({
            email: email.value,
            password: password.value,
        });

        if (error) throw error;

        const user = data.user;
        if (!user) throw new Error("Sign-up succeeded but user is null");

        const user_id = user.id; // UUID

        // 2️⃣ Prepare payload for backend
        const payload = {
            personal: {
                user_id,
                full_name: `${firstName.value} ${lastName.value}`,
                age: birthday.value ? calculateAge(birthday.value) : null,
                is_international: international.value === "yes",
            },
            academic: {
                user_id,
                current_semester: semester.value ? parseInt(semester.value) : 1,
                taken_courses: selectedCourses.value,
                taken_geneds: selectedGeneds.value,
            },
        };

        // 3️⃣ Save Personal + Academic info in your external DB
        const res = await fetch("https://supabase-kqbi.onrender.com/register-student", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!res.ok) {
            console.error(await res.text());
            throw new Error("Failed saving student data");
        }

        showMessage("Account created successfully! Check your email.", "success");
        setTimeout(() => router.push("/login"), 2000);

    } catch (err) {
        showMessage(err.message || "Signup failed.", "error");
    } finally {
        isLoading.value = false;
    }
};

// Helper to calculate age
function calculateAge(birth) {
    const today = new Date();
    const dob = new Date(birth);
    let age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) age--;
    return age;
}

</script>


<style scoped>
.page-background {
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(to bottom right, #a41e34, #ffffff);
    color: #333;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 40px 0;
    margin: 0;
    min-height: 100vh;
    width: 100%;
    position: relative;
}

.container {
    background-color: #fff;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    padding: 40px 50px;
    width: 100%;
    max-width: 550px;
    text-align: left;
    box-sizing: border-box;
}

h1 {
    text-align: center;
    color: #a41e34;
    margin-bottom: 25px;
    font-size: 28px;
}

label {
    display: block;
    margin-top: 14px;
    font-weight: 600;
}

input,
select {
    width: 100%;
    padding: 10px;
    margin-top: 4px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 14px;
    transition: border 0.2s ease-in-out;
    box-sizing: border-box;
}

input:focus,
select:focus {
    outline: none;
    border-color: #a41e34;
}

.radio-group {
    display: flex;
    align-items: center;
    gap: 20px;
    margin: 8px 0 10px 0;
}

.radio-group label {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 0;
    font-weight: normal;
}

.radio-group input[type="radio"] {
    width: auto;
    padding: 0;
    margin: 0;
    cursor: pointer;
}

.chip-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 10px 0 20px 0;
}

.chip {
    background: #f4f4f4;
    border: 1px solid #ccc;
    border-radius: 20px;
    padding: 6px 12px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    font-size: 14px;
}

.chip:hover {
    background-color: #ffe6e9;
}

.chip.selected {
    background-color: #a41e34;
    color: #fff;
    border-color: #a41e34;
}

.submit-btn {
    width: 100%;
    background-color: #a41e34;
    color: #fff;
    padding: 12px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    margin-top: 20px;
    transition: background 0.2s ease-in-out;
}

.submit-btn:hover {
    background-color: #8e162b;
}

.small-text {
    font-size: 13px;
    margin-top: 20px;
    text-align: center;
}

.small-text a {
    color: #a41e34;
    text-decoration: none;
    font-weight: 600;
    cursor: pointer;
}

.small-text a:hover {
    text-decoration: underline;
}

.message-box {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 15px 30px;
    border-radius: 8px;
    font-weight: 600;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-width: 300px;
}
.message-box.success {
    background-color: #e6ffed;
    color: #38a169;
    border: 1px solid #9ae6b4;
}
.message-box.error {
    background-color: #fff5f5;
    color: #e53e3e;
    border: 1px solid #feb2b2;
}
.close-btn {
    background: none;
    border: none;
    color: inherit;
    font-size: 18px;
    margin-left: 15px;
    cursor: pointer;
    line-height: 1;
}

.other-input label {
  font-size: 15px;        
  font-weight: 450;       
  color: #313030;          
  display: block;
  margin-top: 10px;
}


</style>
