import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import LoginPage from "@/components/login.vue";
import { createRouter, createWebHistory } from "vue-router";

// -------------------------
// Mock Router
// -------------------------
const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: "/chat", name: "chat" }],
});

router.push = vi.fn();

// -------------------------
// Mock Supabase
// -------------------------
vi.mock("@/supabase", () => ({
  supabase: {
    auth: {
      signInWithPassword: vi.fn(),
    },
  },
}));

import { supabase } from "@/supabase";

// Reset mocks before each test
beforeEach(() => {
  vi.clearAllMocks();
});

// -------------------------
// TEST SUITE
// -------------------------
describe("Login Page Unit Tests", () => {

  it("shows error when fields are empty", async () => {
    const wrapper = mount(LoginPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.email = "";
    wrapper.vm.password = "";

    await wrapper.vm.handleLogin();

    expect(wrapper.vm.message.type).toBe("error");
    expect(wrapper.vm.message.text).toContain("required");
  });

  it("detects invalid email format", async () => {
    const wrapper = mount(LoginPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.email = "abc@";
    wrapper.vm.password = "123456";

    await wrapper.vm.handleLogin();

    expect(wrapper.vm.message.type).toBe("error");
    expect(wrapper.vm.message.text).toContain("Invalid email format");
  });

  it("sets loading state before API responds", async () => {
    // Mock a pending Promise so loading = true stays true
    supabase.auth.signInWithPassword.mockImplementation(
      () => new Promise(() => {})
    );

    const wrapper = mount(LoginPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.email = "email@test.com";
    wrapper.vm.password = "password123";

    wrapper.vm.handleLogin();

    expect(wrapper.vm.isLoading).toBe(true);
  });

  it("handles successful login", async () => {
    supabase.auth.signInWithPassword.mockResolvedValue({
      data: { user: { id: "123" } },
      error: null,
    });

    const wrapper = mount(LoginPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.email = "valid@test.com";
    wrapper.vm.password = "password";

    await wrapper.vm.handleLogin();

    expect(wrapper.vm.message.type).toBe("success");
    expect(router.push).toHaveBeenCalledWith("/chat");
  });

  it("shows error for invalid credentials", async () => {
    supabase.auth.signInWithPassword.mockResolvedValue({
      data: null,
      error: { message: "Invalid login credentials" },
    });

    const wrapper = mount(LoginPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.email = "wrong@test.com";
    wrapper.vm.password = "badpass";

    await wrapper.vm.handleLogin();

    expect(wrapper.vm.message.type).toBe("error");
    expect(wrapper.vm.message.text.toLowerCase()).toContain("invalid");
  });
});
