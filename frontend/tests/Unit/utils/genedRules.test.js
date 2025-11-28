import { describe, it, expect } from "vitest";

function autoGeneds(international, selected) {
  const list = [...selected];

  if (!list.includes("GS")) list.push("GS");
  if (international === "yes" && !list.includes("GG")) list.push("GG");

  return list;
}

describe("Utils: GenEd Rules", () => {
  it("adds GS for all students", () => {
    expect(autoGeneds("no", [])).toEqual(["GS"]);
  });

  it("adds GG for international students", () => {
    expect(autoGeneds("yes", ["GS"])).toEqual(["GS", "GG"]);
  });

  it("does not duplicate GenEds", () => {
    expect(autoGeneds("yes", ["GS", "GG"])).toEqual(["GS", "GG"]);
  });
});
