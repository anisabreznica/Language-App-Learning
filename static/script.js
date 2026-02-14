function toggleMenu(event) {
    if (event) event.stopPropagation();
    const dropdown = document.getElementById("dropdown");
    if (dropdown) {
        dropdown.style.display = (dropdown.style.display === "none" || dropdown.style.display === "") ? "block" : "none";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.getElementById("dropdown");
    if (dropdown) {
        dropdown.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }
});


window.onclick = function(event) {
    if (!event.target.matches('.menu-icon') && !event.target.matches('.menu-line')) {
        const dropdown = document.getElementById("dropdown");
        if (dropdown && dropdown.style.display === "block") {
            dropdown.style.display = "none";
        }
    }
}


function speak(text, langCode) {
    window.speechSynthesis.cancel();

    const msg = new SpeechSynthesisUtterance(text);
    
    if (langCode === 'de') {
        msg.lang = 'de-DE';
    } else if (langCode === 'en') {
        msg.lang = 'en-US';
    } else if (langCode === 'sq') {
        msg.lang = 'sq-AL';
    }

    msg.rate = 0.9;  // Shpejtsia
    msg.pitch = 1.0; // Toni
    window.speechSynthesis.speak(msg);
}

let currentQuestionIdx = 0;
let score = 0;

function nextQuestion(isCorrect) {
    if (isCorrect) score++;
    
    currentQuestionIdx++;
}
