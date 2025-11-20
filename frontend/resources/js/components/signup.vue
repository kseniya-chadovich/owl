<template>
    <div
        class="min-h-screen bg-gradient-to-b from-[#800020] to-[#880808] text-white flex flex-col"
    >
        <!-- NAVBAR -->
        <header
            class="w-full border-b border-white/10 bg-black/10 backdrop-blur-sm"
        >
            <div
                class="flex justify-between items-center max-w-6xl mx-auto px-6 py-4"
            >
                <h1 class="text-xl font-semibold tracking-tight">
                    AI Scheduler
                </h1>

                <div class="flex items-center space-x-3">
                    <button
                        @click="$router.push('/')"
                        class="hidden sm:inline-flex border border-white/70 text-white font-medium px-3 py-1.5 rounded-lg text-sm hover:bg-white/10 transition"
                    >
                        ← Home
                    </button>

                    <button
                        @click="$router.push('/login')"
                        class="border border-white/80 bg-transparent text-white font-medium px-4 py-1.5 rounded-lg text-sm hover:bg-white hover:text-[#800020] transition"
                    >
                        Login
                    </button>
                </div>
            </div>
        </header>

        <!-- MAIN -->
        <main class="flex-1 flex items-start justify-center px-4 py-10">
            <div class="relative w-full max-w-4xl">
                <!-- Glow effect -->
                <div
                    class="pointer-events-none absolute -inset-6 rounded-3xl bg-gradient-to-br from-white/40 via-white/5 to-transparent blur-2xl opacity-70"
                ></div>

                <!-- MESSAGE BOX -->
                <transition name="fade-msg">
                    <div
                        v-if="message.visible"
                        :class="[
                            'mb-4 flex items-center justify-between text-sm px-4 py-3 rounded-lg border shadow-md relative z-20 bg-white',
                            message.type === 'success'
                                ? 'border-emerald-500 text-emerald-700'
                                : 'border-red-500 text-red-700',
                        ]"
                    >
                        <span>{{ message.text }}</span>
                        <button
                            @click="message.visible = false"
                            class="ml-4 text-lg leading-none hover:scale-110 transition-transform"
                        >
                            &times;
                        </button>
                    </div>
                </transition>

                <!-- SIGNUP CARD -->
                <div
                    :class="[
                        'relative z-10 bg-white/95 text-black backdrop-blur-xl rounded-2xl border border-white/40 px-8 py-10 shadow-xl',
                        'transform-gpu transition-all duration-700',
                        showCard ? 'card-in' : 'card-init',
                    ]"
                >
                    <h1 class="text-2xl font-bold mb-2 text-center">
                        Student Signup / Profile Info
                    </h1>
                    <p class="text-sm text-neutral-700 mb-6 text-center">
                        Create your account and tell us a bit about your
                        academic background.
                    </p>

                    <form @submit.prevent="handleSubmit" class="space-y-6">
                        <!-- BASIC INFO -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label
                                    for="firstName"
                                    class="block text-sm font-semibold text-neutral-800 mb-1"
                                >
                                    First Name
                                </label>
                                <input
                                    type="text"
                                    id="firstName"
                                    v-model="firstName"
                                    required
                                    class="w-full px-3 py-2 rounded-lg border border-neutral-300 text-sm focus:outline-none focus:ring-2 focus:ring-[#800020]"
                                />
                            </div>

                            <div>
                                <label
                                    for="lastName"
                                    class="block text-sm font-semibold text-neutral-800 mb-1"
                                >
                                    Last Name
                                </label>
                                <input
                                    type="text"
                                    id="lastName"
                                    v-model="lastName"
                                    required
                                    class="w-full px-3 py-2 rounded-lg border border-neutral-300 text-sm focus:outline-none focus:ring-2 focus:ring-[#800020]"
                                />
                            </div>
                        </div>

                        <!-- EMAIL + PASSWORD -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label
                                    for="email"
                                    class="block text-sm font-semibold text-neutral-800 mb-1"
                                >
                                    Email
                                </label>
                                <input
                                    type="email"
                                    id="email"
                                    v-model="email"
                                    required
                                    class="w-full px-3 py-2 rounded-lg border border-neutral-300 text-sm focus:outline-none focus:ring-2 focus:ring-[#800020]"
                                />
                            </div>

                            <div>
                                <label
                                    for="birthday"
                                    class="block text-sm font-semibold text-neutral-800 mb-1"
                                >
                                    Date of Birth
                                </label>
                                <input
                                    type="date"
                                    id="birthday"
                                    v-model="birthday"
                                    class="w-full px-3 py-2 rounded-lg border border-neutral-300 text-sm focus:outline-none focus:ring-2 focus:ring-[#800020]"
                                />
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label
                                    for="password"
                                    class="block text-sm font-semibold text-neutral-800 mb-1"
                                >
                                    Password
                                </label>
                                <input
                                    type="password"
                                    id="password"
                                    v-model="password"
                                    required
                                    class="w-full px-3 py-2 rounded-lg border border-neutral-300 text-sm focus:outline-none focus:ring-2 focus:ring-[#800020]"
                                />
                            </div>

                            <div>
                                <label
                                    for="confirmPassword"
                                    class="block text-sm font-semibold text-neutral-800 mb-1"
                                >
                                    Confirm Password
                                </label>
                                <input
                                    type="password"
                                    id="confirmPassword"
                                    v-model="confirmPassword"
                                    required
                                    class="w-full px-3 py-2 rounded-lg border border-neutral-300 text-sm focus:outline-none focus:ring-2 focus:ring-[#800020]"
                                />
                            </div>
                        </div>

                        <!-- INTERNATIONAL + ENROLLMENT + SEMESTER -->
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                                <p
                                    class="text-sm font-semibold text-neutral-800 mb-1"
                                >
                                    International Student
                                </p>
                                <div
                                    class="flex items-center gap-4 text-sm text-neutral-800"
                                >
                                    <label
                                        class="inline-flex items-center gap-1"
                                    >
                                        <input
                                            type="radio"
                                            value="yes"
                                            v-model="international"
                                            class="h-4 w-4"
                                        />
                                        <span>Yes</span>
                                    </label>
                                    <label
                                        class="inline-flex items-center gap-1"
                                    >
                                        <input
                                            type="radio"
                                            value="no"
                                            v-model="international"
                                            class="h-4 w-4"
                                        />
                                        <span>No</span>
                                    </label>
                                </div>
                            </div>

                            <div>
                                <label
                                    for="semester"
                                    class="block text-sm font-semibold text-neutral-800 mb-1"
                                >
                                    Current Semester
                                </label>
                                <select
                                    id="semester"
                                    v-model="semester"
                                    class="w-full px-3 py-2 rounded-lg border border-neutral-300 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#800020]"
                                >
                                    <option disabled value="">
                                        Select semester
                                    </option>
                                    <option v-for="n in 8" :key="n" :value="n">
                                        {{ n }}
                                    </option>
                                </select>
                            </div>

                            <div>
                                <p
                                    class="text-sm font-semibold text-neutral-800 mb-1"
                                >
                                    Enrollment Type
                                </p>
                                <div
                                    class="flex items-center gap-4 text-sm text-neutral-800"
                                >
                                    <label
                                        class="inline-flex items-center gap-1"
                                    >
                                        <input
                                            type="radio"
                                            value="full-time"
                                            v-model="enrollment"
                                            class="h-4 w-4"
                                        />
                                        <span>Full-time</span>
                                    </label>
                                    <label
                                        class="inline-flex items-center gap-1"
                                    >
                                        <input
                                            type="radio"
                                            value="part-time"
                                            v-model="enrollment"
                                            class="h-4 w-4"
                                        />
                                        <span>Part-time</span>
                                    </label>
                                </div>
                            </div>
                        </div>

                        <!-- COURSES -->
                        <div>
                            <label
                                class="block text-sm font-semibold text-neutral-800 mb-1"
                            >
                                Taken Courses
                            </label>
                            <p class="text-xs text-neutral-500 mb-2">
                                Tap to select all CIS / Math / Physics courses
                                you have already taken.
                            </p>
                            <div class="chip-container">
                                <div
                                    v-for="course in courses"
                                    :key="course"
                                    :class="[
                                        'chip',
                                        {
                                            selected:
                                                selectedCourses.includes(
                                                    course
                                                ),
                                        },
                                    ]"
                                    @click="toggleCourse(course)"
                                >
                                    {{ course }}
                                </div>
                            </div>

                            <label
                                for="otherCourse"
                                class="block text-sm font-semibold text-neutral-800 mb-1 mt-3"
                            >
                                Other Course(s)
                            </label>
                            <input
                                type="text"
                                id="otherCourse"
                                v-model="otherCourse"
                                placeholder="Enter any additional courses (comma separated)"
                                class="w-full px-3 py-2 rounded-lg border border-neutral-300 text-sm focus:outline-none focus:ring-2 focus:ring-[#800020]"
                            />
                        </div>

                        <!-- GENEDS -->
                        <div>
                            <label
                                class="block text-sm font-semibold text-neutral-800 mb-1"
                            >
                                Taken GenEd Types
                            </label>
                            <p class="text-xs text-neutral-500 mb-2">
                                GS will be auto-added for CS majors. GG is
                                required for international students.
                            </p>
                            <div class="chip-container">
                                <div
                                    v-for="gened in geneds"
                                    :key="gened"
                                    :class="[
                                        'chip',
                                        {
                                            selected:
                                                selectedGeneds.includes(gened),
                                        },
                                        gened === 'GS' ||
                                        (gened === 'GG' &&
                                            international === 'yes')
                                            ? 'disabled'
                                            : '',
                                    ]"
                                    @click="
                                        gened !== 'GS' &&
                                            !(
                                                gened === 'GG' &&
                                                international === 'yes'
                                            ) &&
                                            toggleGened(gened)
                                    "
                                >
                                    {{ gened }}
                                </div>
                            </div>

                            <label
                                for="otherGened"
                                class="block text-sm font-semibold text-neutral-800 mb-1 mt-3"
                            >
                                Other GenEd Type(s)
                            </label>
                            <input
                                type="text"
                                id="otherGened"
                                v-model="otherGened"
                                placeholder="Enter other GenEd types (comma separated)"
                                class="w-full px-3 py-2 rounded-lg border border-neutral-300 text-sm focus:outline-none focus:ring-2 focus:ring-[#800020]"
                            />
                        </div>

                        <!-- SUBMIT -->
                        <div>
                            <button
                                type="submit"
                                class="w-full bg-[#880808] text-white font-semibold text-base py-2.5 rounded-lg shadow-md hover:shadow-lg hover:-translate-y-0.5 transition disabled:opacity-60"
                                :disabled="isLoading"
                            >
                                {{ isLoading ? "Submitting..." : "Submit" }}
                            </button>

                            <p
                                class="text-sm text-center text-neutral-800 mt-3"
                            >
                                Already have an account?
                                <button
                                    type="button"
                                    @click="$router.push('/login')"
                                    class="font-medium text-[#800020] hover:text-[#550014] underline transition"
                                >
                                    Log in
                                </button>
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { supabase } from "../supabase";

const router = useRouter();
const isLoading = ref(false);
const showCard = ref(false);

const DATA_API_URL =
    import.meta.env.VITE_DATA_API_URL || "https://supabase-kqbi.onrender.com";

// form fields
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

// chips
const courses = ref([
    "CIS 1001",
    "SCTC 2001",
    "CIS 1051",
    "CIS 1057",
    "CIS 1068",
    "CIS 1166",
    "CIS 2033",
    "CIS 2107",
    "CIS 2166",
    "CIS 2168",
    "CIS 3207",
    "CIS 3223",
    "CIS 3296",
    "CIS 4398",
    "CIS 4397",
    "CIS 3203",
    "CIS 3211",
    "CIS 3217",
    "CIS 3219",
    "CIS 3242",
    "CIS 3308",
    "CIS 3319",
    "CIS 3381",
    "CIS 3441",
    "CIS 3515",
    "CIS 3605",
    "CIS 3715",
    "CIS 4282",
    "CIS 4305",
    "CIS 4307",
    "CIS 4308",
    "CIS 4319",
    "CIS 4324",
    "CIS 4331",
    "CIS 4345",
    "CIS 4350",
    "CIS 4360",
    "CIS 4382",
    "CIS 4419",
    "CIS 4515",
    "CIS 4517",
    "CIS 4523",
    "CIS 4524",
    "CIS 4615",
    "MATH 1021",
    "MATH 1041",
    "MATH 1042",
    "PHYS 1061",
    "PHYS 1062",
]);

const geneds = ref([
    "GA",
    "GB",
    "GD",
    "GG",
    "GS",
    "GU",
    "GW",
    "GQ",
    "GY",
    "GZ",
]);

const selectedCourses = ref([]);
const selectedGeneds = ref([]);

// message state
const message = ref({
    text: "",
    type: "",
    visible: false,
});

const showMessage = (text, type) => {
    message.value.text = text;
    message.value.type = type;
    message.value.visible = true;
};

const toggleCourse = (course) => {
    const i = selectedCourses.value.indexOf(course);
    if (i === -1) selectedCourses.value.push(course);
    else selectedCourses.value.splice(i, 1);
};

const toggleGened = (gened) => {
    const i = selectedGeneds.value.indexOf(gened);
    if (i === -1) selectedGeneds.value.push(gened);
    else selectedGeneds.value.splice(i, 1);
};

const parseCommaList = (raw) => {
    if (!raw) return [];
    return raw
        .split(",")
        .map((s) => s.trim())
        .filter((s) => s.length > 0);
};

const handleSubmit = async () => {
    isLoading.value = true;

    if (password.value !== confirmPassword.value) {
        showMessage("Passwords do not match. Please re-enter.", "error");
        isLoading.value = false;
        return;
    }

    try {
        // AUTO-ADD REQUIRED GENEDS
        if (!selectedGeneds.value.includes("GS")) {
            selectedGeneds.value.push("GS");
        }

        if (
            international.value === "yes" &&
            !selectedGeneds.value.includes("GG")
        ) {
            selectedGeneds.value.push("GG");
        }

        const fullName = `${firstName.value} ${lastName.value}`.trim();

        const { data, error } = await supabase.auth.signUp({
            email: email.value,
            password: password.value,
            options: {
                data: {
                    display_name: fullName,
                    first_name: firstName.value,
                    last_name: lastName.value,
                    date_of_birth: birthday.value || null,
                    international: international.value === "yes",
                    semester: semester.value ? Number(semester.value) : null,
                    enrollment: enrollment.value || null,
                    taken_courses: selectedCourses.value,
                    geneds: selectedGeneds.value,
                },
            },
        });

        console.log("signUp response:", data, error);

        if (error) throw error;

        const userId = data?.user?.id;
        if (!userId)
            throw new Error("Signup succeeded, but no user id returned.");

        const nowYear = new Date().getFullYear();
        let age = null;
        if (birthday.value) {
            const birthYear = new Date(birthday.value).getFullYear();
            if (!isNaN(birthYear)) {
                age = nowYear - birthYear;
            }
        }

        const extraCourses = parseCommaList(otherCourse.value);
        const extraGeneds = parseCommaList(otherGened.value);

        const personal = {
            user_id: userId,
            full_name: fullName,
            age: age ?? 0,
            is_international: international.value === "yes",
        };

        const academic = {
            user_id: userId,
            current_semester: semester.value ? Number(semester.value) : 0,
            taken_courses: [...selectedCourses.value, ...extraCourses],
            taken_geneds: [...selectedGeneds.value, ...extraGeneds],
        };

        console.log("Sending to data API:", { personal, academic });

        const resp = await fetch(`${DATA_API_URL}/register-student`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ personal, academic }),
        });

        const body = await resp.json().catch(() => ({}));
        console.log("Data API response:", resp.status, body);

        if (!resp.ok) {
            throw new Error(
                body?.detail ||
                    body?.message ||
                    "Failed to save student profile to data API."
            );
        }

        showMessage(
            "Account created and profile saved! Check your email to verify.",
            "success"
        );
        setTimeout(() => router.push("/confirmation"), 2500);
    } catch (err) {
        console.error("Signup error:", err);
        showMessage(err.message || "Signup failed. Please try again.", "error");
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    requestAnimationFrame(() => {
        showCard.value = true;
    });
});
</script>

<style scoped>
/* Card entrance animation */
.card-init {
    opacity: 0;
    transform: translateY(30px) scale(0.96);
    filter: blur(6px);
}
.card-in {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
    transition: all 700ms ease;
}
/* Message fade */
.fade-msg-enter-active,
.fade-msg-leave-active {
    transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-msg-enter-from,
.fade-msg-leave-to {
    opacity: 0;
    transform: translateY(-4px);
}

/* Chips styling (courses & geneds) */
.chip-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 8px 0 4px 0;
}

.chip {
    background: #f4f4f5;
    border: 1px solid #d4d4d8;
    border-radius: 999px;
    padding: 6px 12px;
    cursor: pointer;
    transition: all 0.15s ease-in-out;
    font-size: 0.8rem;
    color: #27272a;
}

.chip:hover {
    background-color: #ffe6eb;
    border-color: #e11d48;
}

.chip.selected {
    background-color: #800020;
    color: #fff;
    border-color: #800020;
}

/* disabled chip (e.g. auto-added GS / GG) */
.chip.disabled {
    opacity: 0.45;
    cursor: not-allowed;
    pointer-events: none;
}
</style>
