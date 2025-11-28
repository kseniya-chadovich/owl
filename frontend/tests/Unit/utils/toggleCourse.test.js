import { describe, it, expect } from "vitest";

function toggleCourse(arr, item) {
  const i = arr.indexOf(item);
  if (i === -1) arr.push(item);
  else arr.splice(i, 1);
  return arr;
}

describe("Utils: toggleCourse", () => {
  it("adds course when not selected", () => {
    const out = toggleCourse([], "CIS 1051");
    expect(out).toEqual(["CIS 1051"]);
  });

  it("removes course when already selected", () => {
    const out = toggleCourse(["CIS 1051"], "CIS 1051");
    expect(out).toEqual([]);
  });
});
