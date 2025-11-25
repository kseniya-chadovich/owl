<template>
    <div
        class="min-h-screen bg-gradient-to-b from-[#800020] to-[#880808] text-white flex flex-col"
    >
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

        <main class="flex-1 flex items-start justify-center px-4 py-10">
            <div class="relative w-full max-w-4xl">
                <div
                    class="pointer-events-none absolute -inset-6 rounded-3xl bg-gradient-to-br from-white/40 via-white/5 to-transparent blur-2xl opacity-70"
                ></div>

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

                    <div v-if="isLoading" class="text-center py-8">
                        <div
                            class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-[#800020]"
                        ></div>
                        <p class="mt-2 text-neutral-600">
                            Loading account details...
                        </p>
                    </div>

                    <div v-else-if="error" class="text-center py-8">
                        <p class="text-red-600 mb-4">{{ error }}</p>
                        <button
                            @click="fetchAccountDetails"
                            class="bg-[#880808] text-white px-4 py-2 rounded-lg hover:bg-[#700618] transition"
                        >
                            Try Again
                        </button>
                    </div>

                    <div v-else-if="studentData" class="space-y-6">
                        <div class="flex justify-end mb-4">
                            <button
                                v-if="!isEditing"
                                @click="enableEditing"
                                class="px-4 py-2 bg-[#880808] text-white rounded-lg hover:bg-[#700618]"
                            >
                                Edit
                            </button>

                            <div v-else class="flex gap-3">
                                <button
                                    @click="saveChanges"
                                    class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                                >
                                    Save
                                </button>
                                <button
                                    @click="cancelEditing"
                                    class="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500"
                                >
                                    Cancel
                                </button>
                            </div>
                        </div>

                        <div class="flex flex-col items-center mb-6">
                            <div class="relative">
                                <img
                                    :src="
                                        previewImage ||
                                        studentData.personal?.profile_picture ||
                                        defaultProfile
                                    "
                                    class="w-28 h-28 rounded-full object-cover border-2 border-[#800020]"
                                />

                                <input
                                    ref="fileInput"
                                    type="file"
                                    accept="image/*"
                                    class="hidden"
                                    @change="handleImageUpload"
                                />
                            </div>

                            <button
                                v-if="isEditing"
                                @click="$refs.fileInput.click()"
                                class="mt-3 px-3 py-1.5 bg-[#800020] text-white text-sm rounded-lg hover:bg-[#6a001a] transition"
                            >
                                Change Photo
                            </button>
                        </div>

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

                                    <p
                                        v-if="!isEditing"
                                        class="text-black font-semibold"
                                    >
                                        {{
                                            studentData.personal?.full_name ||
                                            "Not provided"
                                        }}
                                    </p>

                                    <input
                                        v-else
                                        v-model="editData.full_name"
                                        class="w-full px-3 py-2 border rounded-md"
                                    />
                                </div>

                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        Age
                                    </label>

                                    <p
                                        v-if="!isEditing"
                                        class="text-black font-semibold"
                                    >
                                        {{
                                            studentData.personal?.age ??
                                            "Not provided"
                                        }}
                                    </p>

                                    <input
                                        v-else
                                        v-model.number="editData.age"
                                        type="number"
                                        min="0"
                                        class="w-full px-3 py-2 border rounded-md"
                                    />
                                </div>

                                <div>
                                    <label
                                        class="block text-sm font-medium text-neutral-600 mb-1"
                                    >
                                        International Student
                                    </label>

                                    <p
                                        v-if="!isEditing"
                                        class="text-black font-semibold"
                                    >
                                        {{
                                            studentData.personal
                                                ?.is_international
                                                ? "Yes"
                                                : "No"
                                        }}
                                    </p>

                                    <select
                                        v-else
                                        v-model="editData.is_international"
                                        class="w-full px-3 py-2 border rounded-md"
                                    >
                                        <option :value="true">Yes</option>
                                        <option :value="false">No</option>
                                    </select>
                                </div>
                            </div>
                        </div>

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

                                    <p
                                        v-if="!isEditing"
                                        class="text-black font-semibold"
                                    >
                                        {{
                                            studentData.academic
                                                ?.current_semester ??
                                            "Not provided"
                                        }}
                                    </p>

                                    <input
                                        v-else
                                        v-model.number="
                                            editData.current_semester
                                        "
                                        type="number"
                                        min="1"
                                        class="w-full px-3 py-2 border rounded-md"
                                    />
                                </div>
                            </div>

                            <div class="mt-4">
                                <label
                                    class="block text-sm font-medium text-neutral-600 mb-2"
                                >
                                    Taken Courses
                                </label>

                                <div v-if="!isEditing">
                                    <div
                                        v-if="
                                            studentData.academic
                                                ?.taken_courses &&
                                            studentData.academic.taken_courses
                                                .length
                                        "
                                        class="chip-container"
                                    >
                                        <div
                                            v-for="course in studentData
                                                .academic.taken_courses"
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

                                <textarea
                                    v-else
                                    v-model="editData.taken_courses_string"
                                    class="w-full px-3 py-2 border rounded-md"
                                    placeholder="CIS1001, MATH1041, ..."
                                ></textarea>
                            </div>

                            <div class="mt-4">
                                <label
                                    class="block text-sm font-medium text-neutral-600 mb-2"
                                >
                                    Taken GenEds
                                </label>

                                <div v-if="!isEditing">
                                    <div
                                        v-if="
                                            studentData.academic
                                                ?.taken_geneds &&
                                            studentData.academic.taken_geneds
                                                .length
                                        "
                                        class="chip-container"
                                    >
                                        <div
                                            v-for="gen in studentData.academic
                                                .taken_geneds"
                                            :key="gen"
                                            class="chip selected"
                                        >
                                            {{ gen }}
                                        </div>
                                    </div>

                                    <p v-else class="text-neutral-500 italic">
                                        No GenEds recorded
                                    </p>
                                </div>

                                <textarea
                                    v-else
                                    v-model="editData.taken_geneds_string"
                                    class="w-full px-3 py-2 border rounded-md"
                                    placeholder="GA, GB, GD, ..."
                                ></textarea>
                            </div>
                        </div>

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
const isEditing = ref(false);
const fileInput = ref(null);
const previewImage = ref(null);
const selectedFile = ref(null);

const DATA_URL = "https://supabase-kqbi.onrender.com";

const editData = ref({
    full_name: "",
    age: "",
    is_international: false,
    current_semester: "",
    taken_courses: [],
    taken_geneds: [],

    taken_courses_string: "",  
    taken_geneds_string: "",  
});

const enableEditing = () => {
    isEditing.value = true;

    editData.value = {
        full_name: studentData.value.personal?.full_name || "",
        age: studentData.value.personal?.age || "",
        is_international: studentData.value.personal?.is_international || false,
        current_semester: studentData.value.academic?.current_semester || "",

        taken_courses: [...(studentData.value.academic?.taken_courses || [])],
        taken_geneds: [...(studentData.value.academic?.taken_geneds || [])],

        taken_courses_string: (studentData.value.academic?.taken_courses || []).join(", "),
        taken_geneds_string: (studentData.value.academic?.taken_geneds || []).join(", "),
    };
};

const cancelEditing = () => {
    isEditing.value = false;
};

const defaultProfile = "https://placehold.co/200x200?text=No+Image";

const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    selectedFile.value = file;

    const reader = new FileReader();
    reader.onload = (e) => (previewImage.value = e.target.result);
    reader.readAsDataURL(file);
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

const message = ref({
    text: "",
    type: "",
    visible: false,
});

const showMessage = (text, type) => {
    message.value.text = text;
    message.value.type = type;
    message.value.visible = true;
    setTimeout(() => (message.value.visible = false), 5000);
};

const saveChanges = async () => {
    try {
        isLoading.value = true;
        const user = (await supabase.auth.getUser()).data.user;

        let imageUrl = studentData.value.personal?.profile_picture;

        if (selectedFile.value) {
            const ext = selectedFile.value.name.split(".").pop();
            const fileName = `${user.id}.${ext}`;

            const { data: existingFiles, error: listError } = await supabase.storage
                .from("avatars")
                .list("", { search: fileName });

            const fileExists = existingFiles?.some(f => f.name === fileName);

            let uploadResult;
            
            if (fileExists) {
                uploadResult = await supabase.storage
                    .from("avatars")
                    .update(fileName, selectedFile.value);
                }

            else {
                uploadResult = await supabase.storage
                    .from("avatars")
                    .upload(fileName, selectedFile.value);
                }

            if (uploadResult.error) throw uploadResult.error;

            const { data: urlData } = supabase.storage
                .from("avatars")
                .getPublicUrl(fileName);

            imageUrl = `${urlData.publicUrl}?t=${Date.now()}`;
    }

        const formattedCourses = editData.value.taken_courses_string
            .split(",")
            .map((c) => c.trim())
            .filter((c) => c.length > 0)
            .map((c) => c.replace(/\s*\(\d+\)\s*$/, "").trim());

        const uniqueCourses = [...new Set(formattedCourses)];

        const formattedGeneds = editData.value.taken_geneds_string
            .split(",")
            .map((g) => g.trim().toUpperCase())
            .filter((g) => g.length > 0);

        let uniqueGeneds = [...new Set(formattedGeneds)];

        if (editData.value.is_international && !uniqueGeneds.includes("GG")) {
            uniqueGeneds.push("GG");
        }

        await axios.put(`${DATA_URL}/students/update-personal/${user.id}`, {
            full_name: editData.value.full_name,
            age: editData.value.age,
            is_international: editData.value.is_international,
            profile_picture: imageUrl,
        });

        await axios.put(`${DATA_URL}/students/update-academic/${user.id}`, {
            current_semester: editData.value.current_semester,
            taken_courses: uniqueCourses,
            taken_geneds: uniqueGeneds,
        });

        showMessage("Account updated!", "success");

        isEditing.value = false;
        selectedFile.value = null;
        previewImage.value = null;
        await fetchAccountDetails();

    } catch (err) {
        console.error(err);
        showMessage("Failed to save changes", "error");
    } finally {
        isLoading.value = false;
    }
};

watch(
    () => editData.value.taken_courses_string,
    (newVal) => {
        editData.value.taken_courses = newVal
            .split(",")
            .map((c) => c.trim())
            .filter((c) => c.length > 0);
    }
);

watch(
    () => editData.value.taken_geneds_string,
    (newVal) => {
        editData.value.taken_geneds = newVal
            .split(",")
            .map((g) => g.trim())
            .filter((g) => g.length > 0);
    }
);

const fetchAccountDetails = async () => {
    try {
        isLoading.value = true;

        const { data: { user } } = await supabase.auth.getUser();
        if (!user) throw new Error("No user logged in.");

        authData.value = {
            email: user.email,
            email_confirmed_at: user.email_confirmed_at,
            created_at: user.created_at,
            last_sign_in_at: user.last_sign_in_at,
        };

        const resp = await axios.get(`${DATA_URL}/students/${user.id}`);
        studentData.value = resp.data;

    } catch (err) {
        error.value = err.message || "Failed to fetch account details";
        showMessage(error.value, "error");
    } finally {
        isLoading.value = false;
    }
};

const handleLogout = async () => {
    try {
        await supabase.auth.signOut();
        router.push("/login");
    } catch (err) {
        showMessage("Failed to logout", "error");
    }
};

onMounted(() => {
    requestAnimationFrame(() => (showCard.value = true));
    fetchAccountDetails();
});
</script>

<style scoped>
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

.fade-msg-enter-active,
.fade-msg-leave-active {
    transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-msg-enter-from,
.fade-msg-leave-to {
    opacity: 0;
    transform: translateY(-4px);
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
    transition: all 0.15s ease-in-out;
    font-size: 0.8rem;
    color: #27272a;
}

.chip.selected {
    background-color: #800020;
    color: #fff;
    border-color: #800020;
}

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

