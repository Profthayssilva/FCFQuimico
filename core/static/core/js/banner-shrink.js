/* ===============================
   1️⃣ HEADER TRANSPARENTE + EFEITO SHRINK
   =============================== */
window.addEventListener("scroll", function() {
    const header = document.querySelector(".cabecalho");
    if (!header) return;

    if (window.scrollY > 80) {
        header.classList.add("scrolled");
    } else {
        header.classList.remove("scrolled");
    }
});

/* ===============================
   2️⃣ BANNER DE CONTATO / PRODUTO - SHRINK SUAVE
   =============================== */
window.addEventListener("scroll", function() {
    const banners = document.querySelectorAll(".banner-contato, .banner-produto");
    if (!banners.length) return;

    const shrinkLimit = 150; // distância de rolagem para encolher

    banners.forEach(banner => {
        if (window.scrollY > shrinkLimit) {
            banner.classList.add("shrink");
        } else {
            banner.classList.remove("shrink");
        }
    });
});

/* ===============================
   3️⃣ FORMULÁRIO DE CONTATO - FADE-IN SUAVE
   =============================== */
window.addEventListener("scroll", function() {
    const formSection = document.querySelector(".formulario-contato");
    if (!formSection) return;

    const sectionTop = formSection.getBoundingClientRect().top;
    const triggerHeight = window.innerHeight * 0.85;

    if (sectionTop < triggerHeight) {
        formSection.style.opacity = "1";
        formSection.style.transform = "translateY(0)";
    }
});
