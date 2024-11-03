document.addEventListener("DOMContentLoaded", function() {
    const feedbackForm = document.getElementById("feedbackForm");

    feedbackForm.addEventListener("submit", function(event) {
        const studentName = document.getElementById("student_name").value.trim();
        const staffName = document.getElementById("staff_name").value.trim();
        const feedback = document.getElementById("feedback").value.trim();

        if (!studentName || !staffName || !feedback) {
            alert("All fields are required!");
            event.preventDefault();
        }
    });
});
