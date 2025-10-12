import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./components/homepage.vue";
import ChatPage from "./components/chatpage.vue";

const routes = [
    { path: "/", name: "Home", component: HomePage },
    { path: "/chat", name: "Chat", component: ChatPage },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
