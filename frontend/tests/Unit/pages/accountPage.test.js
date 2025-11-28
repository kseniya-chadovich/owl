import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";
import AccountPage from "@/components/account.vue";
import { createRouter, createWebHistory } from "vue-router";

// mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [],
});

describe("Account Page Unit Tests", () => {

  function mountWithMocks() {
    const wrapper = mount(AccountPage, {
      global: {
        plugins: [router],
      },
    });

    // Prevent onMounted() from fetching data
    vi.spyOn(wrapper.vm, "fetchAccountDetails").mockImplementation(() => {});

    // Provide mock student data
    wrapper.vm.studentData = {
      personal: {
        full_name: "Test User",
        age: 25,
        is_international: true,
      },
      academic: {
        current_semester: 3,
        taken_courses: ["CIS 1051"],
        taken_geneds: ["GA"],
      },
    };

    return wrapper;
  }

  it("enters edit mode", async () => {
    const wrapper = mountWithMocks();

    wrapper.vm.enableEditing();
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.isEditing).toBe(true);
    expect(wrapper.vm.editData.full_name).toBe("Test User");
    expect(wrapper.vm.editData.taken_courses).toEqual(["CIS 1051"]);
  });

  it("cancels edit mode", async () => {
    const wrapper = mountWithMocks();

    wrapper.vm.enableEditing();
    expect(wrapper.vm.isEditing).toBe(true);

    wrapper.vm.cancelEditing();
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.isEditing).toBe(false);
  });

  it("updates taken_courses via watcher", async () => {
    const wrapper = mountWithMocks();

    wrapper.vm.editData.taken_courses_string = "CIS 1051, CIS 1068";
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.editData.taken_courses).toEqual([
      "CIS 1051",
      "CIS 1068",
    ]);
  });

  it("updates taken_geneds via watcher", async () => {
    const wrapper = mountWithMocks();

    wrapper.vm.editData.taken_geneds_string = "ga, gb, GS";
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.editData.taken_geneds).toEqual(["ga", "gb", "GS"]);
  });

  it("showMessage updates UI message", () => {
    const wrapper = mountWithMocks();

    wrapper.vm.showMessage("Updated", "success");

    expect(wrapper.vm.message.text).toBe("Updated");
    expect(wrapper.vm.message.type).toBe("success");
    expect(wrapper.vm.message.visible).toBe(true);
  });
});
