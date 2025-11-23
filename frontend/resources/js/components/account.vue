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
import { ref, onMounted, watch } from "vue";
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
const isEditing = ref(false);
const selectedFile = ref(null);
const previewImage = ref(null);

const DATA_URL = "https://supabase-kqbi.onrender.com";

// -----------------------
// Fields for editing mode
// -----------------------
const editData = ref({
    full_name: "",
    age: "",
    is_international: false,
    current_semester: "",
    taken_courses: [],
    taken_geneds: [],
});

// -----------------------
// Enable / Disable Editing
// -----------------------
const enableEditing = () => {
    isEditing.value = true;

    editData.value = {
        full_name: studentData.value.personal?.full_name || "",
        age: studentData.value.personal?.age || "",
        is_international: studentData.value.personal?.is_international || false,
        current_semester: studentData.value.academic?.current_semester || "",
        taken_courses: [...(studentData.value.academic?.taken_courses || [])],
        taken_geneds: [...(studentData.value.academic?.taken_geneds || [])],
    };
};

const cancelEditing = () => {
    isEditing.value = false;
    selectedFile.value = null;
    previewImage.value = null;
};

// -----------------------
// IMAGE PREVIEW HANDLER
// -----------------------
const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    selectedFile.value = file;

    const reader = new FileReader();
    reader.onload = (e) => (previewImage.value = e.target.result);
    reader.readAsDataURL(file);
};

// -----------------------
// NOTIFICATION SYSTEM
// -----------------------
const message = ref({ text: "", type: "", visible: false });

const showMessage = (text, type) => {
    message.value = { text, type, visible: true };
    setTimeout(() => (message.value.visible = false), 5000);
};

// -----------------------
// SAVE CHANGES
// -----------------------
const saveChanges = async () => {
    try {
        isLoading.value = true;
        const user = (await supabase.auth.getUser()).data.user;

        // -----------------------------
        // 1. Upload image to bucket "avatars"
        // -----------------------------
        let imageUrl = studentData.value.personal?.profile_picture;

        if (selectedFile.value) {
            const fileExt = selectedFile.value.name.split(".").pop();
            const fileName = `${user.id}.${fileExt}`;

            const { error: uploadError } = await supabase.storage
                .from("avatars")
                .upload(fileName, selectedFile.value, { upsert: true });

            if (uploadError) throw uploadError;

            // Get public URL
            const { data: publicURL } = supabase.storage
                .from("avatars")
                .getPublicUrl(fileName);

            imageUrl = publicURL.publicUrl;
        }

        // -----------------------------
        // 2. Clean Courses
        // -----------------------------
        const cleanCourses = editData.value.taken_courses.map((c) =>
            c.replace(/\s*\(\d+\)\s*$/, "").trim()
        );
        const uniqueCourses = [...new Set(cleanCourses)];

        // -----------------------------
        // 3. Clean GenEd Types
        // -----------------------------
        let uniqueGeneds = [
            ...new Set(editData.value.taken_geneds.map((g) => g.trim())),
        ];

        // Auto-add GG if international
        if (editData.value.is_international && !uniqueGeneds.includes("GG")) {
            uniqueGeneds.push("GG");
        }

        // -----------------------------
        // 4. Update personal info
        // -----------------------------
        await axios.put(
            `${DATA_URL}/students/update-personal/${user.id}`,
            {
                full_name: editData.value.full_name,
                age: editData.value.age,
                is_international: editData.value.is_international,
                profile_picture: imageUrl,
            }
        );

        // -----------------------------
        // 5. Update academic info
        // -----------------------------
        await axios.put(
            `${DATA_URL}/students/update-academic/${user.id}`,
            {
                current_semester: editData.value.current_semester,
                taken_courses: uniqueCourses,
                taken_geneds: uniqueGeneds,
            }
        );

        showMessage("Account updated successfully!", "success");
        isEditing.value = false;

        selectedFile.value = null;
        previewImage.value = null;

        await fetchAccountDetails();
    } catch (err) {
        console.error(err);
        showMessage("Failed to save account changes.", "error");
    } finally {
        isLoading.value = false;
    }
};

// -----------------------
// WATCHER to convert arrays <-> strings
// -----------------------
watch(isEditing, (editing) => {
    if (editing) {
        editData.value.taken_courses_string =
            (editData.value.taken_courses || []).join(", ");
        editData.value.taken_geneds_string =
            (editData.value.taken_geneds || []).join(", ");
    } else {
        editData.value.taken_courses =
            editData.value.taken_courses_string
                ?.split(",")
                .map((c) => c.trim())
                .filter(Boolean) || [];

        editData.value.taken_geneds =
            editData.value.taken_geneds_string
                ?.split(",")
                .map((g) => g.trim())
                .filter(Boolean) || [];
    }
});

// -----------------------
// FETCH ACCOUNT DETAILS
// -----------------------
const fetchAccountDetails = async () => {
    isLoading.value = true;
    error.value = "";
    debugInfo.value = "";

    try {
        const { data: { user } } = await supabase.auth.getUser();
        if (!user) throw new Error("No user logged in.");

        authData.value = {
            email: user.email,
            email_confirmed_at: user.email_confirmed_at,
            created_at: user.created_at,
            last_sign_in_at: user.last_sign_in_at,
        };

        const response = await axios.get(`${DATA_URL}/students/${user.id}`);
        studentData.value = response.data;

        debugInfo.value = JSON.stringify(studentData.value, null, 2);
    } catch (err) {
        console.error(err);
        error.value = err.message || "Failed to fetch account details.";
        showMessage(error.value, "error");
    } finally {
        isLoading.value = false;
    }
};

// -----------------------
// LOGOUT
// -----------------------
const handleLogout = async () => {
    try {
        await supabase.auth.signOut();
        router.push("/login");
    } catch (err) {
        showMessage("Failed to logout.", "error");
    }
};

// -----------------------
// ON MOUNT
// -----------------------
onMounted(async () => {
    requestAnimationFrame(() => (showCard.value = true));
    await fetchAccountDetails();
});
</script>
