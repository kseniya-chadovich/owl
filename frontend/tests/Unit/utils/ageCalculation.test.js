import { describe, it, expect } from "vitest";

function computeAge(birthday) {
  if (!birthday) return null;
  const birthYear = new Date(birthday).getFullYear();
  const now = new Date().getFullYear();
  return now - birthYear;
}

describe("Utils: Age Calculation", () => {
  it("calculates age correctly", () => {
    expect(computeAge("2000-01-01")).toBe(new Date().getFullYear() - 2000);
  });

  it("returns null for invalid birthday", () => {
    expect(computeAge("")).toBe(null);
  });
});
