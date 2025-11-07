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
import { ref, onMounted, watch } from "vue";
import axios from "axios";

const BASE_URL = "https://scheduling-assistant-zl2c.onrender.com";
const USER_ID = "mock-user";
const STORAGE_KEY = "scheduling_assistant_chat";

let messageCounter = 0;
const newId = () => `msg-${messageCounter++}`;

const suggestions = [
  "I want classes only on Tuesdays and Thursdays",
  "Avoid early morning classes before 10 AM",
  "Need a lunch break between 12–1 PM",
  "Don't want classes with Professor Smith",
];

const messages = ref([
  {
    id: newId(),
    role: "assistant",
    text: "Hi! I'm your scheduling assistant. Tell me what you'd like for next semester.",
  },
]);

const draftMessage = ref("");
const isLoading = ref(false);
const errorMessage = ref("");
const textareaRef = ref(null);
const selectedScheduleIndex = ref(null);
const selectedMessageId = ref(null);
const currentConfirmMessageId = ref(null);

const autoResize = () => {
  const el = textareaRef.value;
  if (el) {
    el.style.height = "auto";
    el.style.height = el.scrollHeight + "px";
  }
};

// localStorage persistence
onMounted(() => {
  const savedData = localStorage.getItem(STORAGE_KEY);
  if (savedData) {
    try {
      const parsed = JSON.parse(savedData);
      messages.value = parsed.messages || messages.value;
      draftMessage.value = parsed.draftMessage || "";
    } catch (e) {
      console.warn("Failed to load chat history:", e);
    }
  }
});

watch(
  [messages, draftMessage],
  ([newMessages, newDraft]) => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        messages: newMessages,
        draftMessage: newDraft,
      })
    );
  },
  { deep: true }
);

const applySuggestion = (text) => {
  draftMessage.value = text;
};

const resetConversation = async () => {
  localStorage.removeItem(STORAGE_KEY);
  messages.value = [
    {
      id: newId(),
      role: "assistant",
      text: "Conversation reset. Share your new scheduling preferences whenever you're ready.",
    },
  ];
  draftMessage.value = "";
  errorMessage.value = "";
  try {
    await axios.post(`${BASE_URL}/reset`, { user_id: USER_ID }, { timeout: 30000 });
  } catch (err) {
    console.warn("Reset failed:", err);
  }
};

const sendMessage = async () => {
  const text = draftMessage.value.trim();
  if (!text || isLoading.value) return;
  errorMessage.value = "";
  draftMessage.value = "";
  messages.value.push({ id: newId(), role: "user", text });
  isLoading.value = true;

  try {
    const payload = { user_id: USER_ID, message: text };
    const { data } = await axios.post(`${BASE_URL}/dialog`, payload, { timeout: 60000 });
    handleAssistantResponse(data);
  } catch (err) {
    console.error("Failed to reach scheduling API:", err);
    errorMessage.value =
      "Failed to reach the scheduling assistant. Double-check your API URL or try again in a moment.";
    messages.value.push({
      id: newId(),
      role: "assistant",
      text: "I couldn't process that request because the backend isn't responding.",
    });
  } finally {
    isLoading.value = false;
  }
};

// ---- Handle backend data
const handleAssistantResponse = (data) => {
  if (!data || typeof data !== "object") {
    messages.value.push({
      id: newId(),
      role: "assistant",
      text: "Received an unexpected response from the scheduler service.",
    });
    return;
  }

  const { payload, schedules } = data;
  if (Array.isArray(schedules) && schedules.length) {
    messages.value.push({
      id: newId(),
      role: "assistant",
      text: "Here are your possible schedules:",
      schedules,
    });
  } else {
    const summary = buildAssistantReply(data);
    messages.value.push({ id: newId(), role: "assistant", text: summary });
  }
};

// ---- Card selection
const handleSelectSchedule = (index, message) => {
  selectedScheduleIndex.value = index;
  selectedMessageId.value = message.id;

  // Remove previous confirmation message (if any)
  if (currentConfirmMessageId.value) {
    const idx = messages.value.findIndex((m) => m.id === currentConfirmMessageId.value);
    if (idx !== -1) messages.value.splice(idx, 1);
  }

  const confirmMsg = {
    id: newId(),
    role: "assistant",
    text: `You selected Schedule ${index + 1}. Do you want to confirm this schedule?`,
    confirmOptions: ["Yes", "No"],
  };
  messages.value.push(confirmMsg);
  currentConfirmMessageId.value = confirmMsg.id;
};

// ---- Handle Yes / No
const handleConfirmOption = (choice) => {
  if (choice === "Yes" && selectedScheduleIndex.value !== null) {
    messages.value.push({
      id: newId(),
      role: "assistant",
      text:
        "🎉 Amazing! I’m happy I could help you build your routine for next semester. " +
        "Your schedule will be saved to your profile and bookmarked as your current plan.",
    });
  } else {
    selectedScheduleIndex.value = null;
    selectedMessageId.value = null;
    messages.value.push({
      id: newId(),
      role: "assistant",
      text: "Okay! You can select another schedule if you’d like.",
    });
  }
  currentConfirmMessageId.value = null;
};

const buildAssistantReply = (data) => {
  const { payload, schedules } = data;
  const parts = [];
  if (payload) parts.push(`Updated preferences:\n${JSON.stringify(payload, null, 2)}`);
  if (Array.isArray(schedules) && schedules.length) {
    const summaries = schedules.map((schedule, index) => {
      const courses = (schedule.courses || []).map(
        (c) => `${c.course} | ${c.day_time} | ${c.credits}cr`
      );
      return [`--- Schedule ${index + 1} ---`, ...courses].join("\n");
    });
    parts.push(summaries.join("\n\n"));
  } else parts.push("No schedules were generated for these preferences yet.");
  return parts.join("\n\n");
};
</script>
