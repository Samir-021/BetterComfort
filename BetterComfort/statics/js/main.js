// ==============================================================================
// BetterComfort Main Client Scripts
// ==============================================================================

// Header Scroll Effect
const nav = document.querySelector(".navbar");
if (nav) {
    window.addEventListener("scroll", function () {
        if (document.documentElement.scrollTop > 50) {
            nav.classList.add("header-scrolled");
        } else {
            nav.classList.remove("header-scrolled");
        }
    });
}

// Auto-close mobile navbar on link click
const navLinks = document.querySelectorAll(".nav-link");
const navCollapse = document.querySelector(".navbar-collapse.collapse");
if (navLinks && navCollapse) {
    navLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            if (navCollapse.classList.contains("show")) {
                navCollapse.classList.remove("show");
            }
        });
    });
}

// Swiper Slider Initialization
if (document.querySelector(".mySwiper")) {
    new Swiper(".mySwiper", {
        direction: "vertical",
        loop: true,
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        autoplay: {
            delay: 4000,
            disableOnInteraction: false,
        },
    });
}

// Geolocation Handling
let userLat = null;
let userLon = null;
const latInput = document.getElementById("user-lat");
const lonInput = document.getElementById("user-lon");
const searchForm = document.getElementById("search-form");

function updateLocation(position) {
    userLat = position.coords.latitude;
    userLon = position.coords.longitude;

    if (latInput) latInput.value = userLat;
    if (lonInput) lonInput.value = userLon;

    console.log(`[bettercomfort] Location synchronized: ${userLat}, ${userLon}`);
}

function handleLocationError(error) {
    console.warn("[bettercomfort] Geolocation notice:", error.message);
    // Default fallback coordinates (Kathmandu, Nepal center: 27.7172, 85.3240)
    if (!userLat || !userLon) {
        userLat = 27.7172;
        userLon = 85.3240;
        if (latInput) latInput.value = userLat;
        if (lonInput) lonInput.value = userLon;
    }
}

// Initialize Location Detection
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(updateLocation, handleLocationError, {
        enableHighAccuracy: true,
        timeout: 7000,
        maximumAge: 60000,
    });
    navigator.geolocation.watchPosition(updateLocation, handleLocationError, {
        enableHighAccuracy: false,
        timeout: 10000,
        maximumAge: 120000,
    });
} else {
    handleLocationError({ message: "Geolocation not supported by browser." });
}

// Search form submit validation
if (searchForm) {
    searchForm.addEventListener("submit", (event) => {
        if (!latInput.value || !lonInput.value) {
            // Apply fallback coordinates if user coordinates aren't yet detected
            latInput.value = userLat || 27.7172;
            lonInput.value = userLon || 85.3240;
        }
    });
}
