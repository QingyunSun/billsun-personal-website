const revealables = document.querySelectorAll('[data-reveal="true"]');
const navLinks = document.querySelectorAll(".topnav a");
const sections = [...document.querySelectorAll("main section[id]")];

const revealVisibleSections = () => {
  for (const item of revealables) {
    const bounds = item.getBoundingClientRect();
    if (bounds.top < window.innerHeight * 0.92) {
      item.classList.add("is-visible");
    }
  }
};

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      }
    },
    { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
  );

  for (const item of revealables) {
    observer.observe(item);
  }
}

const setActiveNav = () => {
  let activeId = "";

  for (const section of sections) {
    const bounds = section.getBoundingClientRect();
    if (bounds.top <= 180 && bounds.bottom >= 180) {
      activeId = section.id;
      break;
    }
  }

  for (const link of navLinks) {
    link.classList.toggle("is-active", link.getAttribute("href") === `#${activeId}`);
  }
};

const handleScroll = () => {
  revealVisibleSections();
  setActiveNav();
};

document.addEventListener("scroll", handleScroll, { passive: true });
window.addEventListener("load", handleScroll);
window.addEventListener("resize", revealVisibleSections);
revealVisibleSections();
