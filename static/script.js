
const menuBtn = document.getElementById("menuBtn");
const sidebar = document.getElementById("sidebar");

// Open and close sidebar on mobile
menuBtn.addEventListener("click", function () {
    sidebar.classList.toggle("open");
});

// Close sidebar after selecting a navigation link
const navLinks = document.querySelectorAll(".nav-link");

navLinks.forEach(function (link) {
    link.addEventListener("click", function () {

        navLinks.forEach(function (item) {
            item.classList.remove("active");
        });

        link.classList.add("active");

        if (window.innerWidth <= 768) {
            sidebar.classList.remove("open");
        }
    });
});
