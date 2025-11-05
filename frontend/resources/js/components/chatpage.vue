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
            <!-- CHAT MESSAGES -->
            <div class="flex-1 p-6 space-y-6 overflow-y-auto">
                <!-- Message 1 (bot) -->
                <div class="flex items-start gap-3">
                    <div
                        class="flex h-10 w-10 items-center justify-center rounded-full border border-zinc-300 text-[#800020] font-semibold"
                    >
                        🧠
                    </div>
                    <div
                        class="bg-zinc-100 text-zinc-800 px-4 py-3 rounded-2xl rounded-tl-none max-w-[80%]"
                    >
                        Hi! I'm your scheduling assistant. Tell me what you're
                        looking for in your next semester schedule, and I'll
                        help you create the perfect plan.
                    </div>
                </div>

                <!-- Message 2 (user) -->
                <div class="flex items-start justify-end gap-3">
                    <div
                        class="bg-[#800020] text-white px-4 py-3 rounded-2xl rounded-tr-none max-w-[80%]"
                    >
                        Avoid early morning classes before 10 AM
                    </div>
                    <div
                        class="flex h-10 w-10 items-center justify-center rounded-full border border-[#800020]/30 text-[#800020]"
                    >
                        👤
                    </div>
                </div>

                <!-- Message 3 (bot) -->
                <div class="flex items-start gap-3">
                    <div
                        class="flex h-10 w-10 items-center justify-center rounded-full border border-zinc-300 text-[#800020] font-semibold"
                    >
                        🧠
                    </div>
                    <div
                        class="bg-zinc-100 text-zinc-800 px-4 py-3 rounded-2xl rounded-tl-none max-w-[80%]"
                    >
                        Got it! Treating graduation plan and prerequisites as
                        hard constraints, and your preferences as soft ones.
                        Here are some possible schedules you can choose from.
                    </div>
                </div>
            </div>

            <!-- INPUT AREA -->
            <div class="border-t border-zinc-200 bg-zinc-50 p-4">
                <div class="flex items-center gap-3">
                    <input
                        type="text"
                        placeholder="Describe your ideal semester schedule..."
                        class="flex-1 rounded-xl border border-zinc-300 bg-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#800020]/40"
                    />
                    <button
                        class="bg-[#800020] hover:bg-[#800020]/80 text-white p-3 rounded-xl transition"
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

                <!-- Quick suggestion chips -->
                <div class="mt-3 flex flex-wrap gap-2">
                    <button
                        v-for="suggestion in suggestions"
                        :key="suggestion"
                        class="text-sm border border-zinc-300 px-3 py-2 rounded-full text-zinc-700 hover:bg-zinc-100 transition"
                    >
                        {{ suggestion }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
const suggestions = [
    "I want classes only on Tuesdays and Thursdays",
    "Avoid early morning classes before 10 AM",
    "Need a lunch break between 12–1 PM",
    "Don't want classes with Professor Smith",
];
</script>
