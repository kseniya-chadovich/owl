<template>
    <div
        class="min-h-screen bg-gradient-to-b from-[#800020] to-[#880808] text-white"
    >
        <header
            class="flex justify-between items-center max-w-7xl mx-auto px-8 py-6"
        >
            <h1 class="text-2xl font-bold tracking-tight">AI Scheduler</h1>

            <div class="flex space-x-4">
                <button
                    @click="goTo('/signup')"
                    class="border-2 border-white bg-white text-[#800020] font-semibold px-5 py-2 rounded-xl hover:bg-transparent hover:text-white transition-all duration-300"
                >
                    Signup
                </button>

                <button
                    @click="goTo('/login')"
                    class="border-2 border-white bg-white text-[#800020] font-semibold px-5 py-2 rounded-xl hover:bg-transparent hover:text-white transition-all duration-300"
                >
                    Login
                </button>
            </div>
        </header>

        <main class="text-center mt-20 px-6">
            <p
                class="inline-block mb-4 px-4 py-1 rounded-full bg-white/15 border border-white/30 text-sm font-medium fade-up"
                :class="{ in: showHero }"
                style="transition-delay: 80ms"
            >
                🌸 Smart Academic Planning
            </p>

            <h2
                class="text-5xl md:text-6xl font-extrabold leading-tight fade-up pop"
                :class="{ in: showHero }"
                style="transition-delay: 160ms; animation-delay: 160ms"
            >
                Your AI-Powered <br />
                <span class="text-white">Schedule Assistant</span>
            </h2>

            <p
                class="mt-6 text-lg text-white/80 max-w-2xl mx-auto fade-up"
                :class="{ in: showHero }"
                style="transition-delay: 260ms"
            >
                Create the perfect semester schedule that fits your preferences,
                keeps you on track to graduate, and reduces the workload on
                academic advisors.
            </p>

            <div class="mt-8 flex justify-center">
                <button
                    @click="handleGetStarted"
                    class="bg-[#800020] text-white px-8 py-4 rounded-xl font-semibold hover:bg-[#880808] transition-all duration-300 hover:scale-105 fade-up shadow-lg"
                    :class="{ in: showHero }"
                    style="transition-delay: 360ms"
                >
                    Get Started →
                </button>
            </div>
        </main>

        <section
            class="mt-24 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto px-6"
        >
            <div
                v-for="(feature, i) in features"
                :key="feature.title"
                class="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 fade-up hover:scale-105"
                :class="{ in: showFeatures }"
                :style="{ transitionDelay: `${120 * i}ms` }"
            >
                <div class="text-4xl mb-3">{{ feature.icon }}</div>
                <h3 class="text-xl font-semibold">{{ feature.title }}</h3>
                <p class="mt-2 text-white/80">{{ feature.desc }}</p>
            </div>
        </section>

        <footer
            class="mt-24 text-center text-white/70 border-t border-white/20 py-8 text-sm fade-up"
            :class="{ in: showFeatures }"
            style="transition-delay: 400ms"
        >
            © {{ new Date().getFullYear() }} AI Scheduler. All rights reserved.
        </footer>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { supabase } from "../supabase";

const router = useRouter();

const showHero = ref(false);
const showFeatures = ref(false);

const features = [
    {
        icon: "📅",
        title: "Smart Scheduling",
        desc: "AI considers your preferences, requirements, and graduation timeline.",
    },
    {
        icon: "🤝",
        title: "For Students & Advisors",
        desc: "Reduces advisor workload while empowering student choice.",
    },
    {
        icon: "🎓",
        title: "Graduation Ready",
        desc: "Always keeps you on track to graduate on time.",
    },
];

const goTo = (path) => {
    router.push(path);
};

const handleGetStarted = async () => {
    try {
        // Check if user is logged in
        const {
            data: { user },
        } = await supabase.auth.getUser();

        if (user) {
            // User is logged in, go to chat
            router.push("/chat");
        } else {
            // User is not logged in, go to login
            router.push("/login");
        }
    } catch (error) {
        console.error("Error checking auth status:", error);
        // If there's an error, default to login page
        router.push("/login");
    }
};

onMounted(() => {
    requestAnimationFrame(() => {
        showHero.value = true;
        setTimeout(() => (showFeatures.value = true), 550);
    });
});
</script>

<style scoped>
.fade-up {
    opacity: 0;
    transform: translateY(16px);
    filter: blur(6px);
    transition: opacity 700ms ease, transform 700ms ease, filter 700ms ease;
}
.fade-up.in {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
}

@keyframes popIn {
    0% {
        transform: scale(0.98);
    }
    60% {
        transform: scale(1.015);
    }
    100% {
        transform: scale(1);
    }
}
.pop.in {
    animation: popIn 700ms cubic-bezier(0.2, 0.65, 0.25, 1) both;
}
</style>
