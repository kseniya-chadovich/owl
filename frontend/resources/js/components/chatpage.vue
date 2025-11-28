<template>
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

    <div
        v-if="sidebarOpen"
        @click="sidebarOpen = false"
        class="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 transition-opacity duration-300"
    ></div>

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
                            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                        />
                    </svg>
                </div>
                <span class="font-semibold">Current Schedule</span>
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

    <div
        class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50/30 flex flex-col items-center pt-4 pb-8 px-4"
    >
        <div class="text-center mb-6">
            <h1 class="text-3xl md:text-4xl font-bold text-slate-800 mb-3">
                Chat with Your Scheduling Assistant
            </h1>
            <p class="text-slate-500 text-base max-w-1xl mx-auto">
                Describe your preferences and let's build
                your perfect semester schedule.
            </p>
        </div>

        <div v-if="isInitializing" class="py-12 text-center text-slate-600">
            <div class="flex justify-center mb-3">
                <div
                    class="w-12 h-12 bg-gradient-to-br from-[#800020] to-[#a83232] rounded-xl flex items-center justify-center"
                >
                    <div
                        class="animate-spin rounded-full h-6 w-6 border-2 border-white border-t-transparent"
                    ></div>
                </div>
            </div>
            <p class="text-base font-medium">Loading your chat session...</p>
        </div>

        <div
            v-else
            class="w-full max-w-6xl bg-white rounded-2xl shadow-sm flex flex-col overflow-hidden"
            style="height: 70vh; margin-top: 0"
        >
            <div
                v-if="errorMessage"
                class="mx-4 mt-3 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700 flex items-center gap-2"
            >
                <div
                    class="w-5 h-5 bg-red-100 rounded-full flex items-center justify-center"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-3 w-3 text-red-600"
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
                </div>
                {{ errorMessage }}
            </div>

            <div
                ref="messagesContainer"
                class="flex-1 p-5 space-y-4 overflow-y-auto"
                style="max-height: calc(75vh - 160px)"
            >
                <div
                    v-for="message in messages"
                    :key="message.id"
                    class="flex items-start gap-3"
                    :class="message.role === 'user' ? 'justify-end' : ''"
                >
                    <div
                        v-if="message.role === 'assistant'"
                        class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-[#800020] to-[#a83232] text-white font-semibold shrink-0 shadow-sm text-sm"
                    >
                        AI
                    </div>

                    <div
                        v-else
                        class="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-100 text-slate-700 font-semibold shrink-0 shadow-sm order-last text-sm"
                    >
                        You
                    </div>

                    <div
                        v-if="!message.schedules"
                        class="max-w-[80%] whitespace-pre-wrap rounded-xl px-4 py-3 leading-relaxed shadow-sm"
                        :class="
                            message.role === 'assistant'
                                ? 'bg-white text-slate-800 rounded-tl-none text-sm'
                                : 'bg-gradient-to-r from-[#800020] to-[#a83232] text-white rounded-tr-none text-sm'
                        "
                    >
                        <p class="font-medium">{{ message.text }}</p>

                        <div
                            v-if="message.confirmOptions"
                            class="flex gap-2 mt-3"
                        >
                            <button
                                v-for="opt in message.confirmOptions"
                                :key="opt"
                                @click="handleConfirmOption(opt)"
                                class="px-3 py-2 text-sm rounded-lg bg-white text-slate-700 hover:bg-slate-50 transition-all duration-200 font-medium shadow-sm"
                            >
                                {{ opt }}
                            </button>
                        </div>
                    </div>

                    <div v-else class="flex flex-col gap-3 max-w-[60%] w-full">
                        <div
                            v-for="(schedule, index) in message.schedules"
                            :key="index"
                            @click="handleSelectSchedule(index, message)"
                            class="rounded-xl p-4 transition-all duration-300 cursor-pointer bg-white hover:shadow-md relative"
                            :class="[
                                selectedScheduleIndex === index &&
                                message.id === selectedMessageId
                                    ? 'ring-2 ring-[#800020] ring-opacity-30 bg-[#800020]/5'
                                    : 'shadow-sm',
                            ]"
                        >
                            <div class="flex justify-between items-center mb-3">
                                <div class="flex items-center gap-2">
                                    <h3
                                        class="font-bold text-slate-800 text-sm"
                                    >
                                        Schedule {{ index + 1 }}
                                    </h3>
                                    <span
                                        class="inline-flex items-center rounded-full bg-[#800020]/10 text-[#800020] text-xs px-2 py-1 font-medium"
                                    >
                                        {{ schedule.courses.length }} courses
                                    </span>
                                </div>

                                <span
                                    v-if="
                                        selectedScheduleIndex === index &&
                                        message.id === selectedMessageId
                                    "
                                    class="inline-flex items-center text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-1 rounded-full"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        class="h-3 w-3 mr-1"
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
                                    Selected
                                </span>
                            </div>

                            <div class="space-y-2">
                                <div
                                    v-for="course in schedule.courses"
                                    :key="course.course"
                                    class="flex items-center justify-between p-2 bg-slate-50 rounded-lg"
                                >
                                    <div class="flex-1 min-w-0">
                                        <div
                                            class="flex items-center gap-2 mb-1"
                                        >
                                            <h4
                                                class="font-semibold text-slate-800 text-sm truncate"
                                            >
                                                {{ course.course }}
                                            </h4>
                                            <div
                                                class="flex gap-1 flex-shrink-0"
                                            >
                                                <span
                                                    v-if="course.category"
                                                    class="inline-flex items-center px-2 py-1 rounded-full bg-[#800020]/10 text-[#800020] text-xs font-medium"
                                                    >{{ course.category }}</span
                                                >
                                                <span
                                                    v-if="course.gened_type"
                                                    class="inline-flex items-center px-2 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-medium"
                                                    >{{
                                                        course.gened_type
                                                    }}</span
                                                >
                                            </div>
                                        </div>

                                        <div
                                            class="flex items-center gap-3 text-sm text-slate-600"
                                        >
                                            <span
                                                class="flex items-center gap-1"
                                            >
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    class="h-3 w-3"
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
                                                {{ course.day_time || "TBD" }}
                                            </span>
                                            <span
                                                class="flex items-center gap-1"
                                                v-if="course.instructor"
                                            >
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    class="h-3 w-3"
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
                                                {{ course.instructor }}
                                            </span>
                                        </div>
                                    </div>

                                    <div
                                        class="flex items-center gap-2 ml-3 flex-shrink-0"
                                    >
                                        <span
                                            class="bg-white text-slate-700 px-2 py-1 rounded-full text-sm font-semibold shadow-sm"
                                            >{{ course.credits }} cr</span
                                        >
                                    </div>
                                </div>
                            </div>

                            <div
                                class="mt-3 flex justify-between items-center text-sm text-slate-600"
                            >
                                <p class="font-semibold text-slate-800">
                                    Total:
                                    {{
                                        schedule.total_credits ?? "n/a"
                                    }}
                                    credits
                                </p>
                                <p class="text-slate-500 text-sm">
                                    Click to select
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="isLoading" class="flex items-start gap-3">
                    <div
                        class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-[#800020] to-[#a83232] text-white font-semibold shadow-sm text-sm"
                    >
                        AI
                    </div>
                    <div
                        class="bg-white rounded-xl rounded-tl-none px-4 py-3 shadow-sm"
                    >
                        <div class="flex items-center gap-2 text-slate-600">
                            <div class="flex space-x-1">
                                <div
                                    class="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                                    style="animation-delay: 0.1s"
                                ></div>
                                <div
                                    class="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                                    style="animation-delay: 0.2s"
                                ></div>
                                <div
                                    class="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                                    style="animation-delay: 0.3s"
                                ></div>
                            </div>
                            <span class="text-sm font-medium">Thinking...</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bg-slate-50/80 p-4">
                <div class="flex items-end gap-3">
                    <textarea
                        ref="textareaRef"
                        placeholder="Describe your ideal semester schedule..."
                        v-model="draftMessage"
                        @input="autoResize"
                        @keydown.enter.exact.prevent="sendMessage"
                        rows="1"
                        class="flex-1 resize-none rounded-xl bg-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 text-slate-700 placeholder-slate-500 font-medium transition-all duration-200 text-sm shadow-sm"
                        :disabled="isLoading"
                        style="max-height: 100px; min-height: 48px"
                    ></textarea>

                    <button
                        @click="resetConversation"
                        :disabled="isLoading"
                        class="bg-white hover:bg-slate-50 text-slate-700 p-3 rounded-xl transition-all duration-200 flex items-center justify-center shadow-sm hover:shadow-md flex-shrink-0"
                        title="Reset session"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            class="w-4 h-4"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M4 4v6h6M20 20v-6h-6M4 10a8 8 0 0116 0m0 4a8 8 0 01-16 0"
                            />
                        </svg>
                    </button>

                    <button
                        @click="sendMessage"
                        :disabled="isLoading || !draftMessage.trim()"
                        class="bg-gradient-to-r from-[#800020] to-[#a83232] hover:from-[#700018] hover:to-[#982b2b] text-white p-3 rounded-xl transition-all duration-200 flex items-center justify-center shadow-sm hover:shadow-md font-medium flex-shrink-0"
                        :class="
                            isLoading || !draftMessage.trim()
                                ? 'opacity-50 cursor-not-allowed'
                                : 'hover:scale-105'
                        "
                        title="Send"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            class="w-4 h-4"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
                            />
                        </svg>
                    </button>
                </div>

                <div class="mt-3 flex flex-wrap gap-2">
                    <button
                        v-for="suggestion in suggestions"
                        :key="suggestion"
                        class="text-sm bg-white px-3 py-2 rounded-lg text-slate-700 hover:bg-slate-50 transition-all duration-200 font-medium shadow-sm"
                        @click="applySuggestion(suggestion)"
                        :disabled="isLoading"
                    >
                        {{ suggestion }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { supabase } from "../supabase";

const router = useRouter();
const AI_URL = "https://scheduling-assistant-zl2c.onrender.com";
const DATA_URL = "https://supabase-kqbi.onrender.com";

const user = ref(null);
const messages = ref([]);
const draftMessage = ref("");
const isLoading = ref(false);
const sidebarOpen = ref(false);
const messagesContainer = ref(null);
const isInitializing = ref(true);
const selectedScheduleIndex = ref(null);
const selectedMessageId = ref(null);
const confirmMessageId = ref(null);
const suggestions = [
    "No morning classes",
    "Only 12 credits",
    "I prefer T/Th classes",
    "Avoid online courses",
];
const textareaRef = ref(null);

let messageCounter = 0;
const newId = () => `msg-${messageCounter++}`;
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const stripSection = (courseName) =>
    courseName.replace(/\s*\(\d+\)\s*$/, "").trim();

const scrollToBottom = async () => {
    await nextTick();
    if (messagesContainer.value)
        messagesContainer.value.scrollTop =
            messagesContainer.value.scrollHeight;
};

watch(() => messages.value.length, scrollToBottom, { flush: "post" });
watch(
    () => isLoading.value,
    () => !isLoading.value && scrollToBottom()
);

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
    }
};

const loadUser = async () => {
    const { data } = await supabase.auth.getUser();
    user.value = data?.user;

    if (!user.value) {
        isInitializing.value = false;
        return;
    }

    const resp = await axios.get(
        `${DATA_URL}/students/conversation/${user.value.id}`
    );
    const stored = resp.data?.conversation || [];

    if (!stored.length) {
        messages.value = [
            {
                id: newId(),
                role: "assistant",
                text: "Hi! I'm your scheduling assistant. I can help you build the perfect semester schedule based on your preferences and academic requirements.",
            },
        ];
        isInitializing.value = false;
        await scrollToBottom();
        return;
    }

    messages.value = stored.map((t) => {
        try {
            if (t.startsWith("{") && t.includes("schedules")) {
                const parsed = JSON.parse(t);
                return {
                    id: newId(),
                    role: "assistant",
                    text: "Here are your schedules:",
                    schedules: parsed.schedules,
                };
            }
        } catch {}

        if (t.startsWith("User:"))
            return { id: newId(), role: "user", text: t.replace("User: ", "") };
        return { id: newId(), role: "assistant", text: t };
    });

    isInitializing.value = false;
    await scrollToBottom();
};

onMounted(loadUser);

const saveConversation = async () => {
    if (!user.value) return;
    const lines = messages.value.map((m) =>
        m.schedules
            ? JSON.stringify({ schedules: m.schedules })
            : m.role === "user"
            ? `User: ${m.text}`
            : m.text
    );
    await axios.post(`${DATA_URL}/students/conversation`, {
        user_id: user.value.id,
        conversation: lines,
    });
};

const sendMessage = async () => {
    if (!draftMessage.value.trim() || !user.value) return;

    const text = draftMessage.value;
    draftMessage.value = "";
    messages.value.push({ id: newId(), role: "user", text });

    if (confirmMessageId.value) {
        const idx = messages.value.findIndex(
            (m) => m.id === confirmMessageId.value
        );
        if (idx !== -1) messages.value.splice(idx, 1);
        confirmMessageId.value = null;
    }

    isLoading.value = true;

    try {
        const academicResp = await axios.get(
            `${DATA_URL}/students/${user.value.id}`
        );
        const academic = academicResp.data.academic || {
            taken_courses: [],
            taken_geneds: [],
            current_semester: 1,
        };

        const { data } = await axios.post(`${AI_URL}/dialog`, {
            user_id: user.value.id,
            message: text,
            academic,
        });

        if (Array.isArray(data.schedules)) {
            messages.value.push({
                id: newId(),
                role: "assistant",
                text: "Here are your schedules:",
                schedules: data.schedules,
            });
            confirmMessageId.value = null;
        } else {
            messages.value.push({
                id: newId(),
                role: "assistant",
                text: data.payload ? "Updated your preferences!" : "Okay!",
            });
        }

        await saveConversation();
    } finally {
        isLoading.value = false;
    }
};

const handleSelectSchedule = (index, message) => {
    selectedScheduleIndex.value = index;
    selectedMessageId.value = message.id;
    const n = index + 1;

    if (!confirmMessageId.value) {
        const msgId = newId();
        confirmMessageId.value = msgId;
        messages.value.push({
            id: msgId,
            role: "assistant",
            text: `You're looking at Schedule ${n}. Do you want to confirm it or add more requirements?`,
            confirmOptions: ["Confirm", "Add more requirements"],
        });
    } else {
        const msg = messages.value.find((m) => m.id === confirmMessageId.value);
        if (msg)
            msg.text = `You're looking at Schedule ${n}. Do you want to confirm it or add more requirements?`;
    }
};

const handleConfirmOption = async (option) => {
    const schedMsg = messages.value.find(
        (m) => m.id === selectedMessageId.value
    );
    const selected = schedMsg.schedules[selectedScheduleIndex.value];

    if (option === "Confirm") {
        const scheduleTextLines = selected.courses
            .map(
                (c) =>
                    `${stripSection(c.course)} | ${c.day_time || "TBD"} | ${
                        c.credits
                    }cr | ${c.category}${
                        c.gened_type ? " | GenEd: " + c.gened_type : ""
                    }${c.instructor ? " | Prof: " + c.instructor : ""}`
            )
            .join("\n");
        messages.value.push({
            id: newId(),
            role: "user",
            text: `I confirm this schedule:\n${scheduleTextLines}`,
        });

        await axios.post(`${DATA_URL}/students/schedules`, {
            user_id: user.value.id,
            schedule: selected,
        });

        const academicResp = await axios.get(
            `${DATA_URL}/students/${user.value.id}`
        );
        const academic = academicResp.data.academic;
        const newCourses = selected.courses.map((c) => stripSection(c.course));
        const newGeneds = selected.courses
            .map((c) => c.gened_type)
            .filter((g) => g && g.length > 0);
        const updatedCourses = Array.from(
            new Set([...academic.taken_courses, ...newCourses])
        );
        const updatedGeneds = Array.from(
            new Set([...academic.taken_geneds, ...newGeneds])
        );
        const updatedSemester = Math.min(
            8,
            Number(academic.current_semester) + 1
        );

        await axios.post(`${DATA_URL}/register-student`, {
            personal: academicResp.data.personal,
            academic: {
                user_id: user.value.id,
                current_semester: updatedSemester,
                taken_courses: updatedCourses,
                taken_geneds: updatedGeneds,
            },
        });

        await axios.post(`${AI_URL}/reset`, { user_id: user.value.id });
        await axios.delete(
            `${DATA_URL}/students/conversation/${user.value.id}`
        );

        let countdown = 5;
        const countdownMsgId = newId();
        messages.value.push({
            id: countdownMsgId,
            role: "assistant",
            text: `Your schedule has been saved! 🎉\nResetting in ${countdown}…`,
        });

        while (countdown > 0) {
            await wait(1000);
            countdown--;
            const msg = messages.value.find((m) => m.id === countdownMsgId);
            if (msg)
                msg.text = `Your schedule has been saved! 🎉\nResetting in ${countdown}…`;
        }

        messages.value = [
            {
                id: newId(),
                role: "assistant",
                text: "Session reset! Let's plan your next semester. 📚",
            },
        ];
        confirmMessageId.value = null;
        selectedScheduleIndex.value = null;
        selectedMessageId.value = null;
        return;
    }

    messages.value.push({
        id: newId(),
        role: "user",
        text: "I want to add more requirements.",
    });
    messages.value.push({
        id: newId(),
        role: "assistant",
        text: "Sure! What would you like to adjust?",
    });
    confirmMessageId.value = null;
    await saveConversation();
};

const applySuggestion = (s) => (draftMessage.value = s);
const autoResize = () => {
    const el = textareaRef.value;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 100) + "px";
};

const resetConversation = async () => {
    if (!user.value) return;
    await axios.post(`${AI_URL}/reset`, { user_id: user.value.id });
    await axios.delete(`${DATA_URL}/students/conversation/${user.value.id}`);
    messages.value = [
        {
            id: newId(),
            role: "assistant",
            text: "Session reset! How can I help you?",
        },
    ];
    confirmMessageId.value = null;
    selectedScheduleIndex.value = null;
    selectedMessageId.value = null;
};
</script>
