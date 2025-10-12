import { createRouter, createWebHistory } from "vue-router";

import Home from "./components/homepage.vue";
import Login from "./components/login.vue";
import Signup from "./components/signup.vue";
import Chat from "./components/chatpage.vue";
const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },

    {
        path: "/login",
        name: "Login",
        component: Login, 
    },

    {
        path: "/signup",
        name: "Signup",
        component: Signup, 
    },

    {
        path: "/chat",
        name: "Chat",
        component: Chat,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
