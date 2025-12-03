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

        <div class="flex items-center gap-3">
          <button
            @click="$router.push('/')"
            class="border border-slate-300 bg-white text-slate-700 px-4 py-2 rounded-xl hover:bg-slate-50 hover:border-slate-400 transition-all duration-300 font-medium text-sm"
          >
            ← Home
          </button>
          <button
            @click="$router.push('/signup')"
            class="bg-gradient-to-r from-[#800020] to-[#a83232] text-white px-4 py-2 rounded-xl hover:shadow-md transition-all duration-300 font-medium text-sm"
          >
            Sign Up
          </button>
        </div>
      </div>
    </header>

    <main class="flex-1 flex items-center justify-center px-4 py-8">
      <div class="w-full max-w-md fade-up" :class="{ in: isMounted }">
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

        <div
          class="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 slide-up"
          :class="{ in: isMounted }"
        >
          <div class="text-center mb-8">
            <h1
              class="text-3xl font-bold text-slate-800 mb-3 slide-up"
              :class="{ in: isMounted }"
              style="animation-delay: 0.1s"
            >
              Welcome back 👋
            </h1>
            <p
              class="text-slate-600 text-base slide-up"
              :class="{ in: isMounted }"
              style="animation-delay: 0.2s"
            >
              Log in to access your AI scheduling assistant.
            </p>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-6">
            <div
              class="space-y-2 slide-up"
              :class="{ in: isMounted }"
              style="animation-delay: 0.3s"
            >
              <label for="email" class="text-sm font-medium text-slate-700">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                v-model="email"
                required
                class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                placeholder="Enter your email"
              />
            </div>

            <div
              class="space-y-2 slide-up"
              :class="{ in: isMounted }"
              style="animation-delay: 0.4s"
            >
              <label for="password" class="text-sm font-medium text-slate-700">
                Password
              </label>
              <div class="relative">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  id="password"
                  v-model="password"
                  required
                  class="w-full px-4 py-3 pr-12 rounded-xl border border-slate-300 bg-white text-slate-700 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#800020]/40 focus:border-transparent transition-all duration-200"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700 transition-colors text-lg"
                >
                  <span v-if="showPassword">🙈</span>
                  <span v-else>👁️</span>
                </button>
              </div>
            </div>

            <div
              class="slide-up"
              :class="{ in: isMounted }"
              style="animation-delay: 0.5s"
            >
              <button
                type="submit"
                class="w-full bg-gradient-to-r from-[#800020] to-[#a83232] text-white font-semibold py-3.5 rounded-xl hover:shadow-md transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="isLoading"
              >
                <span
                  v-if="isLoading"
                  class="flex items-center justify-center gap-2"
                >
                  <div
                    class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
                  ></div>
                  Logging in...
                </span>
                <span v-else>Login</span>
              </button>
            </div>

            <p
              class="text-center text-slate-600 text-sm slide-up"
              :class="{ in: isMounted }"
              style="animation-delay: 0.6s"
            >
              Don't have an account?
              <button
                type="button"
                @click="$router.push('/signup')"
                class="font-medium text-[#800020] hover:text-[#a83232] transition-colors underline"
              >
                Sign up here
              </button>
            </p>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { supabase } from "../supabase";

const router = useRouter();

const email = ref("");
const password = ref("");
const isLoading = ref(false);
const showPassword = ref(false);
const isMounted = ref(false);

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
  }, 4000);
};

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const handleLogin = async () => {
  // Check empty fields
  if (!email.value || !password.value) {
    showMessage("Both fields are required.", "error");
    return;
  }

  // Check **email format**
  if (!emailPattern.test(email.value)) {
    showMessage("Invalid email format.", "error");
    return;
  }

  isLoading.value = true;

  try {
    const result = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value,
    });

    // Defensive: mock might return undefined
    if (!result) {
      throw new Error("Authentication failed.");
    }

    const { data, error } = result;

    if (error) {
      throw new Error(error.message || "Invalid login.");
    }

    if (!data?.user) {
      throw new Error("Authentication failed: no user returned.");
    }

    showMessage("Login successful!", "success");
    router.push("/chat");
  } catch (err) {
    console.error("Login error", err);
    const readable =
      err?.message && typeof err.message === "string"
        ? err.message
        : "Invalid email or password.";
    showMessage(readable, "error");
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  setTimeout(() => (isMounted.value = true), 100);
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

.fade-up {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.fade-up.in {
  opacity: 1;
  transform: translateY(0);
}

.slide-up {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.slide-up.in {
  opacity: 1;
  transform: translateY(0);
}
</style>
