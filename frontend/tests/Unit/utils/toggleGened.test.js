import { describe, it, expect } from "vitest";

function toggleGened(arr, item) {
  const i = arr.indexOf(item);
  if (i === -1) arr.push(item);
  else arr.splice(i, 1);
  return arr;
}

describe("Utils: toggleGened", () => {
  it("adds gened when not selected", () => {
    const out = toggleGened([], "GA");
    expect(out).toEqual(["GA"]);
  });

  it("removes gened when selected", () => {
    const out = toggleGened(["GA"], "GA");
    expect(out).toEqual([]);
  });
});
