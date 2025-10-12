function toggleSelect(el) {
  el.classList.toggle("selected");
}

document.getElementById("signupForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword")?.value;

  // Check if passwords match
  if (confirmPassword !== undefined && password !== confirmPassword) {
    alert("Passwords do not match. Please re-enter.");
    return;
  }

  const selectedCourses = Array.from(
    document.querySelectorAll("#courses .chip.selected")
  ).map((chip) => chip.textContent);

  const selectedGeneds = Array.from(
    document.querySelectorAll("#geneds .chip.selected")
  ).map((chip) => chip.textContent);

  const data = {
    firstName: document.getElementById("firstName").value,
    lastName: document.getElementById("lastName").value,
    email: document.getElementById("email").value,
    password: password,
    birthday: document.getElementById("birthday").value,
    international: document.querySelector('input[name="international"]:checked')
      ?.value,
    semester: document.getElementById("semester").value,
    enrollment: document.querySelector('input[name="enrollment"]:checked')
      ?.value,
    takenCourses: selectedCourses,
    geneds: selectedGeneds,
  };

  console.log("Form Data Submitted:", data);
  alert("Form submitted successfully!");
});
