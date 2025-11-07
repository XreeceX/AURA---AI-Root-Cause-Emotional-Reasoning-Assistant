(() => {
  // Analysis progress bar hooked to the existing Analyze button
  const progressHost = document.createElement('div');
  progressHost.className = 'progress';
  const bar = document.createElement('span');
  progressHost.appendChild(bar);

  const toolbar = document.querySelector('#go')?.parentElement;
  if (toolbar) toolbar.parentElement.insertBefore(progressHost, toolbar.nextSibling);

  let timer;
  function startProgress() {
    clearInterval(timer);
    bar.style.width = '0%';
    let w = 0;
    timer = setInterval(() => {
      w = Math.min(90, w + Math.max(1, (90 - w) * 0.08));
      bar.style.width = w + '%';
    }, 120);
  }
  function endProgress() {
    clearInterval(timer);
    bar.style.width = '100%';
    setTimeout(() => (bar.style.width = '0%'), 500);
  }

  // Tag reveal + mobile collapsible plan list
  const out = document.getElementById('out');
  const observer = new MutationObserver(() => {
    const tags = out.querySelectorAll('.tag');
    tags.forEach((el, i) => { el.style.animationDelay = `${i * 40}ms`; });

    // Make any <ol> or .plan-list sections collapsible on small screens
    const lists = out.querySelectorAll('ol, .plan-list');
    lists.forEach((list) => {
      if (list.dataset.enhanced) return;
      list.dataset.enhanced = '1';
      const wrapper = document.createElement('div');
      wrapper.className = 'collapsible open';
      wrapper.style.maxHeight = list.scrollHeight + 'px';
      list.parentNode.insertBefore(wrapper, list);
      wrapper.appendChild(list);
      const toggle = document.createElement('button');
      toggle.textContent = 'Toggle details';
      toggle.style.marginTop = '8px';
      toggle.className = 'btn';
      wrapper.parentNode.appendChild(toggle);
      toggle.addEventListener('click', () => {
        const isOpen = wrapper.classList.toggle('open');
        wrapper.style.maxHeight = isOpen ? list.scrollHeight + 'px' : '0px';
      });
    });
  });
  observer.observe(out, { childList: true, subtree: true });

  // Wrap existing onclick to add progress start/end
  const button = document.getElementById('go');
  if (button) {
    const original = button.onclick;
    button.onclick = async () => {
      startProgress();
      try {
        await original();
      } finally {
        endProgress();
      }
    };
  }
})();
