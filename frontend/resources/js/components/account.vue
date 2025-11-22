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
                        @click="$router.push('/chat')"
                        class="hidden sm:inline-flex border border-white/70 text-white font-medium px-3 py-1.5 rounded-lg text-sm hover:bg-white/10 transition"
                    >
                        ← Chat
                    </button>
                    <button
                        @click="handleLogout"
                        class="border border-white/80 bg-transparent text-white font-medium px-4 py-1.5 rounded-lg text-sm hover:bg-white hover:text-[#800020] transition"
                    >
                        Logout
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

                <!-- ACCOUNT CARD -->
                <div
                    :class="[
                        'relative z-10 bg-white/95 text-black backdrop-blur-xl rounded-2xl border border-white/40 px-8 py-10 shadow-xl',
                        'transform-gpu transition-all duration-700',
                        showCard ? 'card-in' : 'card-init',
                    ]"
                >
                    <h1 class="text-2xl font-bold mb-2 text-center">
                        Account Details
                    </h1>
                    <p class="text-sm text-neutral-700 mb-6 text-center">
                        Your personal and academic information.
                    </p>

                    <!-- LOADING STATE -->
                    <div v-if="isLoading" class="text-center py-8">
                        <div
                            class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-[#800020]"
                        ></div>
                        <p class="mt-2 text-neutral-600">
                            Loading account details...
                        </p>
                    </div>

                    <!-- ERROR STATE -->
                    <div v-else-if="error" class="text-center py-8">
                        <p class="text-red-600 mb-4">{{ error }}</p>
                        <button
                            @click="fetchAccountDetails"
                            class="bg-[#880808] text-white px-4 py-2 rounded-lg hover:bg-[#700618] transition"
                        >
                            Try Again
                        </button>
                    </div>

                    <!-- ACCOUNT DETAILS -->
                    <div v-else-if="studentData" class="space-y-6">
                        <!-- PERSONAL INFORMATION -->
                        <div class="bg-neutral-50 rounded-xl p-6">
                            <h2
                                class="text-lg font-semibold mb-4 text-[#800020] border-b pb-2"
                            >
                                Personal Information
                            </h2>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        Full Name
                                    </label>
                                    <p class="text-black font-semibold">
                                        {{
                                            studentData.personal?.full_name ||
                                            studentData.full_name ||
                                            "Not provided"
                                        }}
                                    </p>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        Age
                                    </label>
                                    <p class="text-black font-semibold">
                                        {{
                                            studentData.personal?.age ||
                                            studentData.age ||
                                            "Not provided"
                                        }}
                                    </p>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        International Student
                                    </label>
                                    <p class="text-black font-semibold">
                                        {{
                                            studentData.personal
                                                ?.is_international ||
                                            studentData.is_international
                                                ? "Yes"
                                                : "No"
                                        }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- ACADEMIC INFORMATION -->
                        <div class="bg-neutral-50 rounded-xl p-6">
                            <h2
                                class="text-lg font-semibold mb-4 text-[#800020] border-b pb-2"
                            >
                                Academic Information
                            </h2>
                            <div
                                class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4"
                            >
                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        Current Semester
                                    </label>
                                    <p class="text-black font-semibold">
                                        {{
                                            studentData.academic
                                                ?.current_semester ||
                                            studentData.current_semester ||
                                            "Not provided"
                                        }}
                                    </p>
                                </div>
                            </div>

                            <!-- TAKEN COURSES -->
                            <div class="mt-4">
                                <label
                                    class="block text-sm font-medium text-neutral-600 mb-2"
                                >
                                    Taken Courses
                                </label>
                                <div
                                    v-if="
                                        (studentData.academic?.taken_courses &&
                                            studentData.academic.taken_courses
                                                .length) ||
                                        (studentData.taken_courses &&
                                            studentData.taken_courses.length)
                                    "
                                    class="chip-container"
                                >
                                    <div
                                        v-for="course in studentData.academic
                                            ?.taken_courses ||
                                        studentData.taken_courses ||
                                        []"
                                        :key="course"
                                        class="chip selected"
                                    >
                                        {{ course }}
                                    </div>
                                </div>
                                <p v-else class="text-neutral-500 italic">
                                    No courses recorded
                                </p>
                            </div>

                            <!-- GENEDS -->
                            <div class="mt-4">
                                <label
                                    class="block text-sm font-medium text-neutral-600 mb-2"
                                >
                                    Taken GenEds
                                </label>
                                <div
                                    v-if="
                                        (studentData.academic?.taken_geneds &&
                                            studentData.academic.taken_geneds
                                                .length) ||
                                        (studentData.taken_geneds &&
                                            studentData.taken_geneds.length) ||
                                        (studentData.geneds &&
                                            studentData.geneds.length)
                                    "
                                    class="chip-container"
                                >
                                    <div
                                        v-for="gened in studentData.academic
                                            ?.taken_geneds ||
                                        studentData.taken_geneds ||
                                        studentData.geneds ||
                                        []"
                                        :key="gened"
                                        class="chip selected"
                                    >
                                        {{ gened }}
                                    </div>
                                </div>
                                <p v-else class="text-neutral-500 italic">
                                    No GenEds recorded
                                </p>
                            </div>
                        </div>

                        <!-- AUTH INFORMATION -->
                        <div class="bg-neutral-50 rounded-xl p-6">
                            <h2
                                class="text-lg font-semibold mb-4 text-[#800020] border-b pb-2"
                            >
                                Account Information
                            </h2>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        Email
                                    </label>
                                    <p class="text-black font-semibold">
                                        {{ authData?.email || "Not available" }}
                                    </p>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        Email Verified
                                    </label>
                                    <p class="text-black font-semibold">
                                        {{
                                            authData?.email_confirmed_at
                                                ? "Yes"
                                                : "No"
                                        }}
                                    </p>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        Account Created
                                    </label>
                                    <p class="text-black font-semibold">
                                        {{ formatDate(authData?.created_at) }}
                                    </p>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        Last Sign In
                                    </label>
                                    <p class="text-black font-semibold">
                                        {{
                                            formatDate(
                                                authData?.last_sign_in_at
                                            )
                                        }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- NO DATA STATE -->
                    <div v-else class="text-center py-8">
                        <p class="text-neutral-600">No account data found.</p>
                        <button
                            @click="fetchAccountDetails"
                            class="bg-[#880808] text-white px-4 py-2 rounded-lg hover:bg-[#700618] transition mt-4"
                        >
                            Retry Fetch
                        </button>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { supabase } from "../supabase";
import axios from "axios";

const router = useRouter();

const isLoading = ref(false);
const showCard = ref(false);
const studentData = ref(null);
const authData = ref(null);
const error = ref("");
const debugInfo = ref("");

const DATA_URL = "https://supabase-kqbi.onrender.com";

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
    setTimeout(() => {
        message.value.visible = false;
    }, 5000);
};

const formatDate = (dateString) => {
    if (!dateString) return "Not available";
    return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
};

const fetchAccountDetails = async () => {
    isLoading.value = true;
    error.value = "";
    debugInfo.value = "";

    try {
        // Get current user from Supabase
        const {
            data: { user },
            error: authError,
        } = await supabase.auth.getUser();

        if (authError) throw authError;
        if (!user) {
            throw new Error("No user logged in");
        }

        console.log("Fetching data for user:", user.id);

        // Store auth data
        authData.value = {
            email: user.email,
            email_confirmed_at: user.email_confirmed_at,
            created_at: user.created_at,
            last_sign_in_at: user.last_sign_in_at,
        };

        // Try the main students endpoint (same as chatpage)
        try {
            console.log("Trying endpoint:", `${DATA_URL}/students/${user.id}`);
            const response = await axios.get(`${DATA_URL}/students/${user.id}`);
            console.log("Response received:", response.data);

            if (response.data) {
                studentData.value = response.data;
                debugInfo.value = JSON.stringify(response.data, null, 2);
            } else {
                throw new Error("Empty response from server");
            }
        } catch (apiError) {
            console.error("API Error:", apiError);
            debugInfo.value = `API Error: ${apiError.message}\nEndpoint: ${DATA_URL}/students/${user.id}`;

            // Try alternative endpoints
            try {
                console.log("Trying alternative endpoint: /student_personal");
                const personalResponse = await axios.get(
                    `${DATA_URL}/student_personal/${user.id}`
                );
                console.log("Personal response:", personalResponse.data);

                const academicResponse = await axios.get(
                    `${DATA_URL}/student_academic/${user.id}`
                );
                console.log("Academic response:", academicResponse.data);

                studentData.value = {
                    personal: personalResponse.data,
                    academic: academicResponse.data,
                };
                debugInfo.value += `\n\nAlternative endpoint data:\nPersonal: ${JSON.stringify(
                    personalResponse.data,
                    null,
                    2
                )}\nAcademic: ${JSON.stringify(
                    academicResponse.data,
                    null,
                    2
                )}`;
            } catch (altError) {
                console.error("Alternative endpoint error:", altError);
                throw new Error(
                    `Cannot fetch student data: ${apiError.message}`
                );
            }
        }

        if (!studentData.value) {
            throw new Error("No student data found");
        }
    } catch (err) {
        console.error("Error fetching account details:", err);
        error.value = err.message || "Failed to load account details";
        showMessage(error.value, "error");
        debugInfo.value = `Final Error: ${err.message}\nStack: ${err.stack}`;
    } finally {
        isLoading.value = false;
    }
};

const handleLogout = async () => {
    try {
        const { error } = await supabase.auth.signOut();
        if (error) throw error;

        router.push("/login");
    } catch (err) {
        console.error("Logout error:", err);
        showMessage("Failed to logout", "error");
    }
};

onMounted(() => {
    requestAnimationFrame(() => {
        showCard.value = true;
    });
    fetchAccountDetails();
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

/* Chips styling */
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
    transition: all 0.15s ease-in-out;
    font-size: 0.8rem;
    color: #27272a;
}

.chip.selected {
    background-color: #800020;
    color: #fff;
    border-color: #800020;
}

/* Loading spinner */
.animate-spin {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>
