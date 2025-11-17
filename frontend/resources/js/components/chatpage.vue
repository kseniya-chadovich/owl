<template>
  <div class="min-h-screen bg-white flex flex-col items-center py-16 px-4">
    <!-- TITLE -->
    <div class="text-center mb-12">
      <h1 class="text-4xl md:text-5xl font-bold text-[#800020]">
        Chat with Your Scheduling Assistant
      </h1>
      <p class="text-zinc-600 mt-3 text-lg">
        Describe your preferences in natural language
      </p>
    </div>

    <!-- CHAT CONTAINER -->
    <div
      class="w-full max-w-3xl bg-white border border-zinc-200 rounded-3xl shadow-sm flex flex-col overflow-hidden"
    >
      <!-- STATUS -->
      <div
        v-if="errorMessage"
        class="mx-4 mt-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
      >
        {{ errorMessage }}
      </div>

      <!-- CHAT MESSAGES -->
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

          <!-- TEXT MESSAGES -->
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

            <!-- Confirmation options -->
            <div v-if="message.confirmOptions" class="flex gap-3 mt-3">
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

          <!-- SCHEDULE CARDS -->
          <div v-else class="flex flex-col gap-4 max-w-[80%]">
            <div
              v-for="(schedule, index) in message.schedules"
              :key="index"
              @click="handleSelectSchedule(index, message)"
              class="border rounded-xl p-4 transition cursor-pointer relative"
              :class="[
                selectedScheduleIndex === index && message.id === selectedMessageId
                  ? 'bg-[#800020]/10 border-[#800020] shadow-inner'
                  : 'bg-white border-zinc-200 hover:bg-pink-50'
              ]"
            >
              <div class="flex justify-between items-center mb-2">
                <h3 class="font-semibold text-[#800020]">
                  Schedule {{ index + 1 }}
                </h3>
                <span
                  v-if="selectedScheduleIndex === index && message.id === selectedMessageId"
                  class="text-red-500"
                >
                  ✅
                </span>
              </div>
              <ul class="text-sm text-zinc-700 mb-2">
                <li v-for="course in schedule.courses" :key="course.course">
                  {{ course.course }} |
                  {{ course.day_time || "TBD" }} |
                  {{ course.credits }}cr |
                  {{ course.category }}
                </li>
              </ul>
              <p class="text-sm text-zinc-600">
                Total credits: {{ schedule.total_credits ?? "n/a" }}
              </p>
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
          <div class="rounded-2xl rounded-tl-none bg-zinc-100 px-4 py-3">
            Thinking…
          </div>
        </div>
      </div>

      <!-- INPUT AREA -->
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

const BASE_URL = "https://scheduling-assistant-zl2c.onrender.com"; // AI service URL
const messages = ref([]);
const draftMessage = ref("");
const isLoading = ref(false);
const errorMessage = ref("");
const textareaRef = ref(null);

let messageCounter = 0;
const newId = () => `msg-${messageCounter++}`;

// Suggestion buttons
const suggestions = [
  "I want classes only on Tuesdays and Thursdays",
  "Avoid early morning classes before 10 AM",
  "Need a lunch break between 12–1 PM",
  "Don't want classes with Professor Smith",
];

// ---------------------------------------------------------------------
// 1) Load User ID from Supabase Auth
// ---------------------------------------------------------------------
const userId = ref(null);

onMounted(async () => {
  const { data } = await supabase.auth.getUser();

  if (!data?.user) {
    errorMessage.value = "You must be logged in to use the assistant.";
    return;
  }

  userId.value = data.user.id;

  // Initialize chat with backend state
  await loadInitialConversation();
});

// ---------------------------------------------------------------------
// 2) Load conversation from backend (/dialog initializes itself)
// ---------------------------------------------------------------------
async function loadInitialConversation() {
  messages.value = [
    {
      id: newId(),
      role: "assistant",
      text: "Loading your conversation...",
    },
  ];

  try {
    const res = await axios.post(`${BASE_URL}/dialog`, {
      user_id: userId.value,
      message: "__LOAD_STATE__",
    });

    // Remove loading message
    messages.value = [];

    // Add assistant reply
    messages.value.push({
      id: newId(),
      role: "assistant",
      text: "Hi! I'm your scheduling assistant. How can I help today?",
    });
  } catch (e) {
    console.error("Failed to load conversation:", e);
    messages.value = [
      {
        id: newId(),
        role: "assistant",
        text: "Hi! I'm your scheduling assistant. Tell me your preferences!",
      },
    ];
  }
}

// ---------------------------------------------------------------------
// 3) Handle user sending messages
// ---------------------------------------------------------------------
const sendMessage = async () => {
  const text = draftMessage.value.trim();
  if (!text || isLoading.value) return;

  draftMessage.value = "";
  errorMessage.value = "";

  // Show user message in UI
  messages.value.push({ id: newId(), role: "user", text });

  isLoading.value = true;

  try {
    const payload = {
      user_id: userId.value,
      message: text,
    };

    const { data } = await axios.post(`${BASE_URL}/dialog`, payload, {
      timeout: 60000,
    });

    handleAssistantResponse(data);
  } catch (err) {
    console.error(err);
    errorMessage.value = "Unable to reach the AI right now.";
    messages.value.push({
      id: newId(),
      role: "assistant",
      text: "I couldn't reach the AI server. Please try again shortly.",
    });
  } finally {
    isLoading.value = false;
  }
};

// ---------------------------------------------------------------------
// 4) Process backend assistant response
// ---------------------------------------------------------------------
const handleAssistantResponse = (data) => {
  if (!data) {
    messages.value.push({
      id: newId(),
      role: "assistant",
      text: "Received an unexpected response.",
    });
    return;
  }

  const { payload, schedules } = data;

  if (Array.isArray(schedules) && schedules.length > 0) {
    messages.value.push({
      id: newId(),
      role: "assistant",
      text: "Here are your schedule options:",
      schedules,
    });
  } else {
    messages.value.push({
      id: newId(),
      role: "assistant",
      text: buildAssistantReply(data),
    });
  }
};

// ---------------------------------------------------------------------
// 5) Reset conversation for this user
// ---------------------------------------------------------------------
const resetConversation = async () => {
  messages.value = [
    {
      id: newId(),
      role: "assistant",
      text: "Resetting your session...",
    },
  ];

  try {
    await axios.post(`${BASE_URL}/reset`, {
      user_id: userId.value,
    });
  } catch (e) {
    console.warn("Reset error:", e);
  }

  messages.value.push({
    id: newId(),
    role: "assistant",
    text: "Your session has been reset. Tell me your new preferences!",
  });
};

// ---------------------------------------------------------------------
// 6) Suggestion button click
// ---------------------------------------------------------------------
const applySuggestion = (text) => {
  draftMessage.value = text;
};

// ---------------------------------------------------------------------
// 7) Format complex replies
// ---------------------------------------------------------------------
const buildAssistantReply = (data) => {
  const { payload, schedules } = data;

  const parts = [];

  if (payload) {
    parts.push(`Updated preferences:\n${JSON.stringify(payload, null, 2)}`);
  }

  if (Array.isArray(schedules) && schedules.length) {
    const summaries = schedules.map((s, i) => {
      const courses = (s.courses || []).map(
        (c) => `${c.course} | ${c.day_time} | ${c.credits} cr`
      );
      return [`--- Schedule ${i + 1} ---`, ...courses].join("\n");
    });
    parts.push(summaries.join("\n\n"));
  }

  return parts.join("\n\n");
};
</script>

