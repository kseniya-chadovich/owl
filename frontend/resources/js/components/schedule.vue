<template>
  <div class="min-h-screen bg-white relative">

    <button
      @click="sidebarOpen = true"
      class="fixed top-4 left-4 z-50 bg-white border border-zinc-300 p-2 rounded-lg shadow hover:bg-zinc-100"
    >
      <svg xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6 text-[#800020]"
        fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16" />
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

      <div class="p-4 flex flex-col gap-4">

        <button
          class="w-full bg-[#800020] text-white px-4 py-3 rounded-xl hover:bg-[#800020]/80 transition"
          @click="$router.push('/account'); sidebarOpen = false;"
        >
          Account Information
        </button>

        <button
          class="w-full bg-zinc-200 text-[#800020] px-4 py-3 rounded-xl hover:bg-zinc-300 transition"
          @click="$router.push('/chat'); sidebarOpen = false;"
        >
          Scheduling Assistant
        </button>

      </div>
    </div>

    <div class="max-w-2xl mx-auto pt-20 px-4">

      <h1 class="text-3xl font-bold text-[#800020] mb-6">
        Your Current Schedule
      </h1>

      <div v-if="isLoading" class="text-zinc-600">Loading…</div>

      <div v-else-if="!schedule">
        <p class="text-zinc-600">No schedule saved yet.</p>
      </div>
      
      <div v-else>
        <div class="p-4 rounded-xl border border-zinc-300 bg-zinc-50 shadow-sm">

          <h2 class="text-xl font-semibold text-[#800020] mb-3">
            Saved Schedule
          </h2>

          <ul class="space-y-2">
            <li
              v-for="course in schedule.courses"
              :key="course.course"
              class="text-sm text-zinc-700 bg-white p-3 rounded-lg border border-zinc-200"
            >
              <strong>{{ course.course }}</strong>
              | {{ course.day_time || "TBD" }}
              | {{ course.credits }}cr
              | {{ course.category }}
              <span v-if="course.gened_type"> | GenEd: {{ course.gened_type }}</span>
              <span v-if="course.instructor"> | Prof: {{ course.instructor }}</span>
            </li>
          </ul>

          <p class="mt-3 text-sm text-zinc-600">
            Total credits: <strong>{{ schedule.total_credits }}</strong>
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { supabase } from "../supabase";

const DATA_URL = "https://supabase-kqbi.onrender.com";

const sidebarOpen = ref(false);
const schedule = ref(null);
const isLoading = ref(true);
const user = ref(null);

onMounted(async () => {
  const { data } = await supabase.auth.getUser();
  user.value = data?.user;

  if (!user.value) {
    isLoading.value = false;
    return;
  }

  try {
    const resp = await axios.get(`${DATA_URL}/students/schedules/${user.value.id}`);
    schedule.value = resp.data.schedule;
  } catch (err) {
    schedule.value = null;
  }

  isLoading.value = false;
});
</script>
