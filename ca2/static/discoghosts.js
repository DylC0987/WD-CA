// *NOTES*
// Images and Music * Accreditations when required has been made at end of index page for images, Background Music loop was composed by me and is not meant for re-use outside of this game.
// CHEAT - This game has been designed to be tough, so for test purposes press "p" to toggle on and off cheatMode, cheatMode will prevent collisions between the player and ghosts, thus meaning the game won't end and the player is invincible.

let canvas;
let context;

let fpsInterval = 1000 / 30; // the denominator is frames-per-second
let now;
let then = Date.now();
let request_id;
let xhttp;

let backgroundImage = new Image();
let playerImage = new Image();
let ghostImage = new Image();
let ghost2Image = new Image();
let ghost3Image = new Image();
let barImage = new Image();
let tablechairImage = new Image();
let sofaImage = new Image();
let chairImage = new Image();
let discoballImage = new Image();
let heavenImage = new Image();
let backgroundMusic = new Audio();

let cheatMode = false
let musicStarted = false;
let ghostSpawnBegin = false;
let kill_count = 0;

let discoball = {
  x: 0,
  y: 0,
  width: 70,
  height: 70,
  visible: true // This will be used as a condition so the player can't collide with a Discoball when it's not visible to the player
};
let ghosts = [];
let bullets = [];
let player = {
  x : 0, 
  y : 0,
  borderw : 55,
  borderh : 55,
  size: 100,  
  width : 73.5,
  height : 73.5,
  frameX : 0,
  frameY : 0,
  xChange : 8,
  yChange : 8,
  shoot_direction: "up",
  hasBullets: false,
  bulletAcquiredAt: null // This will be used to track time of player getting bullets so we can compare it to the BulletDuration and remove bullet time 
};

let bar = {
  x : 325,
  y : 325,
  width: 170,
  height:170
}

let tableChair = {
  x : 590,
  y : 550,
  width: 200,
  height:150

}

let sofa = {
  x : 0,
  y : 300,
  width: 100,
  height:150

}

let chair = {
  x : 600,
  y : 130,
  width: 70,
  height:100

}

const blockedAreas = [bar, tableChair, sofa, chair];

const bulletDuration = 10000;

let playerAnimationCounter = 0;

//This value determines how often the animation frame updates. Increasing the value will make the animation slower, 
//while decreasing it will make the animation faster.
const playerAnimationUpdate = 5; 

let moveLeft = false;  
let moveRight = false;  
let moveUp = false;  
let moveDown = false;  
let shoot = false

document.addEventListener("DOMContentLoaded", init, false);

function init() {
  canvas = document.querySelector("canvas");
  context = canvas.getContext("2d");

  // Player start location
  player.x = 370
  player.y =  460
  
  
  spawnDiscoball() // intialise discoball 
  displayKillCount();
  

  window.addEventListener("keydown", activate, false);
  window.addEventListener("keyup", deactivate, false);
  
  
  load_assets([
       
    {"var": backgroundImage, "url": "static/Background_Game.png"},
    {"var": playerImage, "url": "static/player_sprite2.png"},
    {"var": ghostImage, "url": "static/ghost1_sprite.png"},
    {"var": ghost2Image, "url": "static/ghost2_sprite.png"},
    {"var": ghost3Image, "url": "static/ghost3_sprite.png"},
    {"var": barImage, "url": "static/barimage.png"},
    {"var": tablechairImage, "url": "static/table_chair.png"},
    {"var": sofaImage, "url": "static/sofa.png"},
    {"var": chairImage, "url": "static/chair.png"},
    {"var": discoballImage, "url": "static/discoball.png"},
    {"var": heavenImage, "url": "static/heaven.jpg"},
    {"var": backgroundMusic, "url": "static/DGaudio.mp3"}
   
    
],draw);
}

function draw() {
  request_id  = window.requestAnimationFrame(draw);
  let now = Date.now();
  let elapsed = now - then;
  if (elapsed <= fpsInterval) {
    return;
  }
  
  then = now - (elapsed % fpsInterval);
  
  context.clearRect(0, 0, canvas.width, canvas.height);

  //-----------------------------------------------------------------BACKGROUND---------------------------------------------------------------------------

  // Draw the background image
  context.drawImage(backgroundImage, 0, 0, canvas.width, canvas.height);

  //-----------------------------------------------------------------OBJECTS---------------------------------------------------------------------------
  context.drawImage(barImage,bar.x,bar.y,bar.width,bar.height)
  context.drawImage(tablechairImage,tableChair.x,tableChair.y,tableChair.width,tableChair.height)
  context.drawImage(sofaImage,sofa.x,sofa.y,sofa.width,sofa.height)
  context.drawImage(chairImage,chair.x,chair.y,chair.width,chair.height)

//-----------------------------------------------------------------PLAYER------------------------------------------------------------

  // PLAYER DRAW
  context.drawImage(playerImage,
    player.frameX * player.width, player.frameY * player.height, player.width, player.height,
    player.x, player.y, player.width, player.height);
  
  if (moveLeft || moveRight || moveDown || moveUp)  {
      playerAnimationCounter += 1;
    if (playerAnimationCounter >= playerAnimationUpdate) {
      player.frameX = (player.frameX + 1) % 4; //  4 frames in the sprite sheet for the player animation
      playerAnimationCounter = 0;
      }
    }  

  if (player.hasBullets === false)  {
    if (moveLeft) {
      player.frameY = 1;
    } else if (moveRight) {
      player.frameY = 0;
    } else if (moveUp) {
      player.frameY = 2;
    } else if (moveDown) {
      player.frameY = 3;
    } 
  } // Animation direction will change based on shooting direction when hasBullets is true, instead of arrow keys(movement)
  else if (player.hasBullets === true) {
    if (player.shoot_direction === "left") {
      player.frameY = 1;
    } else if (player.shoot_direction === "right") {
      player.frameY = 0;
    } else if (player.shoot_direction === "up") {
      player.frameY = 2;
    } else if (player.shoot_direction === "down") {
      player.frameY = 3;
    } 
  }

updateTimer();

// Check if the player has bullets and if the bullet duration has expired.
if (player.hasBullets && Date.now() - player.bulletAcquiredAt > bulletDuration) {
  player.hasBullets = false;
  discoball.visible = true; // Set Visible to true when the timer runs out
  spawnDiscoball();
}

//---------------------------------------------------------------BULLETS-----------------------------------------------------------------------------
// Draw and update bullets
for (let i = 0; i < bullets.length; i += 1) {
  let bullet = bullets[i];
  let removeBullet = false;

// Update bullet position
bullet.x += bullet.vx;
bullet.y += bullet.vy;


let bulletInBlockedArea = bulletCollidingWithBlockedArea(bullet)
let bulletOutsideCanvas = bullet.x < 0 || bullet.x > canvas.width || bullet.y < 0 || bullet.y > canvas.height
  
  if (bulletInBlockedArea || bulletOutsideCanvas) {
    removeBullet = true;
  } else {
    //Check for bullet-ghost collision
    //Using For Loop to iterate through all the ghosts in the ghosts array. 
    //For each ghost, it checks if the bullet collides with the ghost by calling the bullet_collides_ghost() function (bullet and ghost objects as arguments)
    //If a collision is detected (bullet_collides_ghost) will return true 
    //the code removes the ghost from the ghosts array using the splice() method. 
    //The removeBullet variable is then set to true to indicate that the bullet should also be removed.
    for (let j = 0; j < ghosts.length; j += 1) {
      let ghost = ghosts[j];
      if (bullet_collides_ghost(bullet, ghost)) {
        ghosts.splice(j, 1);
        removeBullet = true;
        kill_count += 1;
        displayKillCount();
        j -= 1;
    
        
      }
    }
  }

  // Removing bullets
  if (removeBullet) {
    bullets.splice(i, 1);
    i -= 1; // since we removed a bullet, the array elements will shift, causing one of them to take over the empty gap made by the spliced bullet,
  // we need to decrement so this shifted bullet doesn't get skipped in the loop as otherwise the loop will continue to the next place rather than checking this filled gap..
  } else {
    // Draw the bullet
    context.fillStyle = "chartreuse";
context.beginPath();
context.arc(bullet.x + bullet.size , //Centre of the circle x-coordinate
            bullet.y + bullet.size , //Centre of the circle y-coordinate
            bullet.size, // The radius of the circle
            0, // The starting angle of the arc
            360); // The ending angle of the arc (360degrees)
context.fill();
  }
} 

//--------------------------------------------------------------DISCOBALL------------------------------------------------------------------------------



if (player_collides_discoball(discoball) && discoball.visible === true) {
  player.hasBullets = true;
  player.bulletAcquiredAt = Date.now();
  discoball.visible = false; 
}


// Draw the discoball if it is visible
if (discoball.visible === true) {
  context.drawImage(discoballImage, discoball.x, discoball.y, discoball.width, discoball.height);
}

//--------------------------------------------------------------GHOSTS------------------------------------------------------------------------------

// Iterate through each ghost in the ghosts array
for (let ghost of ghosts) {

 // This is the end game condition
  if (player_collides_ghost(ghost) && cheatMode === false) {
    
    stop();
    return;
  }

  // Calculate the horizontal distance between the player and the ghost.
  let directionX = player.x - ghost.x;
  // Calculate the vertical distance between the player and the ghost.
  let directionY = player.y - ghost.y;

  // Calculate the straight-line distance between the ghost and the player 
  let distance = Math.sqrt(directionX * directionX + directionY * directionY);

  // Ensure that the ghost moves at a constant speed towards the player regardless of the distance between them.
  let normalisedX = directionX / distance;
  let normalisedY = directionY / distance;

  //Update the ghost's x-coordinate by adding the normalised x-direction multiplied by the ghost's speed horizontally (ghost.xChange). 
  ghost.x += normalisedX * ghost.xChange;

  //Update the ghost's y-coordinate by adding the normalized y-direction multiplied by the ghost's speed vertically (ghost.yChange). 
  ghost.y += normalisedY * ghost.yChange;


// Check if ghost is colliding with blocked area.
let ghostInBlockedArea = isCollidingWithBlockedArea(ghost.x, ghost.y, ghost);

// Changing ghosts speed and frame depending on if it's in a blocked area and/or if it has turned into a more aggressive ghost.
if (ghostInBlockedArea) {
  if (kill_count < 10){
    ghost.xChange = 1;
    ghost.yChange = 1;
    ghost.frameX = 1
    }else if (kill_count <= 20) {
      ghost.xChange = 1.5;
    ghost.yChange = 1.5;
    ghost.frameX = 1
      }else  {
        ghost.xChange = 2;
      ghost.yChange = 2;
      ghost.frameX = 1
        }

} else {
  if (kill_count < 10){
  ghost.xChange = 1.5;
  ghost.yChange = 1.5;
  ghost.frameX = 0
  }else if (kill_count <= 20) {
    ghost.xChange = 2.5;
  ghost.yChange = 2.5;
  ghost.frameX = 0
    }else  {
      ghost.xChange = 3;
    ghost.yChange = 3;
    ghost.frameX = 0
      }
}


  updateGhostDirection(ghost);

  

  // Draw the ghost *hard-coded width and height for this one to work properly*
if (kill_count < 10) {
  context.drawImage(ghostImage,
    75.591 * ghost.frameX, 75.591 * ghost.frameY, 75.591, 75.591,
    ghost.x, ghost.y, ghost.width, ghost.height);
  } else if (kill_count <= 20) {
  context.drawImage(ghost3Image,
    75.591 * ghost.frameX, 75.591 * ghost.frameY, 75.591, 75.591,
    ghost.x, ghost.y, ghost.width, ghost.height);
  } else {
  context.drawImage(ghost2Image,
    75.591 * ghost.frameX, 75.591 * ghost.frameY, 75.591, 75.591,
    ghost.x, ghost.y, ghost.width, ghost.height);
  }

}


//-----------------------------------------------------------------MOVING PLAYER---------------------------------------------------------------------------

if (moveLeft && player.x - player.xChange >= 0 && !isCollidingWithBlockedArea(player.x - player.xChange, player.y, player)) {
  player.x = player.x - player.xChange;
}
if (moveRight && player.x + player.xChange + player.width <= canvas.width && !isCollidingWithBlockedArea(player.x + player.xChange, player.y, player)) {
  player.x = player.x + player.xChange;
}

if (moveUp && player.y - player.yChange >= 0 && !isCollidingWithBlockedArea(player.x, player.y - player.yChange, player)) {
  player.y = player.y - player.yChange;
}

if (moveDown && player.y + player.yChange + player.height <= canvas.height && !isCollidingWithBlockedArea(player.x, player.y + player.yChange, player)) {
  player.y = player.y + player.yChange;
}

}
//-----------------------------------------------------------------FUNCTIONS---------------------------------------------------------------------------

function randint(min, max) {
  return Math.round(Math.random() * (max - min)) + min;
}

function spawnDiscoball() {
  // Set of coordinates for spawning
  const locations = [
    { x: 50, y: 50 },
    { x: 200, y: 300 },
    { x: 700, y: 80 },
    { x: 75, y: 600 },
    { x: 600, y: 350 }
  ];

  // Choose a random index from the locations array
  const randomIndex = Math.floor(Math.random() * locations.length);

  // Assign the random location's x and y coordinates to discoball
  discoball.x = locations[randomIndex].x;
  discoball.y = locations[randomIndex].y;
  
}

function spawnGhost() {
  // Choose a random side of the canvas (0: top, 1: right, 2: bottom, 3: left)
  let side = randint(1,4);

  let startX;
  let startY;

  if (side === 1) {
   // Top
   startX = randint(0, canvas.width - 10);
   startY = 0;
  }
  else if (side === 2)// Right
     { startX = canvas.width - 10;
      startY = randint(0, canvas.height - 10);
     }
      
  else if (side === 3) // Bottom
     { startX = randint(0, canvas.width - 10);
      startY = canvas.height - 10;
     }
     
  else if (side === 4) // Left
     { startX = 0;
      startY = randint(0, canvas.height - 10);
     }
      
     let ghost = {
      x: startX,
      y: startY,
      borderh: 50,
      borderw: 60,
      size: 30,
      xChange: 0,
      yChange: 0,
      width: 80,
      height: 80,
      frameX: 0,
      frameY: 0,
      zombieAnimationCounter: 0 
    };

  ghosts.push(ghost);

  // Calculate the time until the next ghost spawns
  let spawnInterval;
  if (kill_count <= 3) {
    spawnInterval = 3000;
  } else if (kill_count <= 7) {
    spawnInterval = 2000;
  } else if (kill_count <= 12) {
    spawnInterval = 1800;
  }else if (kill_count <= 16) {
    spawnInterval = 1600;
  }else if (kill_count <= 20) {
    spawnInterval = 1400;
  }else {
    spawnInterval = 1200;
  }

  // Call spawnGhost again with the calculated delay
  setTimeout(spawnGhost, spawnInterval);
}

function updateGhostDirection(ghost) {
  // Math.atan2 takes two arguments: the difference in y-coordinates (player.y - ghost.y) and the difference in x-coordinates (player.x - ghost.x).
  // Since the angle is initially in radians, it is then converted to degrees by multiplying it by (180 / Math.PI). 
  // This is done because it's easier to work with degrees when defining angle ranges for directions (up, down, left, right).
  let angle = Math.atan2(player.y - ghost.y, player.x - ghost.x) * (180 / Math.PI);

  if (angle >= -45 && angle <= 45) {
    ghost.frameY = 0; // Right
  } else if (angle > 45 && angle < 135) {
    ghost.frameY = 2; // Up
  } else if (angle >= 135 || angle <= -135) {
    ghost.frameY = 1; // Left
  } else if (angle < -45 && angle > -135) {
    ghost.frameY = 3; // Down
  }
}

function createBullet() {
  let bullet = {
    x: player.x + player.width / 2,
    y: player.y + player.height / 2,
    size: 5,
    width: 20,
    height: 20,
    // vx/vy will determine how the bullet will move when it is fired by the player.
    vx: 0,
    vy: 0
  };

// Lines up bullet with gun image location and also sets bullet's velocity.
if (player.shoot_direction === 'left') {
  bullet.x = bullet.x - 35;
  bullet.y = bullet.y - 29;
  bullet.vx = -5;
} else if (player.shoot_direction === 'right') {
    bullet.x = bullet.x + 30;
    bullet.y = bullet.y + 19;
    bullet.vx = 5;
} else if (player.shoot_direction === 'up') {
    bullet.x = bullet.x + 19;
    bullet.y = bullet.y - 35
    bullet.vy = -5;
} else if (player.shoot_direction === 'down') {
    bullet.x = bullet.x - 28;
    bullet.y = bullet.y + 35
    bullet.vy = 5;
}

  bullets.push(bullet);
}

function player_collides_discoball(discoball) {
  if (
    player.x + player.width < discoball.x ||
    discoball.x + discoball.width < player.x ||
    player.y > discoball.y + discoball.height ||
    discoball.y > player.y + player.height
  ) {
    return false;
  } else {
    return true;
  }
}

// // The n in code was calculated using a test border variable that was drawn for visual representation of perimeter:
// let border = {
//   x : player.x,
//   y : player.y,
//   width : 55,
//   height : 55

// }
//      // Draw the player sprite outline
// context.beginPath();
// context.rect(border.x + 0, border.y + 10, border.width, border.height);
// context.stroke();

function player_collides_ghost(ghost) {
  if (player.x + player.borderw < ghost.x + 10 ||
    ghost.x + 10 + ghost.borderw < player.x ||
      player.y + 10 > ghost.y + 12.5 + ghost.borderh ||
      ghost.y + 12.5 > player.y + 10 + player.borderh) {
      return false;
  } else {
      return true;
  }
}

function bullet_collides_ghost(bullet, ghost) {
  if (
    bullet.x + bullet.size  < ghost.x + 5 ||
    ghost.x + ghost.borderw + 5 < bullet.x ||
    bullet.y > ghost.y + ghost.borderh + 7||
    ghost.y + 7 > bullet.y + bullet.size 
  ) {
    return false;
  } else {
    return true;
  }
}

function isCollidingWithBlockedArea(x, y, moving_object) {
  let buffer = 35; //This line sets a buffer value that we can adjust to increase or decrease the allowed proximity around the objects.
  // The buffer value creates an "invisible margin" around the objects, allowing the moving object to get closer or further away from the actual boundaries of the blocked areas
  for (let area of blockedAreas) {
    if (
      x + moving_object.width - buffer > area.x && // Checks if the left side of the moving_object is to the right of the left side of the blocked area(object), accounting for the buffer. If the condition is true, it means the moving_object is not colliding with the left side of the blocked area(object).
      x + buffer < area.x + area.width && //  checks if the right side of the moving object is to the left of the right side of the blocked area, accounting for the buffer. If the condition is true, it means the moving object is not colliding with the right side of the blocked area.
      y + moving_object.height - buffer > area.y && // checks if the top side of the moving object is below the top side of the blocked area, accounting for the buffer. If the condition is true, it means the moving object is not colliding with the top side of the blocked area.
      y + buffer < area.y + area.height //  checks if the bottom side of the moving object is above the bottom side of the blocked area, accounting for the buffer. If the condition is true, it means the moving object is not colliding with the bottom side of the blocked area.
    ) {
      return true;
    }
  }
  return false;
}

function bulletCollidingWithBlockedArea(bullet) {
  let buffer = 10; 

  for (let area of blockedAreas) {
    if (
      bullet.x + bullet.size - buffer > area.x && 
      bullet.x + buffer < area.x + area.width && 
      bullet.y + bullet.height - buffer > area.y && 
      bullet.y + buffer < area.y + area.height 
    ) {
      return true;
    }
  }
  return false;
}
//Displays our kill_count variable score on our webpage.
function displayKillCount() {
  let score_element = document.querySelector("#kill_count");
  score_element.innerHTML = "Kill Count: " + kill_count;
}
//Displays the Bullet Time timer when active.
function updateTimer() {
  if (player.hasBullets) {
    let timeRemaining = bulletDuration - (Date.now() - player.bulletAcquiredAt);
    let secondsRemaining = Math.ceil(timeRemaining / 1000); // Using Ceiling instead of Round, as Round could round time to 0 before it hits it, falsely indicating bullet time is over.
    document.querySelector("#timer").innerHTML = "Bullet Time: " + secondsRemaining + " seconds";
  } else {
    document.querySelector("#timer").innerHTML = "";
  }
}

function activate(event) {
  let key = event.key; 
  if (key === "p") {
    cheatMode = !cheatMode; // "p" will activate the opposite state of whatever cheatMode is currently at
  }

  if (key === "ArrowLeft") {
    moveLeft= true;
    
  } else if(key === "ArrowRight") {
    moveRight = true; 
    
  } else if (key === "ArrowUp") {
    moveUp = true; 
    
  } else if (key === "ArrowDown"){
    moveDown = true; 
    
  }else if (key === " " && player.hasBullets == true ) {
      shoot = true;
      createBullet();
  }
  if (key === "a") {
    
    player.shoot_direction = 'left';
  } else if(key === "d") {
    
    player.shoot_direction = 'right';
  } else if (key === "w") {
    
    player.shoot_direction = 'up';
  } else if (key === "s"){
     
    player.shoot_direction = 'down';
  }

  // Start music and spawn the first ghost when the player starts moving
  if (!musicStarted && (moveLeft || moveRight || moveUp || moveDown)) {
    backgroundMusic.loop = true;
    backgroundMusic.play();
    musicStarted = true;

    if (!ghostSpawnBegin) {
      ghostSpawnBegin = true;
      spawnGhost(); // Spawn the initial ghost
    }
  }
  
}

function deactivate(event) {
  let key = event.key; 

  if (key === "ArrowLeft") {
    moveLeft= false;
    
  } else if(key === "ArrowRight") {
    moveRight = false; 
    
  } else if (key === "ArrowUp") {
    moveUp = false; 
   
  } else if (key === "ArrowDown"){
    moveDown = false; 
    
  }
  else if (key === " " && player.hasBullets == true ) {
    shoot = false;
  }
  if (key === "a") {
    
    player.shoot_direction = 'left';
  } else if(key === "d") {
    
    player.shoot_direction = 'right';
  } else if (key === "w") {
    
    player.shoot_direction = 'up';
  } else if (key === "s"){
     
    player.shoot_direction = 'down';
  }
}

function load_assets(assets, callback) {
  let num_assets = assets.length;
  let loaded = function() {
      console.log("loaded");
      num_assets = num_assets - 1;
      if (num_assets === 0) {
          callback();
      }
  };
  for (let asset of assets) {
      let element = asset.var;
      if (element instanceof HTMLImageElement ) {
          console.log("img"); 
          element.addEventListener("load", loaded, false);
      }
      else if (element instanceof HTMLAudioElement) {
          console.log("audio");
          element.addEventListener("canplaythrough", loaded, false);
      }
  element.src = asset.url;
}
}


function stop() {
  window.removeEventListener("keydown", activate, false);
  window.removeEventListener("keyup", deactivate, false);
  window.cancelAnimationFrame(request_id);
  backgroundMusic.pause();

  // Clear the canvas
  context.clearRect(0, 0, canvas.width, canvas.height);

  // Draw endgame image
  context.drawImage(heavenImage, 0, 0, canvas.width, canvas.height)

  // Display "You Died" text
  context.font = '60px Arial';
  context.fillStyle = 'red';
  context.textAlign = 'center';
  context.fillText("You Died", canvas.width / 2, canvas.height / 2 - 40); // Move this text up

  // Display "Kill count" text
  context.font = '40px Arial'; 
  context.fillStyle = 'white'; 
  context.fillText("Kill Count = " + kill_count, canvas.width / 2, canvas.height / 2 + 40); // Move this text down

  // This is going into my Flask app
  // "score = int(request.form["score"])"
  let data = new FormData();
  data.append("score", kill_count);

  xhttp = new XMLHttpRequest();
  xhttp.addEventListener("readystatechange", handle_response, false);
  xhttp.open("POST", "/store_score", true);
  xhttp.send(data);
 
}

function handle_response() {
  //Check the response has fully arrived
  if( xhttp.readyState === 4 ) {
      // Check the request was successful
      if ( xhttp.status === 200) {
          if( xhttp.responseText === "success") {
              // score was successfully stored in database
              console.log("Yes")
          } else {
            // score was not successfully stored in database
            console.log("No")

          }
      }
  }
}