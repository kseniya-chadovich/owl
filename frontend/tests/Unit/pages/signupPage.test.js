import { describe, it, expect, beforeEach, vi } from "vitest";
import { mount } from "@vue/test-utils";
import SignupPage from "@/components/signup.vue";
import { createRouter, createWebHistory } from "vue-router";

// ------------------------------
// Router mock
// ------------------------------
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/confirmation", component: { template: "<div>done</div>" } }
  ],
});

// ------------------------------
// Supabase mock
// ------------------------------
vi.mock("@/supabase", () => ({
  supabase: {
    auth: {
      signUp: vi.fn(),
    },
  },
}));

import { supabase } from "@/supabase";

// ------------------------------
// Mock fetch
// ------------------------------
global.fetch = vi.fn();

beforeEach(() => {
  vi.clearAllMocks();
});

describe("Signup Page Unit Tests", () => {

  it("shows error when passwords do not match", async () => {
    const wrapper = mount(SignupPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.password = "abc123";
    wrapper.vm.confirmPassword = "zzz999";

    await wrapper.vm.handleSubmit();

    expect(wrapper.vm.message.type).toBe("error");
  });

  it("sets loading state on submit", async () => {
    supabase.auth.signUp.mockResolvedValue({
      data: { user: { id: "123" } },
      error: null,
    });

    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({}),
    });

    const wrapper = mount(SignupPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.email = "test@example.com";
    wrapper.vm.password = "abc123";
    wrapper.vm.confirmPassword = "abc123";

    const promise = wrapper.vm.handleSubmit();

    expect(wrapper.vm.isLoading).toBe(true);

    await promise;
  });

  it("shows success message on valid signup", async () => {
    supabase.auth.signUp.mockResolvedValue({
      data: { user: { id: "user-1" } },
      error: null,
    });

    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({}),
    });

    const wrapper = mount(SignupPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.email = "test@example.com";
    wrapper.vm.password = "abc123";
    wrapper.vm.confirmPassword = "abc123";

    await wrapper.vm.handleSubmit();

    expect(wrapper.vm.message.type).toBe("success");
  });

  it("shows error if Supabase returns an error", async () => {
    supabase.auth.signUp.mockResolvedValue({
      data: null,
      error: { message: "Email already exists" },
    });

    const wrapper = mount(SignupPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.email = "duplicate@example.com";
    wrapper.vm.password = "abc123";
    wrapper.vm.confirmPassword = "abc123";

    await wrapper.vm.handleSubmit();   // FIXED

    expect(wrapper.vm.message.type).toBe("error");
  });

  it("shows error if Data API request fails", async () => {
    supabase.auth.signUp.mockResolvedValue({
      data: { user: { id: "user-1" } },
      error: null,
    });

    global.fetch.mockResolvedValue({
      ok: false,
      json: () => Promise.resolve({ message: "API Error" }),
    });

    const wrapper = mount(SignupPage, {
      global: { plugins: [router] },
    });

    wrapper.vm.email = "test@example.com";
    wrapper.vm.password = "abc123";
    wrapper.vm.confirmPassword = "abc123";

    await wrapper.vm.handleSubmit();   // FIXED

    expect(wrapper.vm.message.type).toBe("error");
  });

});

