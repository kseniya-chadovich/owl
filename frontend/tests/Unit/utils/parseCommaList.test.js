import { describe, it, expect } from "vitest";

// copy from your code
function parseCommaList(raw) {
  if (!raw) return [];
  return raw
    .split(",")
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
}

describe("Utils: parseCommaList", () => {
  it("splits comma-separated values into an array", () => {
    const out = parseCommaList("CIS 1051, CIS 1068");
    expect(out).toEqual(["CIS 1051", "CIS 1068"]);
  });

  it("removes whitespace", () => {
    const out = parseCommaList("  A , B   , C ");
    expect(out).toEqual(["A", "B", "C"]);
  });

  it("returns empty array for empty input", () => {
    expect(parseCommaList("")).toEqual([]);
  });
});
