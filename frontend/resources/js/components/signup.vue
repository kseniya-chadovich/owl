<template>
    <div
        class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50/30 flex flex-col"
    >
        <header
            class="w-full border-b border-white/20 bg-white/80 backdrop-blur-xl shadow-sm"
        >
            <div
                class="flex justify-between items-center max-w-7xl mx-auto px-6 py-4"
            >
                <div class="flex items-center gap-3">
                    <div
                        class="w-10 h-10 bg-gradient-to-br from-[#800020] to-[#a83232] rounded-xl flex items-center justify-center shadow-lg"
                    >
                        <span class="text-white font-bold text-lg">AI</span>
                    </div>
                    <h1
                        class="text-xl font-bold bg-gradient-to-r from-[#800020] to-[#a83232] bg-clip-text text-transparent"
                    >
                        Scheduler
                    </h1>
                </div>

                <div class="flex items-center gap-3">
                    <button
                        @click="$router.push('/')"
                        class="border border-slate-300 bg-white text-slate-700 px-4 py-2 rounded-xl hover:bg-slate-50 hover:border-slate-400 transition-all duration-300 font-medium text-sm"
                    >
                        ← Home
                    </button>
                    <button
                        @click="$router.push('/login')"
                        class="bg-gradient-to-r from-[#800020] to-[#a83232] text-white px-4 py-2 rounded-xl hover:shadow-md transition-all duration-300 font-medium text-sm"
                    >
                        Login
                    </button>
                </div>
            </div>
        </header>

        <main class="flex-1 flex items-start justify-center px-4 py-8">
            <div class="w-full max-w-4xl fade-up" :class="{ in: isMounted }">
                <transition name="fade-msg">
                    <div
                        v-if="message.visible"
                        :class="[
                            'mb-6 flex items-center justify-between px-4 py-3 rounded-xl border shadow-sm text-sm',
                            message.type === 'success'
                                ? 'bg-emerald-50 border-emerald-200 text-emerald-700'
                                : 'bg-red-50 border-red-200 text-red-700',
                        ]"
                    >
                        <div class="flex items-center gap-3">
                            <div
                                :class="[
                                    'w-6 h-6 rounded-full flex items-center justify-center',
                                    message.type === 'success'
                                        ? 'bg-emerald-100 text-emerald-600'
                                        : 'bg-red-100 text-red-600',
                                ]"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-4 w-4"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        v-if="message.type === 'success'"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M5 13l4 4L19 7"
                                    />
                                    <path
                                        v-else
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M6 18L18 6M6 6l12 12"
                                    />
                                </svg>
                            </div>
                            <span class="font-medium">{{ message.text }}</span>
                        </div>
                        <button
                            @click="message.visible = false"
                            class="ml-4 text-lg leading-none hover:scale-110 transition-transform text-slate-500 hover:text-slate-700"
                        >
                            &times;
                        </button>
                    </div>
                </transition>

                <div
                    class="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 slide-up"
                    :class="{ in: isMounted }"
                >
                    <div class="text-center mb-8">
                        <h1
                            class="text-3xl font-bold text-slate-800 mb-3 slide-up"
                            :class="{ in: isMounted }"
                            style="animation-delay: 0.1s"
                        >
                            Create Your Account 🎓
                        </h1>
                        <p
                            class="text-slate-600 text-base slide-up"
                            :class="{ in: isMounted }"
                            style="animation-delay: 0.2s"
                        >
                            Sign up and tell us about your academic background
                        </p>
                    </div>

                    <form @submit.prevent="handleSubmit" class="space-y-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div
                                class="space-y-2 slide-up"
                                :class="{ in: isMounted }"
                                style="animation-delay: 0.3s"
                            >
                                <label
                                    for="firstName"
                                    class="text-sm font-medium text-slate-700"
                                    >First Name</label
                                >
                                <input
                                    type="text"
                                    id="firstName"
                                    v-model="firstName"
                                    required
                                    class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                                    placeholder="Enter your first name"
                                />
                            </div>

                            <div
                                class="space-y-2 slide-up"
                                :class="{ in: isMounted }"
                                style="animation-delay: 0.4s"
                            >
                                <label
                                    for="lastName"
                                    class="text-sm font-medium text-slate-700"
                                    >Last Name</label
                                >
                                <input
                                    type="text"
                                    id="lastName"
                                    v-model="lastName"
                                    required
                                    class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                                    placeholder="Enter your last name"
                                />
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div
                                class="space-y-2 slide-up"
                                :class="{ in: isMounted }"
                                style="animation-delay: 0.5s"
                            >
                                <label
                                    for="email"
                                    class="text-sm font-medium text-slate-700"
                                    >Email</label
                                >
                                <input
                                    type="email"
                                    id="email"
                                    v-model="email"
                                    required
                                    class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                                    placeholder="Enter your email"
                                />
                            </div>

                            <div
                                class="space-y-2 slide-up"
                                :class="{ in: isMounted }"
                                style="animation-delay: 0.6s"
                            >
                                <label
                                    for="birthday"
                                    class="text-sm font-medium text-slate-700"
                                    >Date of Birth</label
                                >
                                <input
                                    type="date"
                                    id="birthday"
                                    v-model="birthday"
                                    class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                                />
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div
                                class="space-y-2 slide-up"
                                :class="{ in: isMounted }"
                                style="animation-delay: 0.7s"
                            >
                                <label
                                    for="password"
                                    class="text-sm font-medium text-slate-700"
                                    >Password</label
                                >
                                <input
                                    type="password"
                                    id="password"
                                    v-model="password"
                                    required
                                    class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                                    placeholder="Create a password"
                                />
                            </div>

                            <div
                                class="space-y-2 slide-up"
                                :class="{ in: isMounted }"
                                style="animation-delay: 0.8s"
                            >
                                <label
                                    for="confirmPassword"
                                    class="text-sm font-medium text-slate-700"
                                    >Confirm Password</label
                                >
                                <input
                                    type="password"
                                    id="confirmPassword"
                                    v-model="confirmPassword"
                                    required
                                    class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                                    placeholder="Confirm your password"
                                />
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div
                                class="space-y-2 slide-up"
                                :class="{ in: isMounted }"
                                style="animation-delay: 0.9s"
                            >
                                <p class="text-sm font-medium text-slate-700">
                                    International Student
                                </p>
                                <div
                                    class="flex items-center gap-4 text-sm text-slate-700"
                                >
                                    <label
                                        class="inline-flex items-center gap-2"
                                    >
                                        <input
                                            type="radio"
                                            value="yes"
                                            v-model="international"
                                            class="h-4 w-4 text-[#800020] focus:ring-[#800020]"
                                        />
                                        <span>Yes</span>
                                    </label>
                                    <label
                                        class="inline-flex items-center gap-2"
                                    >
                                        <input
                                            type="radio"
                                            value="no"
                                            v-model="international"
                                            class="h-4 w-4 text-[#800020] focus:ring-[#800020]"
                                        />
                                        <span>No</span>
                                    </label>
                                </div>
                            </div>

                            <div
                                class="space-y-2 slide-up"
                                :class="{ in: isMounted }"
                                style="animation-delay: 1s"
                            >
                                <label
                                    for="semester"
                                    class="text-sm font-medium text-slate-700"
                                    >Current Semester</label
                                >
                                <select
                                    id="semester"
                                    v-model="semester"
                                    class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                                >
                                    <option disabled value="">
                                        Select semester
                                    </option>
                                    <option v-for="n in 8" :key="n" :value="n">
                                        {{ n }}
                                    </option>
                                </select>
                            </div>

                            <div
                                class="space-y-2 slide-up"
                                :class="{ in: isMounted }"
                                style="animation-delay: 1.1s"
                            >
                                <p class="text-sm font-medium text-slate-700">
                                    Enrollment Type
                                </p>
                                <div
                                    class="flex items-center gap-4 text-sm text-slate-700"
                                >
                                    <label
                                        class="inline-flex items-center gap-2"
                                    >
                                        <input
                                            type="radio"
                                            value="full-time"
                                            v-model="enrollment"
                                            class="h-4 w-4 text-[#800020] focus:ring-[#800020]"
                                        />
                                        <span>Full-time</span>
                                    </label>
                                    <label
                                        class="inline-flex items-center gap-2"
                                    >
                                        <input
                                            type="radio"
                                            value="part-time"
                                            v-model="enrollment"
                                            class="h-4 w-4 text-[#800020] focus:ring-[#800020]"
                                        />
                                        <span>Part-time</span>
                                    </label>
                                </div>
                            </div>
                        </div>

                        <div
                            class="space-y-3 slide-up"
                            :class="{ in: isMounted }"
                            style="animation-delay: 1.2s"
                        >
                            <label class="text-sm font-medium text-slate-700"
                                >Taken Courses</label
                            >
                            <p class="text-xs text-slate-500">
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

                            <div class="space-y-2">
                                <label
                                    for="otherCourse"
                                    class="text-sm font-medium text-slate-700"
                                    >Other Course(s)</label
                                >
                                <input
                                    type="text"
                                    id="otherCourse"
                                    v-model="otherCourse"
                                    placeholder="Enter any additional courses (comma separated)"
                                    class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                                />
                            </div>
                        </div>

                        <div
                            class="space-y-3 slide-up"
                            :class="{ in: isMounted }"
                            style="animation-delay: 1.3s"
                        >
                            <label class="text-sm font-medium text-slate-700"
                                >Taken GenEd Types</label
                            >
                            <p class="text-xs text-slate-500">
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

                            <div class="space-y-2">
                                <label
                                    for="otherGened"
                                    class="text-sm font-medium text-slate-700"
                                    >Other GenEd Type(s)</label
                                >
                                <input
                                    type="text"
                                    id="otherGened"
                                    v-model="otherGened"
                                    placeholder="Enter other GenEd types (comma separated)"
                                    class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                                />
                            </div>
                        </div>

                        <div
                            class="space-y-4 slide-up"
                            :class="{ in: isMounted }"
                            style="animation-delay: 1.4s"
                        >
                            <button
                                type="submit"
                                class="w-full bg-gradient-to-r from-[#800020] to-[#a83232] text-white font-semibold py-3.5 rounded-xl hover:shadow-md transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                                :disabled="isLoading"
                            >
                                <span
                                    v-if="isLoading"
                                    class="flex items-center justify-center gap-2"
                                >
                                    <div
                                        class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
                                    ></div>
                                    Creating Account...
                                </span>
                                <span v-else>Create Account</span>
                            </button>

                            <p class="text-center text-slate-600 text-sm">
                                Already have an account?
                                <button
                                    type="button"
                                    @click="$router.push('/login')"
                                    class="font-medium text-[#800020] hover:text-[#a83232] transition-colors underline"
                                >
                                    Log in here
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
const isMounted = ref(false);

const DATA_API_URL =
    import.meta.env.VITE_DATA_API_URL || "https://supabase-kqbi.onrender.com";

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
        if (!selectedGeneds.value.includes("GS"))
            selectedGeneds.value.push("GS");
        if (
            international.value === "yes" &&
            !selectedGeneds.value.includes("GG")
        )
            selectedGeneds.value.push("GG");

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

        if (error) throw error;

        const userId = data?.user?.id;
        if (!userId)
            throw new Error("Signup succeeded, but no user id returned.");

        const nowYear = new Date().getFullYear();
        let age = null;
        if (birthday.value) {
            const birthYear = new Date(birthday.value).getFullYear();
            if (!isNaN(birthYear)) age = nowYear - birthYear;
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

        const resp = await fetch(`${DATA_API_URL}/register-student`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ personal, academic }),
        });

        const body = await resp.json().catch(() => ({}));
        if (!resp.ok)
            throw new Error(
                body?.detail ||
                    body?.message ||
                    "Failed to save student profile to data API."
            );

        showMessage(
            "Account created and profile saved! Check your email to verify.",
            "success"
        );
        setTimeout(() => router.push("/confirmation"), 2500);
    } catch (err) {
        showMessage(err.message || "Signup failed. Please try again.", "error");
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    setTimeout(() => {
        isMounted.value = true;
    }, 100);
});
</script>

<style scoped>
.fade-msg-enter-active,
.fade-msg-leave-active {
    transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-msg-enter-from,
.fade-msg-leave-to {
    opacity: 0;
    transform: translateY(-4px);
}

.fade-up {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}
.fade-up.in {
    opacity: 1;
    transform: translateY(0);
}

.slide-up {
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.5s ease, transform 0.5s ease;
}
.slide-up.in {
    opacity: 1;
    transform: translateY(0);
}

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

.chip.disabled {
    opacity: 0.45;
    cursor: not-allowed;
    pointer-events: none;
}
</style>
