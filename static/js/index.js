function validateForm() {
    let x = document.forms["login"]["email"].value;
    let y = document.forms["login"]["password"].value;
    // let u= document.forms["signup"]["email"].value;
    // let v = document.forms["signup"]["password"].value;
    if (x == "") {
      alert("Email must be filled out");
      
    }
    else if (y == "") {
        alert("Password  must be filled out");
      
      }

  //  if (u == "") {
  //       alert("Email must be filled out");
        
  //     }
  //  else if (v == "") {
  //         alert("Password  must be filled out");
          
  //       }
  }


  function validateform() {
    
    let u= document.forms["signup"]["email"].value;
    let v = document.forms["signup"]["password"].value;
   

   if (u == "") {
     let a= document.getElementById("my").innerHTML='<div class="alert alert-success" role="alert">A simple success alert—check it out!</div>';
        
      }
   else if (v == "") {
          alert("Password  must be filled out");
          
        }
  }