<template>
    <div
        class="min-h-screen bg-gradient-to-b from-[#800020] to-[#880808] text-white flex flex-col"
    >
        <!-- NAVBAR -->
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
                        @click="$router.push('/')"
                        class="hidden sm:inline-flex border border-white/70 text-white font-medium px-3 py-1.5 rounded-lg text-sm hover:bg-white/10 transition"
                    >
                        ← Home
                    </button>
                    <button
                        @click="$router.push('/signup')"
                        class="border border-white bg-white text-[#800020] font-medium px-4 py-1.5 rounded-lg text-sm hover:bg-transparent hover:text-white transition"
                    >
                        Signup
                    </button>
                </div>
            </div>
        </header>

        <!-- MAIN -->
        <main class="flex-1 flex items-center justify-center px-6 pb-14">
            <div class="relative w-full max-w-md">
                <!-- Glow effect -->
                <div
                    class="pointer-events-none absolute -inset-6 rounded-3xl bg-gradient-to-br from-white/40 via-white/5 to-transparent blur-2xl opacity-70"
                ></div>

                <!-- MESSAGE BOX -->
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

                <!-- LOGIN CARD -->
                <div
                    :class="[
                        'relative z-10 bg-white/90 text-black backdrop-blur-xl rounded-2xl border border-white/40 px-8 py-10 shadow-xl',
                        'transform-gpu transition-all duration-700',
                        showCard ? 'card-in' : 'card-init',
                    ]"
                >
                    <h2 class="text-2xl font-bold mb-2 text-center text-black">
                        Welcome back 👋
                    </h2>
                    <p class="text-sm text-neutral-700 mb-6 text-center">
                        Log in to access your AI scheduling assistant.
                    </p>

                    <form @submit.prevent="handleLogin" class="space-y-5">
                        <!-- EMAIL -->
                        <div class="relative">
                            <input
                                type="email"
                                id="email"
                                v-model="email"
                                @focus="emailFocused = true"
                                @blur="emailFocused = false"
                                required
                                class="floating-input w-full px-4 py-2.5 rounded-lg bg-white border border-neutral-300 text-sm text-black focus:outline-none focus:ring-2 focus:ring-[#800020] transition"
                            />
                            <label
                                for="email"
                                class="floating-label"
                                :class="{
                                    'floating-label--active':
                                        emailFocused || email,
                                }"
                            >
                                Email Address
                            </label>
                        </div>

                        <!-- PASSWORD -->
                        <div class="relative">
                            <input
                                :type="showPassword ? 'text' : 'password'"
                                id="password"
                                v-model="password"
                                @focus="passwordFocused = true"
                                @blur="passwordFocused = false"
                                required
                                class="floating-input w-full px-4 py-2.5 pr-10 rounded-lg bg-white border border-neutral-300 text-sm text-black focus:outline-none focus:ring-2 focus:ring-[#800020] transition"
                            />
                            <label
                                for="password"
                                class="floating-label"
                                :class="{
                                    'floating-label--active':
                                        passwordFocused || password,
                                }"
                            >
                                Password
                            </label>

                            <!-- Eye Icon -->
                            <button
                                type="button"
                                @click="showPassword = !showPassword"
                                class="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-600 hover:text-neutral-900 text-lg"
                            >
                                <span v-if="showPassword">🙈</span>
                                <span v-else>👁️</span>
                            </button>
                        </div>

                        <!-- LOGIN BUTTON -->
                        <button
                            type="submit"
                            class="w-full bg-[#880808] text-white font-semibold text-base py-2.5 rounded-lg shadow-md hover:shadow-lg hover:-translate-y-0.5 transition disabled:opacity-60"
                            :disabled="isLoading"
                        >
                            {{ isLoading ? "Logging in..." : "Login" }}
                        </button>

                        <!-- SIGN UP LINK -->
                        <p class="text-sm text-center text-neutral-800 mt-1">
                            Don’t have an account?
                            <button
                                type="button"
                                @click="$router.push('/signup')"
                                class="font-medium text-[#800020] hover:text-[#550014] underline transition"
                            >
                                Sign up
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
const showCard = ref(false);

// For floating labels
const emailFocused = ref(false);
const passwordFocused = ref(false);

// For password visibility
const showPassword = ref(false);

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

const handleLogin = async () => {
    if (!email.value || !password.value) {
        showMessage("Please enter both email and password.", "error");
        return;
    }

    isLoading.value = true;

    try {
        const { data, error } = await supabase.auth.signInWithPassword({
            email: email.value,
            password: password.value,
        });

        if (error) throw error;

        if (!data.user) {
            showMessage("Login succeeded but no user returned.", "error");
            isLoading.value = false;
            return;
        }

        showMessage("Login successful! Redirecting...", "success");
        router.push("/chat");
    } catch (err) {
        console.error("Login error", err);
        showMessage(err.message || "Invalid email or password.", "error");
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    requestAnimationFrame(() => {
        showCard.value = true;
    });
});
</script>

<style scoped>
/* Message fade */
.fade-msg-enter-active,
.fade-msg-leave-active {
    transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-msg-enter-from,
.fade-msg-leave-to {
    opacity: 0;
    transform: translateY(-4px);
}

/* Card entrance animation */
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

/* Floating label styles */
.floating-input {
    padding-top: 1.4rem;
    padding-bottom: 0.9rem;
}

/* visible, soft gray placeholder */
.floating-input::placeholder {
    color: rgba(75, 85, 99, 0.8); /* neutral-600 */
    opacity: 1;
}

.floating-label {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.85rem;
    color: rgba(55, 65, 81, 0.9); /* neutral-700 */
    pointer-events: none;
    transition: all 0.18s ease-out;
    background: transparent;
}

.floating-label--active {
    top: 0.3rem;
    transform: translateY(0);
    font-size: 0.7rem;
    letter-spacing: 0.02em;
    opacity: 0.95;
}
</style>
