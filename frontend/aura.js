(() => {
  "use strict";

  const toolbar = document.querySelector("#go")?.parentElement;
  if (toolbar) {
    const progressHost = document.createElement("div");
    progressHost.className = "progress progress-analyzing";
    const bar = document.createElement("span");
    progressHost.appendChild(bar);
    toolbar.parentElement.insertBefore(progressHost, toolbar.nextSibling);

    let timer;
    function startProgress() {
      clearInterval(timer);
      bar.style.width = "0%";
      let w = 0;
      timer = setInterval(() => {
        w = Math.min(90, w + Math.max(1, (90 - w) * 0.08));
        bar.style.width = w + "%";
      }, 120);
    }
    function endProgress() {
      clearInterval(timer);
      bar.style.width = "100%";
      setTimeout(() => (bar.style.width = "0%"), 500);
    }

    const button = document.getElementById("go");
    if (button) {
      const original = button.onclick;
      button.onclick = async () => {
        startProgress();
        try {
          await original?.();
        } finally {
          endProgress();
        }
      };
    }
  }

  const out = document.getElementById("out");
  if (!out) return;

  const observer = new MutationObserver(() => {
    out.querySelectorAll(".tag").forEach((el, i) => {
      el.style.animationDelay = `${i * 40}ms`;
    });

    out.querySelectorAll("ol, .plan-list").forEach((list) => {
      if (list.dataset.enhanced) return;
      list.dataset.enhanced = "1";

      const wrapper = document.createElement("div");
      wrapper.className = "collapsible open";
      const maxOpen = 2000;
      wrapper.style.maxHeight = maxOpen + "px";

      list.parentNode.insertBefore(wrapper, list);
      wrapper.appendChild(list);

      const toggle = document.createElement("button");
      toggle.textContent = "Show/hide plan";
      toggle.className = "btn collapsible-toggle";
      toggle.setAttribute("type", "button");
      wrapper.parentNode.insertBefore(toggle, wrapper.nextSibling);

      toggle.addEventListener("click", () => {
        const isOpen = wrapper.classList.toggle("open");
        wrapper.style.maxHeight = isOpen ? maxOpen + "px" : "0";
      });
    });
  });
  observer.observe(out, { childList: true, subtree: true });
})();
