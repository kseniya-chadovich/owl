import { createApp } from "vue";
import App from "./components/app.vue";
import router from "./router";
import Signup from "./components/signup.vue";
import Login from "./components/login.vue";

createApp(App).use(router).mount("#app");
const app = createApp({});
app.component("signup", Signup);
app.component("login", Login);