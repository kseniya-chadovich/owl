<template>
  <div class="page-background">
    <div class="container">
      <h1>Email Confirmation Sent!</h1>
      <p>
        A confirmation email has been sent to your inbox.
        <br />
        Please check your email and click the link to verify your account.
      </p>
    </div>
  </div>
</template>


<style scoped>
.page-background {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(to bottom right, #a41e34, #ffffff);
  color: #333;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  margin: 0;
  min-height: 100vh;
  width: 100%;
  position: relative;
}

.container {
    background-color: #fff;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    padding: 50px 60px;
    width: 90%;
    max-width: 750px; 
    text-align: center;
    box-sizing: border-box;
}



h1 {
    font-size: 28px;
    color: #a41e34;
    margin-bottom: 20px;
}

p {
    font-size: 18px;
    color: #333;
    line-height: 1.6;
}


.login-btn {
  width: 100%;
  background-color: #a41e34;
  color: #fff;
  padding: 12px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
}

.login-btn:hover {
  background-color: #8e162b;
}
</style>
