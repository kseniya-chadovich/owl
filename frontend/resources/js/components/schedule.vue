<template>
    <div
        class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50/30 flex flex-col"
    >
        <!-- NAVBAR -->
        <header
            class="w-full border-b border-white/20 bg-white/80 backdrop-blur-xl shadow-sm"
        >
            <div
                class="flex justify-between items-center max-w-6xl mx-auto px-6 py-4"
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
                    @click="navigateTo('/account')"
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
                                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                            />
                        </svg>
                    </div>
                    <span class="font-semibold">Account Information</span>
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
        <main class="flex-1 max-w-6xl mx-auto w-full px-4 py-8">
            <!-- Header Section -->
            <div class="text-center mb-8">
                <h1 class="text-3xl font-bold text-slate-800 mb-3">
                    Your Academic Schedule
                </h1>
                <p class="text-slate-600 max-w-2xl mx-auto">
                    Overview of your current semester courses, credits, and
                    academic progress
                </p>
            </div>

            <!-- MESSAGE BOX -->
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

            <!-- LOADING STATE -->
            <div v-if="isLoading" class="text-center py-12">
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
                    Loading your academic schedule...
                </p>
            </div>

            <!-- NO SCHEDULE STATE -->
            <div v-else-if="!schedule || !schedule.courses || schedule.courses.length === 0" class="text-center py-12">
                <div class="mb-8">
                    <div class="text-5xl mb-4">📚</div>
                    <h3 class="text-xl font-semibold text-slate-800 mb-3">
                        No Schedule Found
                    </h3>
                    <p class="text-slate-500 mb-6 max-w-md mx-auto">
                        You haven't created a schedule yet. Visit the scheduling
                        assistant to build your perfect semester plan.
                    </p>
                </div>
                <button
                    @click="navigateTo('/chat')"
                    class="bg-gradient-to-r from-[#800020] to-[#a83232] text-white px-6 py-3 rounded-xl hover:shadow-lg transition-all duration-300 font-medium flex items-center gap-2 mx-auto"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            d="M2 10a8 8 0 1116 0 8 8 0 01-16 0zm8-6a6 6 0 00-6 6c0 1.887.454 3.665 1.257 5.234a.5.5 0 00.656.254 10.97 10.97 0 013.087-1.227.5.5 0 00-.278-.948 7.98 7.98 0 00-2.564.956.5.5 0 00-.14.843 2.984 2.984 0 002.827 1.795c.784 0 1.512-.261 2.1-.704a3 3 0 01-2.1-.704.5.5 0 00-.14-.843 7.98 7.98 0 00-2.564-.956.5.5 0 00-.278.948 10.97 10.97 0 013.087 1.227.5.5 0 00.656-.254A5.984 5.984 0 0010 4z"
                        />
                    </svg>
                    Create Schedule
                </button>
            </div>

            <!-- SCHEDULE DISPLAY -->
            <div v-else class="space-y-6">
                <!-- QUICK STATS & ACTIONS -->
                <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    <!-- Stats Cards -->
                    <div
                        class="lg:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-4"
                    >
                        <div
                            class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm"
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        class="h-5 w-5 text-blue-600"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                                        />
                                    </svg>
                                </div>
                                <div>
                                    <div
                                        class="text-2xl font-bold text-slate-800"
                                    >
                                        {{ schedule.courses?.length || 0 }}
                                    </div>
                                    <div class="text-sm text-slate-600">
                                        Total Courses
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div
                            class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm"
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        class="h-5 w-5 text-green-600"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                                        />
                                    </svg>
                                </div>
                                <div>
                                    <div
                                        class="text-2xl font-bold text-slate-800"
                                    >
                                        {{ schedule.total_credits || 0 }}
                                    </div>
                                    <div class="text-sm text-slate-600">
                                        Total Credits
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div
                            class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm"
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-10 h-10 bg-purple-50 rounded-lg flex items-center justify-center"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        class="h-5 w-5 text-purple-600"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                                        />
                                    </svg>
                                </div>
                                <div>
                                    <div
                                        class="text-2xl font-bold text-slate-800"
                                    >
                                        {{ getGenEdCount() }}
                                    </div>
                                    <div class="text-sm text-slate-600">
                                        GenEd Courses
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Actions Card -->

                    <div
                        class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm"
                    >
                        <h3 class="font-bold text-slate-800 mb-3">Actions</h3>
                        <div class="flex gap-2">
                            <button
                                @click="navigateTo('/chat')"
                                class="flex-1 bg-slate-50 text-slate-700 px-4 py-2.5 rounded-lg hover:bg-slate-100 transition-all duration-200 flex items-center justify-center gap-2 font-medium text-sm"
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
                                Modify
                            </button>
                            <button
                                @click="downloadSchedule"
                                class="flex-1 bg-slate-50 text-slate-700 px-4 py-2.5 rounded-lg hover:bg-slate-100 transition-all duration-200 flex items-center justify-center gap-2 font-medium text-sm"
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
                                        d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                                    />
                                </svg>
                                Export
                            </button>
                        </div>
                    </div>
                </div>

                <!-- COURSE LIST -->
                <div
                    class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden"
                >
                    <div
                        class="border-b border-slate-200 bg-slate-50/80 px-6 py-4"
                    >
                        <div class="flex items-center justify-between">
                            <h2 class="text-lg font-semibold text-slate-800">
                                Course Schedule
                            </h2>
                            <div
                                class="flex items-center gap-4 text-sm text-slate-600"
                            >
                                <div class="flex items-center gap-2">
                                    <div
                                        class="w-3 h-3 bg-blue-500 rounded-full"
                                    ></div>
                                    <span>Core</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <div
                                        class="w-3 h-3 bg-purple-500 rounded-full"
                                    ></div>
                                    <span>GenEd</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <div
                                        class="w-3 h-3 bg-emerald-500 rounded-full"
                                    ></div>
                                    <span>Elective</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="divide-y divide-slate-200">
                        <div
                            v-for="course in schedule.courses"
                            :key="course.course"
                            class="p-6 hover:bg-slate-50/50 transition-colors duration-150"
                        >
                            <div class="flex items-start gap-4">
                                <div
                                    class="w-3 h-12 rounded-full mt-1 flex-shrink-0"
                                    :class="getCourseTypeColor(course)"
                                ></div>

                                <div class="flex-1 min-w-0">
                                    <div
                                        class="flex items-start justify-between mb-3"
                                    >
                                        <div>
                                            <h3
                                                class="font-semibold text-slate-800 text-lg mb-1"
                                            >
                                                {{ course.course }}
                                            </h3>
                                            <p
                                                class="text-slate-600 text-sm mb-2"
                                            >
                                                {{
                                                    course.category ||
                                                    "General Course"
                                                }}
                                                <span
                                                    v-if="course.gened_type"
                                                    class="text-purple-600 font-medium"
                                                    >•
                                                    {{
                                                        course.gened_type
                                                    }}</span
                                                >
                                            </p>
                                        </div>
                                        <div class="flex gap-2 ml-4">
                                            <span
                                                class="bg-slate-100 text-slate-700 px-2.5 py-1 rounded-full text-sm font-medium"
                                            >
                                                {{ course.credits }} credit{{
                                                    course.credits !== 1
                                                        ? "s"
                                                        : ""
                                                }}
                                            </span>
                                        </div>
                                    </div>

                                    <div
                                        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm"
                                    >
                                        <div
                                            class="flex items-center gap-2 text-slate-600"
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                class="h-4 w-4 text-slate-500"
                                                fill="none"
                                                viewBox="0 0 24 24"
                                                stroke="currentColor"
                                            >
                                                <path
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    stroke-width="2"
                                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                                                />
                                            </svg>
                                            <span class="font-medium">{{
                                                course.day_time ||
                                                "Schedule TBD"
                                            }}</span>
                                        </div>
                                        <div
                                            class="flex items-center gap-2 text-slate-600"
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                class="h-4 w-4 text-slate-500"
                                                fill="none"
                                                viewBox="0 0 24 24"
                                                stroke="currentColor"
                                            >
                                                <path
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    stroke-width="2"
                                                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                                                />
                                            </svg>
                                            <span>{{
                                                course.instructor ||
                                                "Instructor TBA"
                                            }}</span>
                                        </div>
                                        <div
                                            class="flex items-center gap-2 text-slate-600"
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                class="h-4 w-4 text-slate-500"
                                                fill="none"
                                                viewBox="0 0 24 24"
                                                stroke="currentColor"
                                            >
                                                <path
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    stroke-width="2"
                                                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                                                />
                                            </svg>
                                            <span>Room TBA</span>
                                        </div>
                                        <div
                                            class="flex items-center gap-2 text-slate-600"
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                class="h-4 w-4 text-slate-500"
                                                fill="none"
                                                viewBox="0 0 24 24"
                                                stroke="currentColor"
                                            >
                                                <path
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    stroke-width="2"
                                                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                                                />
                                            </svg>
                                            <span>Enrolled</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- SCHEDULE SUMMARY -->
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { supabase } from "../supabase";

const router = useRouter();
const DATA_URL = "https://supabase-kqbi.onrender.com";

const sidebarOpen = ref(false);
const schedule = ref(null);
const isLoading = ref(true);
const user = ref(null);

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

const getGenEdCount = () => {
    if (!schedule.value?.courses) return 0;
    return schedule.value.courses.filter((course) => course.gened_type).length;
};

const getCourseTypeColor = (course) => {
    if (course.gened_type) return "bg-purple-500";
    if (course.category?.toLowerCase().includes("elective"))
        return "bg-emerald-500";
    return "bg-blue-500";
};

const downloadSchedule = () => {
    if (!schedule.value) return;

    const scheduleText =
        `Course Schedule\n\n` +
        schedule.value.courses
            .map(
                (course) =>
                    `${course.course} | ${course.day_time || "TBD"} | ${
                        course.credits
                    }cr | ${course.category}` +
                    (course.gened_type
                        ? ` | GenEd: ${course.gened_type}`
                        : "") +
                    (course.instructor ? ` | Prof: ${course.instructor}` : "")
            )
            .join("\n") +
        `\n\nTotal Credits: ${schedule.value.total_credits}`;

    const blob = new Blob([scheduleText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "my-schedule.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showMessage("Schedule exported successfully!", "success");
};

const navigateTo = (route) => {
    sidebarOpen.value = false;
    router.push(route);
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

onMounted(async () => {
    const { data } = await supabase.auth.getUser();
    user.value = data?.user;

    if (!user.value) {
        isLoading.value = false;
        return;
    }

    try {
        const resp = await axios.get(
            `${DATA_URL}/students/schedules/${user.value.id}`
        );
        schedule.value = resp.data.schedule;
    } catch (err) {
        console.log("No schedule found or error:", err);
        schedule.value = null;
    }

    isLoading.value = false;
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
