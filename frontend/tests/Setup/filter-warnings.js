const originalWarn = console.warn;

console.warn = (msg, ...args) => {
  if (
    typeof msg === "string" &&
    (msg.includes("[Vue warn]") || msg.includes("[Vue Router warn]"))
  ) {
    return; // ignore these warnings
  }
  originalWarn(msg, ...args);
};
