// Get all radio buttons
const radioButtons = document.querySelectorAll('input[type="radio"]');

// Function to handle radio button change event
function handleRadioButtonChange() {
  // Loop through all radio buttons
  for (let i = 0; i < radioButtons.length; i+=1) {
    const radioButton = radioButtons[i];
    
    // Check if the radio button is checked
    if (radioButton.checked) {
      // Get the parent <li> element
      const parentLi = radioButton.closest('li');
      
      // Change the background color of the parent <li> to white
      parentLi.style.backgroundColor = '#F2BC00';
    } else {
      // Get the parent <li> element
      const parentLi = radioButton.closest('li');
      
      // Revert the background color of the parent <li> to its original color
      parentLi.style.backgroundColor = ''; // or the original color value
    }
  }
}

// Add event listener to each radio button
for (let i = 0; i < radioButtons.length; i+=1) {
  const radioButton = radioButtons[i];
  radioButton.addEventListener('change', handleRadioButtonChange);
}

// Trigger the change event for the initially checked radio button
const initiallyCheckedRadioButton = document.querySelector('input[type="radio"]:checked');
handleRadioButtonChange.call(initiallyCheckedRadioButton);

