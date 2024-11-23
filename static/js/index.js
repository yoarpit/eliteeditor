function validateForm() {
    let x = document.forms["login"]["email"].value;
    let y = document.forms["login"]["password"].value;
    if (x == "") {
      alert("Email must be filled out");
      return "/";
    }
    else if (y == "") {
        alert("Password  must be filled out");
        return "/";
      }
  }