<template>
    <div
        class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50/30 flex flex-col"
    >
        <!-- NAVBAR -->
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

                <button
                    @click="sidebarOpen = true"
                    class="p-2 rounded-xl bg-white border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 hover:scale-105"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-6 w-6 text-slate-700"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M4 6h16M4 12h16M4 18h16"
                        />
                    </svg>
                </button>
            </div>
        </header>

        <!-- SIDEBAR OVERLAY -->
        <div
            v-if="sidebarOpen"
            @click="sidebarOpen = false"
            class="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 transition-opacity duration-300"
        ></div>

        <!-- MODERN SIDEBAR -->
        <div
            class="fixed top-0 right-0 h-full w-80 bg-white/95 backdrop-blur-xl shadow-2xl z-50 transform transition-transform duration-500 ease-out"
            :class="sidebarOpen ? 'translate-x-0' : 'translate-x-full'"
        >
            <div class="p-6 border-b border-slate-100">
                <div class="flex items-center justify-between">
                    <h2
                        class="text-xl font-bold bg-gradient-to-r from-[#800020] to-[#a83232] bg-clip-text text-transparent"
                    >
                        Navigation
                    </h2>
                    <button
                        @click="sidebarOpen = false"
                        class="p-2 rounded-lg hover:bg-slate-100 transition-colors"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5 text-slate-600"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M6 18L18 6M6 6l12 12"
                            />
                        </svg>
                    </button>
                </div>
            </div>

            <div class="p-6 space-y-3">
                <button
                    @click="navigateTo('/schedule')"
                    class="w-full flex items-center gap-4 p-4 rounded-2xl bg-white border border-slate-200 text-slate-700 shadow-sm hover:shadow-md transition-all duration-300 hover:scale-[1.02] hover:border-[#800020]/20"
                >
                    <div class="p-2 bg-[#800020]/10 rounded-xl">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5 text-[#800020]"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                            />
                        </svg>
                    </div>
                    <span class="font-semibold">Current Schedule</span>
                </button>

                <button
                    @click="navigateTo('/chat')"
                    class="w-full flex items-center gap-4 p-4 rounded-2xl bg-white border border-slate-200 text-slate-700 shadow-sm hover:shadow-md transition-all duration-300 hover:scale-[1.02] hover:border-[#800020]/20"
                >
                    <div class="p-2 bg-[#800020]/10 rounded-xl">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5 text-[#800020]"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                            />
                        </svg>
                    </div>
                    <span class="font-semibold">Scheduling Assistant</span>
                </button>

                <div class="pt-6 border-t border-slate-100">
                    <button
                        @click="handleLogout"
                        class="w-full flex items-center gap-4 p-4 rounded-2xl bg-slate-50 text-slate-600 hover:bg-slate-100 transition-all duration-300"
                    >
                        <div class="p-2 bg-slate-200 rounded-xl">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="h-5 w-5"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                                />
                            </svg>
                        </div>
                        <span class="font-semibold">Logout</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- MAIN CONTENT -->
        <main class="flex-1 w-full px-4 py-8">
            <!-- Header Section -->
            <div class="text-center mb-8 max-w-6xl mx-auto">
                <h1 class="text-3xl font-bold text-slate-800 mb-3">
                    Account Details
                </h1>
                <p class="text-slate-600">
                    Your personal and academic information
                </p>
            </div>

            <!-- MESSAGE BOX -->
            <transition name="fade-msg">
                <div
                    v-if="message.visible"
                    :class="[
                        'mb-6 flex items-center justify-between px-4 py-3 rounded-xl border shadow-sm text-sm max-w-6xl mx-auto',
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

            <!-- LOADING STATE -->
            <div v-if="isLoading" class="text-center py-12 max-w-6xl mx-auto">
                <div class="flex justify-center mb-4">
                    <div
                        class="w-12 h-12 bg-gradient-to-br from-[#800020] to-[#a83232] rounded-xl flex items-center justify-center"
                    >
                        <div
                            class="animate-spin rounded-full h-6 w-6 border-2 border-white border-t-transparent"
                        ></div>
                    </div>
                </div>
                <p class="text-slate-600 font-medium">
                    Loading account details...
                </p>
            </div>

            <!-- ERROR STATE -->
            <div v-else-if="error" class="text-center py-8 max-w-6xl mx-auto">
                <p class="text-red-600 mb-4">{{ error }}</p>
                <button
                    @click="fetchAccountDetails"
                    class="border border-[#800020]/80 bg-transparent text-[#800020] font-medium px-4 py-2 rounded-lg text-sm hover:bg-[#800020] hover:text-white transition"
                >
                    Try Again
                </button>
            </div>

            <!-- ACCOUNT CONTENT -->
            <div v-else-if="studentData" class="space-y-6 max-w-6xl mx-auto">
                <!-- PROFILE HEADER -->
                <div
                    class="bg-white rounded-2xl border border-slate-200 shadow-lg p-8"
                >
                    <div class="flex flex-col md:flex-row items-center gap-8">
                        <!-- Profile Picture -->
                        <div class="relative">
                            <img
                                :src="
                                    previewImage ||
                                    studentData.personal?.profile_picture ||
                                    defaultProfile
                                "
                                class="w-32 h-32 rounded-full object-cover border-4 border-[#800020]/20 shadow-lg"
                            />
                            <input
                                ref="fileInput"
                                type="file"
                                accept="image/*"
                                class="hidden"
                                @change="handleImageUpload"
                            />
                            <button
                                v-if="isEditing"
                                @click="$refs.fileInput.click()"
                                class="absolute -bottom-2 -right-2 bg-[#800020] text-white p-3 rounded-full shadow-lg hover:bg-[#6a001a] transition-all duration-200 hover:scale-110"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-5 w-5"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                                    />
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
                                    />
                                </svg>
                            </button>
                        </div>

                        <!-- Profile Info -->
                        <div class="flex-1 text-center md:text-left">
                            <h2 class="text-3xl font-bold text-slate-800 mb-3">
                                {{
                                    studentData.personal?.full_name ||
                                    "No Name Provided"
                                }}
                            </h2>
                            <p class="text-slate-600 mb-6 text-lg">
                                {{ authData?.email }}
                            </p>

                            <div
                                class="flex flex-wrap gap-3 justify-center md:justify-start"
                            >
                                <span
                                    class="bg-[#800020]/10 text-[#800020] px-4 py-2 rounded-full text-sm font-semibold border border-[#800020]/20"
                                >
                                    Semester
                                    {{
                                        studentData.academic
                                            ?.current_semester || "N/A"
                                    }}
                                </span>
                                <span
                                    v-if="
                                        studentData.personal?.is_international
                                    "
                                    class="bg-[#800020]/10 text-[#800020] px-4 py-2 rounded-full text-sm font-semibold border border-[#800020]/20"
                                >
                                    International Student
                                </span>
                                <span
                                    v-if="studentData.personal?.age"
                                    class="bg-[#800020]/10 text-[#800020] px-4 py-2 rounded-full text-sm font-semibold border border-[#800020]/20"
                                >
                                    Age {{ studentData.personal.age }}
                                </span>
                            </div>
                        </div>

                        <!-- Edit Button -->
                        <div class="flex gap-3">
                            <button
                                v-if="!isEditing"
                                @click="enableEditing"
                                class="border border-[#800020]/80 bg-transparent text-[#800020] font-medium px-6 py-3 rounded-lg hover:bg-[#800020] hover:text-white transition flex items-center gap-2"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-4 w-4"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                                    />
                                </svg>
                                Edit Profile
                            </button>

                            <div v-else class="flex gap-3">
                                <button
                                    @click="saveChanges"
                                    class="border border-[#800020]/80 bg-transparent text-[#800020] font-medium px-6 py-3 rounded-lg hover:bg-[#800020] hover:text-white transition flex items-center gap-2"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        class="h-4 w-4"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M5 13l4 4L19 7"
                                        />
                                    </svg>
                                    Save Changes
                                </button>
                                <button
                                    @click="cancelEditing"
                                    class="border border-slate-400 bg-transparent text-slate-600 font-medium px-6 py-3 rounded-lg hover:bg-slate-400 hover:text-white transition"
                                >
                                    Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- PERSONAL INFORMATION -->
                <div
                    class="bg-white rounded-2xl border border-slate-200 shadow-lg overflow-hidden"
                >
                    <div
                        class="border-b border-slate-200 bg-slate-50/80 px-6 py-4"
                    >
                        <h2 class="text-lg font-semibold text-slate-800">
                            Personal Information
                        </h2>
                    </div>
                    <div class="p-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label
                                    class="block text-sm font-medium text-slate-600 mb-2"
                                    >Full Name</label
                                >
                                <div
                                    v-if="!isEditing"
                                    class="text-slate-900 font-medium p-3 bg-slate-50 rounded-lg"
                                >
                                    {{
                                        studentData.personal?.full_name ||
                                        "Not provided"
                                    }}
                                </div>
                                <input
                                    v-else
                                    v-model="editData.full_name"
                                    class="w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#800020] focus:border-transparent"
                                />
                            </div>

                            <div>
                                <label
                                    class="block text-sm font-medium text-slate-600 mb-2"
                                    >Age</label
                                >
                                <div
                                    v-if="!isEditing"
                                    class="text-slate-900 font-medium p-3 bg-slate-50 rounded-lg"
                                >
                                    {{
                                        studentData.personal?.age ||
                                        "Not provided"
                                    }}
                                </div>
                                <input
                                    v-else
                                    v-model.number="editData.age"
                                    type="number"
                                    min="0"
                                    class="w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#800020] focus:border-transparent"
                                />
                            </div>

                            <div>
                                <label
                                    class="block text-sm font-medium text-slate-600 mb-2"
                                    >International Student</label
                                >
                                <div
                                    v-if="!isEditing"
                                    class="text-slate-900 font-medium p-3 bg-slate-50 rounded-lg"
                                >
                                    {{
                                        studentData.personal?.is_international
                                            ? "Yes"
                                            : "No"
                                    }}
                                </div>
                                <select
                                    v-else
                                    v-model="editData.is_international"
                                    class="w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#800020] focus:border-transparent"
                                >
                                    <option :value="true">Yes</option>
                                    <option :value="false">No</option>
                                </select>
                            </div>

                            <div>
                                <label
                                    class="block text-sm font-medium text-slate-600 mb-2"
                                    >Current Semester</label
                                >
                                <div
                                    v-if="!isEditing"
                                    class="text-slate-900 font-medium p-3 bg-slate-50 rounded-lg"
                                >
                                    {{
                                        studentData.academic
                                            ?.current_semester || "Not provided"
                                    }}
                                </div>
                                <input
                                    v-else
                                    v-model.number="editData.current_semester"
                                    type="number"
                                    min="1"
                                    class="w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#800020] focus:border-transparent"
                                />
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ACADEMIC INFORMATION -->
                <div
                    class="bg-white rounded-2xl border border-slate-200 shadow-lg overflow-hidden"
                >
                    <div
                        class="border-b border-slate-200 bg-slate-50/80 px-6 py-4"
                    >
                        <h2 class="text-lg font-semibold text-slate-800">
                            Academic Information
                        </h2>
                    </div>
                    <div class="p-6 space-y-6">
                        <!-- Taken Courses -->
                        <div>
                            <label
                                class="block text-sm font-medium text-slate-600 mb-3"
                                >Taken Courses</label
                            >
                            <div v-if="!isEditing">
                                <div
                                    v-if="
                                        studentData.academic?.taken_courses
                                            ?.length
                                    "
                                    class="flex flex-wrap gap-2"
                                >
                                    <div
                                        v-for="course in studentData.academic
                                            .taken_courses"
                                        :key="course"
                                        class="bg-[#800020]/10 text-[#800020] px-3 py-2 rounded-lg text-sm font-medium border border-[#800020]/20"
                                    >
                                        {{ course }}
                                    </div>
                                </div>
                                <p
                                    v-else
                                    class="text-slate-500 italic p-3 bg-slate-50 rounded-lg"
                                >
                                    No courses recorded
                                </p>
                            </div>
                            <textarea
                                v-else
                                v-model="editData.taken_courses_string"
                                class="w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#800020] focus:border-transparent"
                                placeholder="CIS1001, MATH1041, ..."
                                rows="3"
                            ></textarea>
                        </div>

                        <!-- Taken GenEds -->
                        <div>
                            <label
                                class="block text-sm font-medium text-slate-600 mb-3"
                                >Taken GenEds</label
                            >
                            <div v-if="!isEditing">
                                <div
                                    v-if="
                                        studentData.academic?.taken_geneds
                                            ?.length
                                    "
                                    class="flex flex-wrap gap-2"
                                >
                                    <div
                                        v-for="gen in studentData.academic
                                            .taken_geneds"
                                        :key="gen"
                                        class="bg-[#800020]/10 text-[#800020] px-3 py-2 rounded-lg text-sm font-medium border border-[#800020]/20"
                                    >
                                        {{ gen }}
                                    </div>
                                </div>
                                <p
                                    v-else
                                    class="text-slate-500 italic p-3 bg-slate-50 rounded-lg"
                                >
                                    No GenEds recorded
                                </p>
                            </div>
                            <textarea
                                v-else
                                v-model="editData.taken_geneds_string"
                                class="w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#800020] focus:border-transparent"
                                placeholder="GA, GB, GD, ..."
                                rows="3"
                            ></textarea>
                        </div>
                    </div>
                </div>

                <!-- ACCOUNT INFORMATION -->
                <div
                    class="bg-white rounded-2xl border border-slate-200 shadow-lg overflow-hidden"
                >
                    <div
                        class="border-b border-slate-200 bg-slate-50/80 px-6 py-4"
                    >
                        <h2 class="text-lg font-semibold text-slate-800">
                            Account Information
                        </h2>
                    </div>
                    <div class="p-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label
                                    class="block text-sm font-medium text-slate-600 mb-2"
                                    >Email</label
                                >
                                <div
                                    class="text-slate-900 font-medium p-3 bg-slate-50 rounded-lg"
                                >
                                    {{ authData?.email || "Not available" }}
                                </div>
                            </div>
                            <div>
                                <label
                                    class="block text-sm font-medium text-slate-600 mb-2"
                                    >Email Verified</label
                                >
                                <div
                                    class="text-slate-900 font-medium p-3 bg-slate-50 rounded-lg"
                                >
                                    {{
                                        authData?.email_confirmed_at
                                            ? "Yes"
                                            : "No"
                                    }}
                                </div>
                            </div>
                            <div>
                                <label
                                    class="block text-sm font-medium text-slate-600 mb-2"
                                    >Account Created</label
                                >
                                <div
                                    class="text-slate-900 font-medium p-3 bg-slate-50 rounded-lg"
                                >
                                    {{ formatDate(authData?.created_at) }}
                                </div>
                            </div>
                            <div>
                                <label
                                    class="block text-sm font-medium text-slate-600 mb-2"
                                    >Last Sign In</label
                                >
                                <div
                                    class="text-slate-900 font-medium p-3 bg-slate-50 rounded-lg"
                                >
                                    {{ formatDate(authData?.last_sign_in_at) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- NO DATA STATE -->
            <div v-else class="text-center py-12 max-w-6xl mx-auto">
                <div class="mb-8">
                    <div class="text-5xl mb-4">👤</div>
                    <h3 class="text-xl font-semibold text-slate-800 mb-3">
                        No Account Data Found
                    </h3>
                    <p class="text-slate-500 mb-6">
                        We couldn't find your account information. Please try
                        refreshing the page.
                    </p>
                </div>
                <button
                    @click="fetchAccountDetails"
                    class="border border-[#800020]/80 bg-transparent text-[#800020] font-medium px-6 py-3 rounded-lg hover:bg-[#800020] hover:text-white transition"
                >
                    Retry Fetch
                </button>
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
const DATA_URL = "https://supabase-kqbi.onrender.com";

const isLoading = ref(false);
const studentData = ref(null);
const authData = ref(null);
const error = ref("");
const isEditing = ref(false);
const fileInput = ref(null);
const previewImage = ref(null);
const selectedFile = ref(null);

const defaultProfile = "https://placehold.co/200x200?text=No+Image";

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

const enableEditing = () => {
    isEditing.value = true;
    editData.value = {
        full_name: studentData.value.personal?.full_name || "",
        age: studentData.value.personal?.age || "",
        is_international: studentData.value.personal?.is_international || false,
        current_semester: studentData.value.academic?.current_semester || "",
        taken_courses: [...(studentData.value.academic?.taken_courses || [])],
        taken_geneds: [...(studentData.value.academic?.taken_geneds || [])],
        taken_courses_string: (
            studentData.value.academic?.taken_courses || []
        ).join(", "),
        taken_geneds_string: (
            studentData.value.academic?.taken_geneds || []
        ).join(", "),
    };
};

const cancelEditing = () => {
    isEditing.value = false;
    selectedFile.value = null;
    previewImage.value = null;
};

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

const saveChanges = async () => {
    try {
        isLoading.value = true;
        const user = (await supabase.auth.getUser()).data.user;

        let imageUrl = studentData.value.personal?.profile_picture;

        if (selectedFile.value) {
            const ext = selectedFile.value.name.split(".").pop();
            const fileName = `${user.id}.${ext}`;

            const { data: existingFiles } = await supabase.storage
                .from("avatars")
                .list("", { search: fileName });

            const fileExists = existingFiles?.some((f) => f.name === fileName);
            let uploadResult;

            if (fileExists) {
                uploadResult = await supabase.storage
                    .from("avatars")
                    .update(fileName, selectedFile.value);
            } else {
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

        showMessage("Account updated successfully!", "success");
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
        error.value = "";

        const {
            data: { user },
        } = await supabase.auth.getUser();
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

const navigateTo = (route) => {
    sidebarOpen.value = false;
    router.push(route);
};

const handleLogout = async () => {
    try {
        await supabase.auth.signOut();
        router.push("/login");
    } catch (err) {
        showMessage("Failed to logout", "error");
    }
};

const sidebarOpen = ref(false);

onMounted(() => {
    fetchAccountDetails();
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
</style>
