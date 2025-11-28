import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import SchedulePage from "@/components/schedule.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [],
});

describe("Schedule Page Unit Tests", () => {

  it("shows message when no schedule exists", async () => {
    const wrapper = mount(SchedulePage, {
      global: { plugins: [router] },
    });

    // Manually inject fake state
    wrapper.vm.schedule = { courses: [], total_credits: 0 };
    wrapper.vm.isLoading = false;

    await wrapper.vm.$nextTick();

    expect(wrapper.text().toLowerCase()).toContain("no schedule");
  });

  it("renders schedule when available", async () => {
    const wrapper = mount(SchedulePage, {
      global: { plugins: [router] },
    });

    // ★ NO API, NO AXIOS — DIRECTLY INJECT DATA
    wrapper.vm.schedule = {
      courses: [
        {
          course: "CIS 1051",
          day_time: "MW 9:30",
          instructor: "Smith",
          category: "Core",
          credits: 4,
          gened_type: null,
        },
      ],
      total_credits: 4,
    };
    wrapper.vm.isLoading = false;

    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain("CIS 1051");
  });

});
