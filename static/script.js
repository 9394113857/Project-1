// Function to validate the form fields
function formValidation() {
    var uid = document.registration.userid; // Get the User ID field
    var passid = document.registration.passid; // Get the Password field
    var uname = document.registration.username; // Get the Username field
    var uadd = document.registration.address; // Get the Address field
    var ucountry = document.registration.country; // Get the Country field
    var uzip = document.registration.zip; // Get the Zip field
    var uemail = document.registration.email; // Get the Email field
    var umsex = document.getElementById("msex"); // Get Male sex radio button
    var ufsex = document.getElementById("fsex"); // Get Female sex radio button

    // Validate User ID
    if(userid_validation(uid, 5, 12)) {
        // Validate Password
        if(passid_validation(passid, 7, 12)) {
            // Validate Username
            if(allLetter(uname)) {
                // Validate Address
                if(alphanumeric(uadd)) {
                    // Validate Country selection
                    if(countryselect(ucountry)) {
                        // Validate Zip Code
                        if(allnumeric(uzip)) {
                            // Validate Email
                            if(ValidateEmail(uemail)) {
                                // Validate Sex selection
                                if(validsex(umsex, ufsex)) {
                                    return true; // All validations passed
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return false; // Return false if any validation fails
}

// Function to validate User ID
function userid_validation(uid, mx, my) {
    var uid_len = uid.value.length; // Get the length of User ID
    if (uid_len == 0 || uid_len >= my || uid_len < mx) {
        alert("User ID should not be empty / length between " + mx + " to " + my); // Show alert if invalid length
        uid.focus(); // Focus on the User ID field
        return false; // Return false if invalid
    }
    return true; // Return true if valid
}

// Function to validate Password
function passid_validation(passid, mx, my) {
    var passid_len = passid.value.length; // Get the length of Password
    if (passid_len == 0 || passid_len >= my || passid_len < mx) {
        alert("Password should not be empty / length between " + mx + " to " + my); // Show alert if invalid length
        passid.focus(); // Focus on the Password field
        return false; // Return false if invalid
    }
    return true; // Return true if valid
}

// Function to validate if Username contains only alphabetic characters
function allLetter(uname) {
    var letters = /^[A-Za-z]+$/; // Regular expression for alphabetic characters
    if(uname.value.match(letters)) {
        return true; // Return true if valid
    } else {
        alert('Username must have alphabet characters only'); // Show alert if invalid
        uname.focus(); // Focus on the Username field
        return false; // Return false if invalid
    }
}

// Function to validate if Address is alphanumeric
function alphanumeric(uadd) {
    var letters = /^[0-9a-zA-Z\s]+$/; // Regular expression for alphanumeric characters
    if(uadd.value.match(letters)) {
        return true; // Return true if valid
    } else {
        alert('Address must be alphanumeric'); // Show alert if invalid
        uadd.focus(); // Focus on the Address field
        return false; // Return false if invalid
    }
}

// Function to validate if Country is selected
function countryselect(ucountry) {
    if(ucountry.value == "Default") {
        alert('Select your country from the list'); // Show alert if no country selected
        ucountry.focus(); // Focus on the Country field
        return false; // Return false if invalid
    } else {
        return true; // Return true if valid
    }
}

// Function to validate if Zip code contains only numeric values
function allnumeric(uzip) {
    var numbers = /^[0-9]+$/; // Regular expression for numeric values
    if(uzip.value.match(numbers)) {
        return true; // Return true if valid
    } else {
        alert('ZIP code must be numeric'); // Show alert if invalid
        uzip.focus(); // Focus on the Zip field
        return false; // Return false if invalid
    }
}

// Function to validate if Email is in a valid format
function ValidateEmail(uemail) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/; // Regular expression for email format
    if(uemail.value.match(mailformat)) {
        return true; // Return true if valid
    } else {
        alert("You have entered an invalid email address!"); // Show alert if invalid email
        uemail.focus(); // Focus on the Email field
        return false; // Return false if invalid
    }
}

// Function to validate if Sex is selected (Male or Female)
function validsex(umsex, ufsex) {
    let x = 0; // Counter for selected sex options
    if(umsex.checked) { x++; } // Increase counter if Male is selected
    if(ufsex.checked) { x++; } // Increase counter if Female is selected

    // If both options are selected
    if(x == 2) {
        alert('Both Male and Female are selected. Choose one.'); // Show alert if both are selected
        umsex.checked = false; // Uncheck Male
        ufsex.checked = false; // Uncheck Female
        return false; // Return false if both selected
    }
    if(x == 0) {
        alert('Select Male or Female'); // Show alert if none is selected
        return false; // Return false if none selected
    }
    return true; // Return true if valid
}
