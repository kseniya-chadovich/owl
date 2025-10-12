<template>
    <div class="page-background">
        <!-- Custom Message Box for Success/Error -->
        <div v-if="message.visible" :class="['message-box', message.type]">
            {{ message.text }}
            <button @click="message.visible = false" class="close-btn">
                &times;
            </button>
        </div>

        <div class="container">
            <h1>Login</h1>
            <form @submit.prevent="handleLogin">
                <div class="input-group">
                    <label for="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        v-model="email"
                        placeholder="Enter your email"
                        required
                    />
                </div>

                <div class="input-group">
                    <label for="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        v-model="password"
                        placeholder="Enter your password"
                        required
                    />
                </div>

                <button type="submit" class="login-btn">
                    {{ isLoading ? 'Logging in...' : 'Login' }}
                </button>

                <p class="small-text">
                    Don’t have an account?
                    <a @click="$router.push('/signup')">Sign up</a>
                </p>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'; // Removed onMounted as it's not needed for localStorage
import { useRouter } from 'vue-router';


// --- Router Setup ---
const router = useRouter();
const email = ref('');
const password = ref('');
const isLoading = ref(false);

const message = ref({
    text: '',
    type: '', // 'success' or 'error'
    visible: false,
});


// --- Login Handler ---
const handleLogin = async () => {
    // Basic frontend validation
    if (!email.value || !password.value) {
        showMessage('Please enter both email and password.', 'error');
        return;
    }

    isLoading.value = true;

    // Use localStorage for temporary client-side authentication check
    const storedEmail = localStorage.getItem("userEmail");
    const storedPassword = localStorage.getItem("userPassword");
    
    // Simulate network delay for better user experience
    await new Promise(resolve => setTimeout(resolve, 500)); 

    if (email.value === storedEmail && password.value === storedPassword) {
        // Successful login
        showMessage('Login successful! Redirecting to dashboard...', 'success');
        
        // Use Vue Router to navigate
        setTimeout(() => {
            router.push('/dashboard'); 
        }, 1000);
    } else {
        // Failed login
        showMessage('Invalid email or password.', 'error');
    }
    
    isLoading.value = false;
};

// --- Custom Message Display Function ---
const showMessage = (text, type) => {
    message.value.text = text;
    message.value.type = type;
    message.value.visible = true;
};
</script>

<style scoped>
.page-background {
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(to bottom right, #a41e34, #ffffff);
    color: #333;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px;
    margin: 0;
    min-height: 100vh;
    width: 100%;
    position: relative; 
}

.container {
    background-color: #fff;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    padding: 40px 50px;
    width: 100%; 
    max-width: 400px; 
    text-align: center;
    box-sizing: border-box;
}

h1 {
    color: #a41e34;
    margin-bottom: 25px;
    font-size: 28px;
}

.input-group {
    text-align: left;
    margin-bottom: 18px;
}

label {
    display: block;
    font-weight: 600;
    margin-bottom: 6px;
}

input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 14px;
    transition: border 0.2s ease-in-out;
    box-sizing: border-box; 
}

input:focus {
    outline: none;
    border-color: #a41e34;
}

.login-btn {
    width: 100%;
    background-color: #a41e34;
    color: #fff;
    padding: 12px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    margin-top: 10px;
    transition: background 0.2s ease-in-out;
}

.login-btn:hover {
    background-color: #8e162b;
}

.small-text {
    font-size: 13px;
    margin-top: 20px;
}

.small-text a {
    color: #a41e34;
    text-decoration: none;
    font-weight: 600;
    cursor: pointer; 
}

.small-text a:hover {
    text-decoration: underline;
}


.message-box {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 15px 30px;
    border-radius: 8px;
    font-weight: 600;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-width: 300px;
}
.message-box.success {
    background-color: #e6ffed;
    color: #38a169;
    border: 1px solid #9ae6b4;
}
.message-box.error {
    background-color: #fff5f5;
    color: #e53e3e;
    border: 1px solid #feb2b2;
}
.close-btn {
    background: none;
    border: none;
    color: inherit;
    font-size: 18px;
    margin-left: 15px;
    cursor: pointer;
    line-height: 1;
}
</style>