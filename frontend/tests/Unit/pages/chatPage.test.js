import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import ChatPage from "@/components/chatpage.vue";
import { createRouter, createWebHistory } from "vue-router";

// ---- MOCK SUPABASE ----
vi.mock("@/supabase", () => ({
  supabase: {
    auth: {
      getUser: vi.fn(),
      signOut: vi.fn(),
    },
  },
}));

// ---- MOCK AXIOS ----
vi.mock("axios", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    delete: vi.fn(),
  },
}));

const axios = (await import("axios")).default;
const { supabase } = await import("@/supabase");

// ---- DUMMY ROUTER ----
const router = createRouter({
  history: createWebHistory(),
  routes: [],
});

// ---- FACTORY ----
async function mountChat() {
  const wrapper = mount(ChatPage, {
    global: {
      plugins: [router],
    },
  });

  // wait for onMounted(loadUser) + all async operations
  await flushPromises();
  return wrapper;
}

// ---- BEFORE EACH TEST ----
beforeEach(() => {
  vi.clearAllMocks();

  supabase.auth.getUser.mockResolvedValue({
    data: { user: { id: "test-user" } },
  });

  axios.get.mockResolvedValue({ data: { conversation: [] } });

  axios.post.mockResolvedValue({
    data: { payload: false }, // default assistant response
  });
});


// ======================================================
//                      TESTS
// ======================================================
describe("Chat Page Unit Tests", () => {

  it("does not send empty message", async () => {
    const wrapper = await mountChat();

    wrapper.vm.draftMessage = "";
    await wrapper.vm.sendMessage();

    // Should only contain the initial assistant greeting
    expect(wrapper.vm.messages.length).toBe(1);
  });

  it("adds user message to chat", async () => {
    axios.post.mockResolvedValueOnce({
      data: { payload: true }, // mock AI reply type
    });

    const wrapper = await mountChat();

    wrapper.vm.draftMessage = "Hello!";
    const p = wrapper.vm.sendMessage();

    // Immediately after sending, loading should start
    expect(wrapper.vm.isLoading).toBe(true);

    await p;
    await flushPromises();

    // assistant greeting + user + ai reply
    expect(wrapper.vm.messages.length).toBe(3);

    expect(wrapper.vm.messages[1].role).toBe("user");
    expect(wrapper.vm.messages[1].text).toBe("Hello!");

    expect(wrapper.vm.messages[2].role).toBe("assistant");
  });

  it("clears input after send", async () => {
    const wrapper = await mountChat();

    wrapper.vm.draftMessage = "Test";
    await wrapper.vm.sendMessage();
    await flushPromises();

    expect(wrapper.vm.draftMessage).toBe("");
  });

  it("sets loading indicator when waiting for response", async () => {
    const wrapper = await mountChat();

    wrapper.vm.draftMessage = "Schedule please";

    const p = wrapper.vm.sendMessage();

    // immediately true
    expect(wrapper.vm.isLoading).toBe(true);

    await p;
    await flushPromises();

    // finally false again
    expect(wrapper.vm.isLoading).toBe(false);
  });
});
