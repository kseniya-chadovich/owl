<template>
    
    <button
        @click="sidebarOpen = true"
        class="fixed top-4 left-4 z-50 bg-white border border-zinc-300 p-2 rounded-lg shadow hover:bg-zinc-100"
    >

        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6 text-[#800020]"
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

    <div
        v-if="sidebarOpen"
        @click="sidebarOpen = false"
        class="fixed inset-0 bg-black bg-opacity-40 z-40"
    ></div>

    <div
        class="fixed top-0 left-0 h-full w-64 bg-white shadow-xl z-50 transform transition-transform duration-300"
        :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
        <div class="p-6 border-b border-zinc-200">
            <h2 class="text-xl font-bold text-[#800020]">Menu</h2>
        </div>

        <div class="p-4 flex flex-col gap-3">
            <button
                class="w-full bg-[#800020] text-white px-4 py-3 rounded-xl hover:bg-[#800020]/80 transition"
                @click="
                    $router.push('/account');
                    sidebarOpen = false;
                "
            >
                Account Information
            </button>

            <button
                class="w-full bg-zinc-200 text-[#800020] px-4 py-3 rounded-xl hover:bg-zinc-300 transition"
                @click="
                    $router.push('/schedule');
                    sidebarOpen = false;
                "
            >
                Current Schedule
            </button>
        </div>
    </div>

    <div class="min-h-screen bg-white flex flex-col items-center py-16 px-4">

        <div class="text-center mb-12">
            <h1 class="text-4xl md:text-5xl font-bold text-[#800020]">
                Chat with Your Scheduling Assistant
            </h1>
            <p class="text-zinc-600 mt-3 text-lg">
                Describe your preferences in natural language
            </p>
        </div>

        <div v-if="isInitializing" class="py-20 text-center text-zinc-500">
            <div
                class="animate-spin h-10 w-10 border-4 border-[#800020] border-t-transparent rounded-full mx-auto"
            ></div>
            <p class="mt-4 text-lg">Loading your chat session…</p>
        </div>

        <div
            v-else
            class="w-full max-w-3xl bg-white border border-zinc-200 rounded-3xl shadow-sm flex flex-col overflow-hidden"
        >

            <div
                v-if="errorMessage"
                class="mx-4 mt-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
            >
                {{ errorMessage }}
            </div>

            <div class="flex-1 p-6 space-y-6 overflow-y-auto">
                <div
                    v-for="message in messages"
                    :key="message.id"
                    class="flex items-start gap-3"
                    :class="message.role === 'user' ? 'justify-end' : ''"
                >
                    <div
                        v-if="message.role === 'assistant'"
                        class="flex h-10 w-10 items-center justify-center rounded-full border border-zinc-300 text-[#800020] font-semibold shrink-0"
                    >
                        🧠
                    </div>
                    <div
                        v-else
                        class="flex h-10 w-10 items-center justify-center rounded-full border border-[#800020]/30 text-[#800020] shrink-0 order-last"
                    >
                        👤
                    </div>

                    <div
                        v-if="!message.schedules"
                        class="max-w-[80%] whitespace-pre-wrap rounded-2xl px-4 py-3 text-sm leading-relaxed"
                        :class="
                            message.role === 'assistant'
                                ? 'bg-zinc-100 text-zinc-800 rounded-tl-none'
                                : 'bg-[#800020] text-white rounded-tr-none'
                        "
                    >
                        {{ message.text }}

                        <div
                            v-if="message.confirmOptions"
                            class="flex gap-3 mt-3"
                        >
                            <button
                                v-for="opt in message.confirmOptions"
                                :key="opt"
                                @click="handleConfirmOption(opt)"
                                class="px-4 py-2 text-sm rounded-lg border border-zinc-300 hover:bg-zinc-100 transition"
                            >
                                {{ opt }}
                            </button>
                        </div>
                    </div>

                    <div v-else class="flex flex-col gap-4 max-w-[80%]">
                        <div
                            v-for="(schedule, index) in message.schedules"
                            :key="index"
                            @click="handleSelectSchedule(index, message)"
                            class="border rounded-2xl p-4 transition cursor-pointer relative bg-white/90 backdrop-blur-sm"
                            :class="[
                                selectedScheduleIndex === index &&
                                message.id === selectedMessageId
                                    ? 'border-[#800020] shadow-[0_0_0_1px_rgba(128,0,32,0.3)] bg-[#800020]/5'
                                    : 'border-zinc-200 hover:bg-zinc-50 hover:shadow-sm',
                            ]"
                        >

                            <div class="flex justify-between items-center mb-3">
                                <div class="flex items-center gap-2">
                                    <h3 class="font-semibold text-[#800020]">
                                        Schedule {{ index + 1 }}
                                    </h3>
                                    <span
                                        class="inline-flex items-center rounded-full bg-[#800020]/10 text-[#800020] text-xs px-2 py-0.5"
                                    >
                                        {{ schedule.courses.length }} courses
                                    </span>
                                </div>

                                <span
                                    v-if="
                                        selectedScheduleIndex === index &&
                                        message.id === selectedMessageId
                                    "
                                    class="inline-flex items-center text-xs font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full"
                                >
                                    ✅ Selected
                                </span>
                            </div>
                            
                            <div class="mt-1 overflow-x-auto">
                                <table
                                    class="min-w-full text-xs sm:text-sm border-separate border-spacing-y-1"
                                >
                                    <thead>
                                        <tr class="text-zinc-500">
                                            <th
                                                class="text-left font-medium pr-3 pb-1"
                                            >
                                                Course
                                            </th>
                                            <th
                                                class="text-left font-medium pr-3 pb-1 hidden sm:table-cell"
                                            >
                                                Time
                                            </th>
                                            <th
                                                class="text-left font-medium pr-3 pb-1"
                                            >
                                                Credits
                                            </th>
                                            <th
                                                class="text-left font-medium pr-3 pb-1 hidden md:table-cell"
                                            >
                                                Type
                                            </th>
                                            <th
                                                class="text-left font-medium pb-1 hidden lg:table-cell"
                                            >
                                                Details
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr
                                            v-for="course in schedule.courses"
                                            :key="course.course"
                                            class="bg-zinc-50/80 hover:bg-zinc-100 transition-colors"
                                        >

                                            <td
                                                class="px-3 py-2 rounded-l-xl align-top"
                                            >
                                                <div
                                                    class="font-semibold text-zinc-900"
                                                >
                                                    {{ course.course }}
                                                </div>

                                                <div
                                                    class="mt-1 text-[11px] text-zinc-500 sm:hidden space-y-0.5"
                                                >
                                                    <div>
                                                        <span
                                                            class="font-medium"
                                                            >Time:</span
                                                        >
                                                        {{
                                                            course.day_time ||
                                                            "TBD"
                                                        }}
                                                    </div>
                                                    <div
                                                        v-if="course.instructor"
                                                    >
                                                        <span
                                                            class="font-medium"
                                                            >Prof:</span
                                                        >
                                                        {{ course.instructor }}
                                                    </div>
                                                </div>
                                            </td>

                                            <td
                                                class="px-3 py-2 align-top text-zinc-700 hidden sm:table-cell"
                                            >
                                                {{ course.day_time || "TBD" }}
                                            </td>

                                            <td class="px-3 py-2 align-top">
                                                <span
                                                    class="inline-flex items-center px-2 py-0.5 rounded-full bg-zinc-100 text-zinc-800 text-[11px]"
                                                >
                                                    {{ course.credits }} cr
                                                </span>
                                            </td>

                                            <td
                                                class="px-3 py-2 align-top hidden md:table-cell"
                                            >
                                                <div
                                                    class="flex flex-wrap gap-1"
                                                >
                                                    <span
                                                        v-if="course.category"
                                                        class="inline-flex items-center px-2 py-0.5 rounded-full bg-[#800020]/10 text-[#800020] text-[11px]"
                                                    >
                                                        {{ course.category }}
                                                    </span>
                                                    <span
                                                        v-if="course.gened_type"
                                                        class="inline-flex items-center px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 text-[11px]"
                                                    >
                                                        GenEd:
                                                        {{ course.gened_type }}
                                                    </span>
                                                </div>
                                            </td>

                                            <td
                                                class="px-3 py-2 align-top text-zinc-700 hidden lg:table-cell rounded-r-xl"
                                            >
                                                <span v-if="course.instructor"
                                                    >Prof:
                                                    {{
                                                        course.instructor
                                                    }}</span
                                                >
                                                <span
                                                    v-else
                                                    class="text-zinc-400 italic"
                                                    >Instructor TBA</span
                                                >
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            <div
                                class="mt-3 flex justify-between items-center text-xs sm:text-sm text-zinc-600"
                            >
                                <p>
                                    <span class="font-medium text-zinc-800"
                                        >Total credits:</span
                                    >
                                    {{ schedule.total_credits ?? "n/a" }}
                                </p>
                                <p class="hidden sm:block text-zinc-500">
                                    Click to select this schedule.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div
                    v-if="isLoading"
                    class="flex items-start gap-3 text-sm text-zinc-500"
                >
                    <div
                        class="flex h-10 w-10 items-center justify-center rounded-full border border-zinc-300 text-[#800020] font-semibold"
                    >
                        🧠
                    </div>
                    <div
                        class="rounded-2xl rounded-tl-none bg-zinc-100 px-4 py-3"
                    >
                        Thinking…
                    </div>
                </div>
            </div>

            <div class="border-t border-zinc-200 bg-zinc-50 p-4">
                <div class="flex items-end gap-3">
                    <textarea
                        ref="textareaRef"
                        placeholder="Describe your ideal semester schedule..."
                        v-model="draftMessage"
                        @input="autoResize"
                        @keydown.enter.exact.prevent="sendMessage"
                        rows="1"
                        class="flex-1 resize-none rounded-xl border border-zinc-300 bg-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#800020]/40"
                        :disabled="isLoading"
                    ></textarea>

                    <button
                        @click="resetConversation"
                        :disabled="isLoading"
                        class="bg-zinc-200 hover:bg-zinc-300 text-[#800020] p-3 rounded-xl transition flex items-center justify-center"
                        title="Reset session"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="2"
                            stroke="currentColor"
                            class="w-5 h-5"
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
                        class="bg-[#800020] hover:bg-[#800020]/80 text-white p-3 rounded-xl transition flex items-center justify-center"
                        :class="
                            isLoading || !draftMessage.trim()
                                ? 'opacity-50 cursor-not-allowed'
                                : ''
                        "
                        title="Send"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="2"
                            stroke="currentColor"
                            class="w-5 h-5"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M3 10h11M9 21l12-9L9 3v7H3v4h6v7z"
                            />
                        </svg>
                    </button>
                </div>

                <div class="mt-3 flex flex-wrap gap-2">
                    <button
                        v-for="suggestion in suggestions"
                        :key="suggestion"
                        class="text-sm border border-zinc-300 px-3 py-2 rounded-full text-zinc-700 hover:bg-zinc-100 transition"
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
import { ref, onMounted } from "vue";
import axios from "axios";
import { supabase } from "../supabase";

const AI_URL = "https://scheduling-assistant-zl2c.onrender.com";
const DATA_URL = "https://supabase-kqbi.onrender.com";

const user = ref(null);
const messages = ref([]);
const draftMessage = ref("");
const isLoading = ref(false);
const sidebarOpen = ref(false);

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

let messageCounter = 0;
const newId = () => `msg-${messageCounter++}`;
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const stripSection = (courseName) => {
    return courseName.replace(/\s*\(\d+\)\s*$/, "").trim();
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
                text: "Hi! I'm your scheduling assistant.",
            },
        ];
        isInitializing.value = false;
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

        if (t.startsWith("User:")) {
            return {
                id: newId(),
                role: "user",
                text: t.replace("User: ", ""),
            };
        }

        return { id: newId(), role: "assistant", text: t };
    });

    isInitializing.value = false;
};

onMounted(async () => {
    await loadUser();
});

const saveConversation = async () => {
    if (!user.value) return;

    const lines = messages.value.map((m) => {
        if (m.schedules) return JSON.stringify({ schedules: m.schedules });
        return m.role === "user" ? `User: ${m.text}` : m.text;
    });

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
        if (msg) {
            msg.text = `You're looking at Schedule ${n}. Do you want to confirm it or add more requirements?`;
        }
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

        await axios.post(`${AI_URL}/reset`, {
            user_id: user.value.id,
        });

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

const applySuggestion = (s) => {
    draftMessage.value = s;
};

const textareaRef = ref(null);
const autoResize = () => {
    const el = textareaRef.value;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = el.scrollHeight + "px";
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
