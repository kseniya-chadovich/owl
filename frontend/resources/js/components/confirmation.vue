<template>
    <div
        class="min-h-screen bg-gradient-to-b from-[#800020] to-[#880808] text-white flex flex-col"
    >

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
                    <button
                        @click="$router.push('/login')"
                        class="border border-white/80 bg-transparent text-white font-medium px-4 py-1.5 rounded-lg text-sm hover:bg-white hover:text-[#800020] transition"
                    >
                        Login
                    </button>
                </div>
            </div>
        </header>

        <main class="flex-1 flex items-center justify-center px-4 py-10">
            <div class="relative w-full max-w-xl">

                <div
                    class="pointer-events-none absolute -inset-6 rounded-3xl bg-gradient-to-br from-white/40 via-white/5 to-transparent blur-2xl opacity-70"
                ></div>

                <div
                    class="relative z-10 bg-white/95 text-black backdrop-blur-xl rounded-2xl border border-white/40 px-8 py-10 shadow-xl text-center animate-fade-up"
                >
                    <div
                        class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-[#800020]/10 text-[#800020] text-2xl"
                    >
                        ✉️
                    </div>

                    <h1 class="text-2xl font-bold mb-2">
                        Email Confirmation Sent!
                    </h1>
                    <p
                        class="text-sm md:text-base text-neutral-700 mb-6 leading-relaxed"
                    >
                        We’ve sent a confirmation email to your inbox.
                        <br class="hidden md:block" />
                        Please check your email and click the link to verify
                        your account.
                    </p>

                    <button
                        @click="$router.push('/login')"
                        class="inline-flex items-center justify-center bg-[#880808] text-white font-semibold text-sm md:text-base px-6 py-2.5 rounded-lg shadow-md hover:shadow-lg hover:-translate-y-0.5 transition"
                    >
                        Go to Login
                    </button>

                    <p class="text-xs text-neutral-600 mt-4">
                        Didn’t get the email? Check your spam folder or try
                        again from the login page.
                    </p>
                </div>
            </div>
        </main>
    </div>
</template>

<style scoped>

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(16px);
        filter: blur(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
        filter: blur(0);
    }
}
.animate-fade-up {
    animation: fadeUp 0.6s ease-out forwards;
}
</style>
